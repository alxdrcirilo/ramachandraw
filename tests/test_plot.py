from matplotlib.axes import Axes

from ramachandraw import utils


def test_plot_return_single(temp_dir, pdb_single):
    result = utils.plot(pdb_filepath=pdb_single)
    assert isinstance(result, Axes)


def test_plot_return_multiple(temp_dir, pdb_multiple):
    result = utils.plot(pdb_filepath=pdb_multiple)
    assert isinstance(result, Axes)
