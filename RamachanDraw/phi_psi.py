from Bio.PDB import PDBParser, PPBuilder
from math import pi
from rich.console import Console
from rich.table import Table

console = Console(color_system='windows')


def phi_psi(pdb_file, return_ignored=False):
    def get_ignored_res(file: str):
        x, y, ignored, output = [], [], [], {}
        for model in PDBParser().get_structure(id=None, file=file):
            for chain in model:
                peptides = PPBuilder().build_peptides(chain)
                for peptide in peptides:
                    for aa, angles in zip(peptide, peptide.get_phi_psi_list()):
                        residue = chain.id + ":" + aa.resname + str(aa.id[1])
                        output[residue] = angles

        for key, value in output.items():
            # Only get residues with both phi and psi angles
            if value[0] and value[1]:
                x.append(value[0] * 180 / pi)
                y.append(value[1] * 180 / pi)
            else:
                ignored.append((key, value))

        return output, ignored, x, y

    def start(fp: str):
        phi_psi_data, ignored_res, x, y = get_ignored_res(file=fp)

        if return_ignored:
            table = Table(title='Ignored residues')
            table.add_column('Aminoacid\nresidue', style='red')
            table.add_column('\u03C6-\u03C8\nangles', justify='center')
            for _ in ignored_res:
                table.add_row(_[0], str(_[1]))
            console.print(table)

            return phi_psi_data, ignored_res
        else:
            return phi_psi_data

    if type(pdb_file) is str:
        output = start(fp=pdb_file)
    if type(pdb_file) is list:
        output = []
        for file in pdb_file:
            output.append(start(fp=file))

    return output
