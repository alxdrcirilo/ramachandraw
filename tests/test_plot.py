from matplotlib.axes import Axes

from ramachandraw import utils


def test_plot_return_single(temp_dir, pdb_single):
    result = utils.plot(pdb_filepath=pdb_single)
    assert isinstance(result, Axes)


def test_plot_return_multiple(temp_dir, pdb_multiple):
    result = utils.plot(pdb_filepath=pdb_multiple)
    assert isinstance(result, Axes)


def test_plot_custom_title_single(temp_dir, pdb_single):
    result = utils.plot(
        pdb_filepath=pdb_single,
        title="My custom title",
        save=False,
    )
    assert result.get_title() == "My custom title"


def test_plot_default_title_single(temp_dir, pdb_single):
    result = utils.plot(
        pdb_filepath=pdb_single,
        title=None,
        save=False,
    )
    assert result.get_title() == pdb_single


def test_plot_custom_title_multiple(temp_dir, pdb_multiple):
    result = utils.plot(
        pdb_filepath=pdb_multiple,
        title="My batch title",
        save=False,
    )
    assert result.get_title() == "My batch title"


def test_plot_default_title_multiple(temp_dir, pdb_multiple):
    result = utils.plot(
        pdb_filepath=pdb_multiple,
        title=None,
        save=False,
    )
    assert result.get_title() == f"Batch ({len(pdb_multiple)} files)"
