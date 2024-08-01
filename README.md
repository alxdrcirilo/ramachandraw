# Ramachandran plotting tool

[![ramachandraw](https://github.com/alxdrcirilo/ramachandraw/actions/workflows/coveralls.yaml/badge.svg)](https://github.com/alxdrcirilo/ramachandraw/actions/workflows/coveralls.yaml)
[![coverage](https://coveralls.io/repos/github/alxdrcirilo/ramachandraw/badge.svg?branch=master)](https://coveralls.io/github/alxdrcirilo/ramachandraw?branch=master)
[![python version](https://img.shields.io/badge/python-3.9|3.10|3.11|3.12-blue)](https://www.python.org/)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![license: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![PyPI](https://img.shields.io/pypi/v/ramachandraw)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ramachandraw)

Draws a [Ramachandran plot](https://en.wikipedia.org/wiki/Ramachandran_plot) based on the input PDB file (e.g. `1mbn.pdb`). Makes use of a Gaussian KDE (kernel density
estimation) to plot the density of favoured torsion angles (&phi; and &psi;).

Single mode                |  Batch mode
:-------------------------:|:-------------------------:
![](https://raw.githubusercontent.com/alxdrcirilo/ramachandraw/master/images/plot_single.png) | ![](https://raw.githubusercontent.com/alxdrcirilo/ramachandraw/master/images/plot_batch.png)

## Installation

RamachanDraw is hosted on [PyPi](https://pypi.org/project/RamachanDraw/).

```bash
pip install ramachandraw
```

## Usage

RamachanDraw includes useful functions to effortlessly draw a Ramachandran plot.

### Fetch the PDB file

To draw a Ramachandran plot, we need a PDB file. RamachanDraw conveniently includes a function to automatically fetch and locally store the PDB file for the given PDB id.

#### Example

```python
from ramachandraw.utils import fetch_pdb

fetch_pdb(pdb_id, verbose)
```

- `pdb_id (str|list|tuple)`: PDB id(s) corresponding to the PDB file(s) to be downloaded
- `verbose (bool)` (*optional*): set the verbosity, defaults to `False`
- **Returns**: path(s) to PDB file(s)

### Extract &phi; and &psi; torsion angles

RamachanDraw extracts the &phi; and &psi; torsion angles from the PDB file by taking advantage of the [Biopython](https://biopython.org/) module. Additionally, aminoacid residues that were not drawn on the plot can be extract using the `return_ignored` argument.

#### Example

```python
from ramachandraw.parser import get_phi_psi

phi_psi(pdb_filepath, prune, hide_warnings)
```

- `pdb_id (str|list|tuple)`: PDB filepath(s)
- `prune (bool)` (*optional*): prunes aminoacids with missing torsion angle(s), defaults to `True`
- `hide_warnings (bool)` (*optional*): sets the verbosity of the PDB structure parser, defaults to `True`
- **Returns**: Dictionary with keys as aminoacid residues and values as (&phi;, &psi;) angles.

### Ramachandran plot

Makes use of the [matplotlib](https://matplotlib.org/) module to draw a highly customizable Ramachandran plot.

#### Example

```python
from ramachandraw.utils import plot

plot(pdb_filepath, cmap="viridis", alpha=0.75, dpi=100, save=True, show=False, filename="plot.png")
```

- `pdb_file (str|list|tuple)`: PDB id(s) corresponding to the PDB entry to be downloaded
- `cmap (str)` (*optional*): colormap to be used (from `matplotlib`) for the density of the favoured ("allowed") regions; default
  is *viridis*.
- `alpha (float)` (*optional*): sets the opacity of the colormap (value between 0-1); default is 0.75.
- `dpi (int)` (*optional*): resolution (in *dots per inch*); default is `100`.
- `save (bool)` (*optional*):
  - `True`: saves the plot locally; default is True.
- `show (bool)` (*optional*):
  - `True`: shows the plot using the Qt5Agg backend; default is False.
- `filename (str)` (*optional*): filename to be used in case the plot is saved (i.e. `save=True`); default is `plot.png`.
- **Returns**: Ramachandran plot (`matplotlib.axes.Axes` object) that can be further customized if needed

## Example

Herein you will find an example from the PDB id corresponding to the myoglobin entry: [1MBN](https://www.ebi.ac.uk/pdbe/entry/pdb/1mbn/index) - in the Protein Data Bank.

### Single PDB

```python
from ramachandraw.parser import get_phi_psi
from ramachandraw.utils import fetch_pdb, plot


# PDB id
pdb_id = "1mbn"

# Draw the Ramachandran plot
plot(fetch_pdb(pdb_id))

# Generate a dictionary to store the (phi, psi) torsion angles
torsion_angles = get_phi_psi(fetch_pdb(pdb_id))
```

### Batch of PDBs

```python
from ramachandraw.parser import get_phi_psi
from ramachandraw.utils import fetch_pdb, plot


# PDB id
pdb_ids = ["1mbn", "4hhb"]

# Draw the Ramachandran plot
plot(fetch_pdb(pdb_ids))

# Generate a list of dictionaries to store the (phi, psi) torsion angles
torsion_angles = get_phi_psi(fetch_pdb(pdb_ids))
```

## Contributing

Feedback and constructive criticism is welcome. If necessary, open an issue in the [issues](https://github.com/alxdrcirilo/ramachandraw/issues) tab.

## License

[MIT](https://choosealicense.com/licenses/mit/)
