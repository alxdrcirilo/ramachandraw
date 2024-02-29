from itertools import chain

from ramachandraw.parser import get_phi_psi


def test_get_phi_psi_success_pruned(temp_dir, pdb_single):
    result = get_phi_psi(pdb_filepath=pdb_single)
    assert isinstance(result, dict)
    assert None not in list(chain(*result.values()))


def test_get_phi_psi_success_not_pruned(temp_dir, pdb_single):
    result = get_phi_psi(pdb_filepath=pdb_single, prune=False)
    assert isinstance(result, dict)
    assert None in list(chain(*result.values()))


def test_get_phi_psi_multiple(temp_dir, pdb_multiple):
    result = get_phi_psi(pdb_filepath=pdb_multiple)
    assert isinstance(result, list)
