import pytest

from ramachandraw import utils

SINGLE_PDB: list = [
    (["1mbn"], {}, (".pdb/pdb1mbn.ent")),
    ([], {"pdb_id": "1mbn"}, (".pdb/pdb1mbn.ent")),
]

MULTIPLE_PDB: list = [
    ([["1mbn", "4hhb"]], {}, ([".pdb/pdb1mbn.ent", ".pdb/pdb4hhb.ent"])),
    ([], {"pdb_id": ["1mbn", "4hhb"]}, ([".pdb/pdb1mbn.ent", ".pdb/pdb4hhb.ent"])),
]


@pytest.mark.parametrize("args, kwargs, expected_result", SINGLE_PDB + MULTIPLE_PDB)
def test_fetch_pdb_success(
    temp_dir,
    args: list[str] | list[list[str]],
    kwargs: dict[str, str] | dict[str, list[str]],
    expected_result: str | list[str],
) -> None:
    """Test `ramachandraw.parser.fetch_pdb` function with `*args` and `**kwargs`.

    :temp_dir: fixture to move to a temporary working directory (in `conftest.py`)
    :param list[str] | list[list[str]] args: arguments (e.g. `"1mbn"`)
    :param dict[str, str] | dict[str, list[str]] kwargs: keyword arguments
        (e.g. `pdb_id="1mbn"`)
    :param str | list[str] expected_result: path(s) to the PDB file(s)
        (e.g. `".pdb/pdb1mbn.ent"`)
    """
    result = utils.fetch_pdb(*args, **kwargs)
    assert result == expected_result


@pytest.mark.parametrize("args, kwargs", [(["1lyz"], {"verbose": True})])
def test_fetch_pdb_verbose(
    temp_dir,
    capsys: pytest.CaptureFixture[str],
    args: list[str] | list[list[str]],
    kwargs: dict[str, str] | dict[str, list[str]],
) -> None:
    """Test `ramachandraw.parser.fetch_pdb` function with `*args` and `**kwargs`.

    :param pytest.CaptureFixture[str] capsys: capture sysout fixture
    :param list[str] | list[list[str]] args: arguments (e.g. `"1mbn"`)
    :param dict[str, str] | dict[str, list[str]] kwargs: keyword arguments
        (e.g. `pdb_id="1mbn"`)
    """
    utils.fetch_pdb(*args, **kwargs)
    captured = capsys.readouterr()
    assert "Downloading PDB structure" in captured.out


@pytest.mark.parametrize("args, kwargs", [([], {})])
def test_fetch_pdb_raise_no_pdb_exception(
    temp_dir,
    args: list[str] | list[list[str]],
    kwargs: dict[str, str] | dict[str, list[str]],
) -> None:
    """Test `NoPdbIdProvided` is raised when no `pdb_id` is provided.

    :param list[str] | list[list[str]] args: arguments (e.g. `"1mbn"`)
    :param dict[str, str] | dict[str, list[str]] kwargs: keyword arguments
        (e.g. `pdb_id="1mbn"`)
    """
    with pytest.raises(utils.NoPdbIdProvided):
        utils.fetch_pdb(*args, **kwargs)
