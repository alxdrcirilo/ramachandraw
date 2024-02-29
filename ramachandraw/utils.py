from functools import wraps
from importlib import resources
from itertools import cycle
from typing import Union

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from Bio.PDB import PDBList
from matplotlib.axes import Axes
from matplotlib.lines import Line2D

from ramachandraw.parser import get_phi_psi


class NoPdbIdProvided(Exception):
    pass


def handle_multiple_ids(func):
    """Decorator allowing more than one PDB id to be processed.

    Whenever a Sequence of type list | tuple is provided, the wrapper will iterate over them.
    Otherwise, when only one PDB is provided, the wrapped function will only be called once.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        pdbs = None
        if args:
            pdbs = args[0] if args[0] else None
        elif kwargs and not pdbs:
            pdbs = kwargs.get("pdb_id", None)

        verbose = kwargs.get("verbose", False)

        if not pdbs:
            raise NoPdbIdProvided(
                "Please provide one or more PDB ids using the `pdb_id` argument."
            )

        if isinstance(pdbs, str):
            return func(pdb_id=pdbs, verbose=verbose)
        elif isinstance(pdbs, (list, tuple)):
            return [func(pdb_id=pdb, verbose=verbose) for pdb in pdbs]

    return wrapper


@handle_multiple_ids
def fetch_pdb(
    pdb_id: Union[str, list, tuple], verbose: bool = False
) -> Union[str, list[str]]:
    """Fetch PDB file given a PDB id (in .ent format).

    :param Union[str, list, tuple] pdb_id: pdb id(s) (e.g. "1mbn")
    :param bool verbose: logs warnings if set to True, defaults to False
    :return Union[str, list[str]]: pdb filepath(s) (e.g. ".pbd/pdb1mbn.ent")
    """
    pdbl = PDBList(verbose=verbose)
    return pdbl.retrieve_pdb_file(pdb_code=pdb_id, pdir=".pdb", file_format="pdb")


def plot(
    pdb_filepath: Union[str, list, tuple],
    cmap: str = "viridis",
    alpha: float = 0.75,
    dpi: int = 100,
    save: bool = True,
    show: bool = False,
    filename: str = "plot.png",
) -> Axes:
    """Draw the Ramachandrawn plot.

    This function is highly customizable, allowing different (optional) parameters.

    :param Union[str, list, tuple] pdb_filepath: pdb filepath(s) (e.g. ".pbd/pdb1mbn.ent")
    :param str cmap: colormap, defaults to "viridis"
    :param float alpha: transparency (i.e. alpha value), defaults to 0.75
    :param int dpi: resolution (i.e. "dots per inch"), defaults to 100
    :param bool save: saves the plot to a file if True, defaults to True
    :param bool show: shows the plot interactively if True, defaults to False
    :param str out: filename for plot output, defaults to "plot.png"
    :return Axes: Axes object to enable further customization if required
    """

    def plot_density_map() -> None:
        """Plot the density map of allowed/favoured regions.

        The density map was obtained using the Top8000 dataset (top 8k high-resolution PDB structures).
        """
        density_file = resources.files(package="ramachandraw") / "kde.dat"
        with density_file.open("r") as kde_data:
            z = np.fromfile(kde_data)
        z = np.reshape(z, (100, 100))

        # Normalize
        data = np.log10(np.rot90(z))
        ax.imshow(
            data, cmap=plt.get_cmap(cmap), extent=(-180, 180, -180, 180), alpha=alpha
        )

        # Add contour lines
        data = np.rot90(np.fliplr(z))
        ax.contour(
            data,
            colors="k",
            linewidths=0.5,
            levels=[10**i for i in range(-7, 0)],
            antialiased=True,
            extent=[-180, 180, -180, 180],
            alpha=0.5,
        )

    def draw(data: dict[str, list], color: str = "k") -> None:
        """Plot the aminoacid residues given their Φ-Ψ torsion angles.

        :param dict[str, list] data: angles data (e.g. {"A:ARG156": [-29.8, -32.4]})
        :param str color: marker color, defaults to "k" (black)
        """
        x = [torsion[0] for torsion in data.values()]
        y = [torsion[1] for torsion in data.values()]
        ax.scatter(x=x, y=y, marker="o", s=1, c=color)

    fig = plt.figure(figsize=(5.5, 5), dpi=dpi)
    ax = plt.subplot(111)
    plot_density_map()

    ticks = list(range(-180, 181, 45))
    ax.set(
        aspect="equal",
        xlabel="\u03C6",
        ylabel="\u03C8",
        xlim=(-180, 180),
        ylim=(-180, 180),
        xticks=ticks,
        yticks=ticks,
        title=pdb_filepath[0],
    )
    plt.axhline(y=0, color="k", lw=0.5)
    plt.axvline(x=0, color="k", lw=0.5)
    plt.grid(visible=None, which="major", axis="both", color="k", alpha=0.2)

    angles = get_phi_psi(pdb_filepath=pdb_filepath)

    # Single PDB
    if isinstance(angles, dict):
        draw(data=angles)

    # Multiple PDBs
    elif isinstance(angles, list):
        ax.set_title(f"Batch ({len(pdb_filepath)} files)")
        colors = cycle(mcolors.TABLEAU_COLORS.values())
        custom_legend = []
        for pdb, data in zip(pdb_filepath, angles):
            color = next(colors)
            draw(data=data, color=color)  # type: ignore
            point = Line2D(
                [0],
                [0],
                label=pdb,
                marker="o",
                markerfacecolor=color,
                markeredgewidth=0,
                markersize=5,
                linestyle="",
            )
            custom_legend.append(point)
        handles, _ = plt.gca().get_legend_handles_labels()
        handles.extend(custom_legend)
        ax.legend(handles=handles, loc=1)

    if save:
        fig.savefig(filename)
    if show:
        fig.show()

    return ax
