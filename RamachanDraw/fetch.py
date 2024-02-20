from typing import Union
from os.path import exists, realpath, basename
from os import sep
from Bio.PDB import PDBList


def get_file(pdb:str):
    if not exists(realpath(pdb)):
        path = fetch(pdb)
    else:
        path = realpath(pdb)
    return path


def fetch(pdb: Union[str, list, tuple]):
    def start(pdb_id: str):
        return PDBList(verbose=False).retrieve_pdb_file(pdb_code=pdb_id, pdir='PDB', file_format='pdb')

    if isinstance(pdb, str):
        return start(pdb_id=pdb)
    if isinstance(pdb, (tuple, list)):
        return [start(pdb_id=entry) for entry in pdb]
