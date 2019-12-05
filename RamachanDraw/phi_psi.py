from Bio.PDB import PDBParser, PPBuilder
from math import pi


def phi_psi(pdb_file, return_ignored=False):
    # Initialize variables
    x, y = [], []
    # Initialize dictionary which holds the values of the torsion angles
    #   - Keys: residues
    #   - Values: torsion angles
    phi_psi_dict = {}

    for model in PDBParser().get_structure(id=None, file=pdb_file):
        # Create dictionary to store parsed values
        for chain in model:
            peptides = PPBuilder().build_peptides(chain)
            for peptide in peptides:
                for aminoacid, angles in zip(peptide, peptide.get_phi_psi_list()):
                    residue = aminoacid.resname + str(aminoacid.id[1])
                    phi_psi_dict[residue] = angles

    ignored_res = []
    for key, value in phi_psi_dict.items():
        # Only get residues with both phi and psi angles
        if value[0] and value[1]:
            x.append(value[0] * 180 / pi)
            y.append(value[1] * 180 / pi)
        else:
            ignored_res.append((key, value))

    if return_ignored:
        print('Warning!\nIgnored residues:\n=================')
        for res, angles in ignored_res:
            print(res, ':\t', angles)
        return phi_psi_dict, ignored_res
    else:
        return phi_psi_dict
