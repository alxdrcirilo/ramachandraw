from os.path import exists, realpath
from typing import Union

from Bio.PDB import PDBList


def get_file(pdb: str) -> str:
    """
    Fetches a PDB structure file if not already existent and returns a path to an existing file.
    :param pdb: filepath or accession to retrieve structure file
    :return: path to existing (PDB) file, empty string otherwise
    """
    if not exists(realpath(pdb)):
        path = fetch(pdb)
    else:
        path = pdb
    path = realpath(path)
    if not exists(path):
        path = ""
    return path


def fetch(pdb: Union[str, list, tuple]):
    def start(pdb_id: str):
        return PDBList(verbose=False).retrieve_pdb_file(pdb_code=pdb_id, pdir='PDB', file_format='pdb')
        # still may print "Desired structure doesn't exists" from retrieve_pdb_file function

    if isinstance(pdb, str):
        return start(pdb_id=pdb)
    if isinstance(pdb, (tuple, list)):
        return [start(pdb_id=entry) for entry in pdb]
