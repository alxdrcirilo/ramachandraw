from Bio.PDB import PDBList
from typing import Union


def fetch(pdb: Union[str, list]):
    def start(pdb_id: str):
        return PDBList().retrieve_pdb_file(pdb_code=pdb_id, pdir='PDB', file_format='pdb')

    if type(pdb) is str:
        return start(pdb_id=pdb)
    if type(pdb) is list:
        return [start(pdb_id=entry) for entry in pdb]
