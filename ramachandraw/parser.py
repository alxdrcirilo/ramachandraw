from collections import defaultdict
from math import degrees

from Bio.PDB import PDBParser, PPBuilder


def _extract_angles(pdb_file: str, hide_warnings: bool) -> dict[str, list]:
    """Extract the Φ-Ψ torsion angles from a single PDB file.

    :param str pdb_file: pdb filepath (e.g. `".pdb/pdb1mbn.ent"`)
    :param bool hide_warnings: silences PDBParser warnings if True
    :return dict[str, list]: angles keyed by aminoacid residue
    """
    angles: dict[str, list] = defaultdict(list)
    pdbp = PDBParser(QUIET=hide_warnings)
    ppb = PPBuilder()

    for model in pdbp.get_structure(id=None, file=pdb_file):
        for chain in model:
            for peptide in ppb.build_peptides(chain):
                residues = zip(peptide, peptide.get_phi_psi_list(), strict=False)
                for aminoacid, phi_psi in residues:
                    residue = f"{chain.id}:{aminoacid.resname}{aminoacid.id[1]}"
                    for angle in phi_psi:
                        try:
                            angles[residue].append(degrees(angle))
                        except TypeError:
                            angles[residue].append(None)
    return angles


def get_phi_psi(
    pdb_filepath: str | list | tuple,
    prune: bool = True,
    hide_warnings: bool = True,
) -> dict[str, list] | list[dict[str, list]]:
    """Get the Φ-Ψ torsion angles given a PDB file.

    This function will generate a dictionary with:
        - Key: 'Chain:AminoacidPosition' (e.g. A:ARG118)
        - Value: [Φ, Ψ] angles (e.g. [-42.8, -45.2])

    :param str | list | tuple pdb_filepath: pdb filepath(s) (e.g. `".pdb/pdb1mbn.ent"`)
    :param bool prune: prunes aminoacids with missing torsion angle(s), defaults to True
    :param bool hide_warnings: silences PDBParser warnings if True, defaults to True
    :return dict | list[dict]: dictionary of torsion angles (list if more than one)
    """
    if isinstance(pdb_filepath, str):
        pdb_filepath = [pdb_filepath]

    angles = []
    for pdb_file in pdb_filepath:
        pdb_angles = _extract_angles(pdb_file=pdb_file, hide_warnings=hide_warnings)
        if prune:
            pdb_angles = {k: v for (k, v) in pdb_angles.items() if None not in v}
        angles.append(pdb_angles)

    if len(angles) == 1:
        return angles[0]
    else:
        return angles
