from Bio.PDB import *


def fetch(PDB_id):
    return PDBList().retrieve_pdb_file(pdb_code=PDB_id, pdir='PDB', file_format='pdb')
