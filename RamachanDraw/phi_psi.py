from math import pi
from typing import Union

from Bio.PDB import PDBParser, PPBuilder
from rich.console import Console
from rich.table import Table

from .fetch import get_file

console = Console(color_system='windows')


def get_ignored_res(pdb_file_path: str, ignore_pdb_warnings: bool = False) -> tuple[dict, list, list, list]:
    """
    Calculates the Phi/Psi angles and corresponding x-y values
    :param pdb_file_path:
    :param ignore_pdb_warnings:
    :return: [0] dictionary with chain:residue as key and tuple angles as value
             [1] list of tuples of ignored residues with tuple[0] residue name and tuple[1] of phi-psi angles as tuple
             [2] phi-angles
             [3] psi-angles
    """
    phi, psi, res_ignored, res_output = [], [], [], {}
    pdb_file_path = get_file(pdb_file_path)

    for model in PDBParser(PERMISSIVE=False, QUIET=ignore_pdb_warnings).get_structure(id=None, file=pdb_file_path):
        for chain in model:
            peptides = PPBuilder().build_peptides(chain)
            for peptide in peptides:
                for aa, angles in zip(peptide, peptide.get_phi_psi_list()):
                    residue = chain.id + ":" + aa.resname + str(aa.id[1])
                    res_output[residue] = angles

    for key, value in res_output.items():
        # Only get residues with both phi and psi angles
        if value[0] and value[1]:
            phi.append(value[0] * 180 / pi)
            psi.append(value[1] * 180 / pi)
        else:
            res_ignored.append((key, value))

    return res_output, res_ignored, phi, psi


def phi_psi(pdb_file: Union[str, tuple, list], return_ignored: bool = False, print_ignored: bool = False,
            ignore_pdb_warnings: bool = False) -> list:
    """
    Calculates phi-psi angles for given PDB file(s)
    :param pdb_file: PDB file path (or iterable of PDB file paths)
    :param return_ignored: additionally returns a tuple of ignored residues
    :param print_ignored: print a table of ignored residues with corresponding angles to console
    :param ignore_pdb_warnings: ignore all occurring warnings from PDB structure parser
    :return: a list of tuples with [0] dictionary with chain:residue as key and tuple angles as value
                                   [1] if return_ignored: list of tuples of ignored residues
    """
    if ignore_pdb_warnings:
        try:
            from Bio.PDB.PDBExceptions import PDBConstructionWarning
            from warnings import simplefilter
            simplefilter('ignore', PDBConstructionWarning)
        except ImportError:
            pass

    def start(fp: str) -> tuple:
        phi_psi_data, ignored_res, _, _ = get_ignored_res(pdb_file_path=fp, ignore_pdb_warnings=ignore_pdb_warnings)

        # print ignored residue table
        if print_ignored:
            table = Table(title='Ignored residues')
            table.add_column('Aminoacid\nresidue', style='red')
            table.add_column('\u03C6-\u03C8\nangles', justify='center')
            for ignored in ignored_res:
                table.add_row(ignored[0], str(ignored[1]))  # [0] chain:residue name, [1] tuple of phi-psi angles
            console.print(table)

        if return_ignored:
            return phi_psi_data, ignored_res
        else:
            return phi_psi_data,

    output = []
    if isinstance(pdb_file, str):
        output = [start(fp=pdb_file)]
    elif isinstance(pdb_file, (tuple, list)):
        for file in pdb_file:
            output.append(start(fp=file))

    return output
