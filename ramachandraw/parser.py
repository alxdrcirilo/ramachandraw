from collections import defaultdict
from math import degrees
from typing import Union

from Bio.PDB import PDBParser, PPBuilder


def get_phi_psi(
    pdb_filepath: Union[str, list, tuple],
    prune: bool = True,
    hide_warnings: bool = True,
) -> Union[dict[str, list], list[dict[str, list]]]:
    """Get the Φ-Ψ torsion angles given a PDB file.

    This function will generate a dictionary with:
        - Key: 'Chain:AminoacidPosition' (e.g. A:ARG118)
        - Value: [Φ, Ψ] angles (e.g. [-42.8, -45.2])

    :param Union[str, list, tuple] pdb_filepath: pdb filepath(s) (e.g. `".pbd/pdb1mbn.ent"`)
    :param bool prune: prunes aminoacids with missing torsion angle(s), defaults to True
    :param bool hide_warnings: logs PDBParser warnings if set to True, defaults to True
    :return Union[dict[str, list], list[dict[str, list]]]: dictionary of torsion angles (list if more than one)
    """

    def __extract_angles(pdb_file: str) -> dict[str, list]:
        """Extract the Φ-Ψ torsion angles.

        :param str pdb_file: pdb filepath (e.g. `".pbd/pdb1mbn.ent"`)
        :return dict[str, list]: dictionary with aminoacid residue as key, and Φ-Ψ angles as values
        """
        angles: dict[str, list] = defaultdict(list)
        pdbp = PDBParser(QUIET=hide_warnings)
        ppb = PPBuilder()

        for model in pdbp.get_structure(id=None, file=pdb_file):
            for chain in model:
                peptides = ppb.build_peptides(chain)
                for peptide in peptides:
                    for aminoacid, phi_psi in zip(peptide, peptide.get_phi_psi_list()):
                        residue = f"{chain.id}:{aminoacid.resname}{aminoacid.id[1]}"
                        for angle in phi_psi:
                            try:
                                angles[residue].append(degrees(angle))
                            except TypeError:
                                angles[residue].append(None)
        return angles

    if isinstance(pdb_filepath, str):
        pdb_filepath = [pdb_filepath]

    angles = []
    for pdb_file in pdb_filepath:
        pdb_angles = __extract_angles(pdb_file=pdb_file)
        if prune:
            pdb_angles = {k: v for (k, v) in pdb_angles.items() if None not in v}
        angles.append(pdb_angles)

    if len(angles) == 1:
        return angles[0]
    else:
        return angles
