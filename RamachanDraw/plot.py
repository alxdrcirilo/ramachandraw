from os import sep as os_separator
from os.path import realpath, exists
from typing import Union

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from pkg_resources import resource_stream

from .phi_psi import get_ignored_res


def get_pdb_name(path: Union[str, list, tuple], remove_extension: bool = True, upper_case: bool = False) -> tuple:
    """
    Extracts the PDB file name(s)
    :param path: path to extract name from
    :param remove_extension: with(out) file extension
    :param upper_case: convert output names to upper case
    :return: Filenames as iterable
    """
    if isinstance(path, str):
        path = [path]

    path_out = []
    for p in path:
        path_split = p.split(os_separator)
        pdb_name = path_split[-1]
        if remove_extension:
            pdb_name = '.'.join(pdb_name.split(".")[:-1])
        path_out.append(pdb_name.upper() if upper_case else pdb_name)
    return tuple(path_out)


def plot(pdb_file: Union[str, list, tuple], cmap: str = 'viridis', alpha: float = 0.75, dpi: int = 100,
         save: bool = True, show: bool = False, out: str = 'plot.png',
         ignore_pdb_warnings: bool = False) -> (plt.Axes, dict):
    """
    Plots Ramachandran plots of given PDB files.
    :param pdb_file: Input PDB file path as string or list of PDB file paths
    :param cmap: Plot CMAP
    :param alpha: Plot alpha
    :param dpi: Plot DPI
    :param save: Save plot to <out> path
    :param show: Show plot
    :param out: Plot output path
    :param ignore_pdb_warnings: silence call for PDB file parsing
    :return: [0] matplotlib object
             [1] dictionary with pdb_file name(s) as key and tuple of (phi_psi_data, ignored_res, x, y) as value
    """
    batch_mode = isinstance(pdb_file, list)
    save = (isinstance(out, str) and len(out) > 0) or save

    size = (8.5, 5) if batch_mode else (5.5, 5)
    plt.figure(figsize=size, dpi=dpi)
    ax = plt.subplot(111)
    ax.set_title("Batch" if batch_mode else ''.join(get_pdb_name(pdb_file)))  # Batch or PDB file name

    # Import 'density_estimate.dat' data file
    with resource_stream('RamachanDraw', 'data/density_estimate.dat') as plot_background_stream:
        z = np.fromfile(plot_background_stream)
    z = np.reshape(z, (100, 100))

    ax.set_aspect('equal')
    ax.set_xlabel('\u03C6')
    ax.set_ylabel('\u03C8')
    ax.set_xlim(-180, 180)
    ax.set_ylim(-180, 180)
    ax.set_xticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
    ax.set_yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
    plt.axhline(y=0, color='k', lw=0.5)
    plt.axvline(x=0, color='k', lw=0.5)
    plt.grid(visible=None, which='major', axis='both', color='k', alpha=0.2)

    # Normalize data
    data = np.log(np.rot90(z))
    ax.imshow(data, cmap=plt.get_cmap(cmap), extent=(-180, 180, -180, 180), alpha=alpha)

    # Fit contour lines correctly
    data = np.rot90(np.fliplr(z))
    ax.contour(data, colors='k', linewidths=0.5,
               levels=[10 ** i for i in range(-7, 0)],
               antialiased=True, extent=[-180, 180, -180, 180], alpha=0.65)

    def start(fp, color=None):
        fp = realpath(fp)
        assert exists(fp), \
            'Unable to fetch file: {}. PDB entry probably does not exist.'.format(fp)
        phi_psi_data, ignored_res, x, y = get_ignored_res(pdb_file_path=fp, ignore_pdb_warnings=ignore_pdb_warnings)
        ax.scatter(x, y, marker='.', s=3, c="".join([color if color else 'k']), label=''.join(get_pdb_name(fp)))
        return phi_psi_data, ignored_res, x, y

    file_output_map = {key: None for key in pdb_file}
    if batch_mode:
        for idx, file_path in enumerate(pdb_file):
            file_output_map[file_path] = start(fp=file_path, color=list(mcolors.BASE_COLORS.keys())[idx])
        ax.legend(bbox_to_anchor=(1.04, 1), loc='upper left')
    else:
        file_output_map[pdb_file] = start(fp=pdb_file)

    if save:
        plt.savefig(out)
    if show:
        plt.show()

    # return params
    return ax, file_output_map
