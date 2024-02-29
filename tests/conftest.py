import os
import shutil

import pytest

from ramachandraw.utils import fetch_pdb


@pytest.fixture(scope="session")
def temp_dir(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("temp_dir")
    os.chdir(temp_dir)
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture(scope="session")
def pdb_single():
    return fetch_pdb(pdb_id="1mbn")


@pytest.fixture(scope="session")
def pdb_multiple():
    return fetch_pdb(pdb_id=["1mbn", "4hhb"])
