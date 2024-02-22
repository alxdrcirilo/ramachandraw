# Ramachandran plotting tool

![PyPI](https://img.shields.io/pypi/v/RamachanDraw)
![PyPI - Downloads](https://img.shields.io/pypi/dm/RamachanDraw)
![PyPI - License](https://img.shields.io/pypi/l/RamachanDraw)

Draws a Ramachandran plot based on the input PDB file (e.g. 1MBN.pdb). Makes use of a Gaussian KDE (kernel density
estimation) to plot the density of favoured torsion angles (&phi; and &psi;).

![](https://raw.githubusercontent.com/alxdrcirilo/RamachanDraw/master/extras/plot.png)

## Installation

RamachanDraw is hosted on [PyPi](https://pypi.org/project/RamachanDraw/).

```
pip install RamachanDraw
```

## Usage

RamachanDraw includes useful functions to effortlessly draw a Ramachandran plot.

### Fetch the PDB file from the online repository

To draw a Ramachandran plot, we need a PDB file. You can use a local PDB file by specifying the path. Alternatively,
RamachanDraw conveniently includes a function to automatically fetch and locally store the PDB file for the given PDB
id.

#### Arguments

```
fetch(pdb_file)
```

- ```pdb_file (str|list)```: PDB id(s) corresponding to the PDB entry to be downloaded.
- ```Returns```: path to PDB file.

### Extract &phi; and &psi; angles

RamachanDraw extracts the &phi; and &psi; angles from the PDB file by taking advantage of
the [Biopython](https://biopython.org/) module. Additionally, aminoacid residues that were not drawn on the plot can be
extract using the ```return_ignored``` argument.

#### Arguments

```
phi_psi(pdb_file, return_ignored, print_ignored, ignore_pdb_warnings)
```

- ```pdb_file```: one of the following:
    - ```pdb_file (str)```: PDB id corresponding to the PDB entry to be downloaded.
    - ```pdb_file (str)```: PDB file path to use.
    - ```pdb_file (list)```: List of PDB file paths to use.
- ```return_ignored (bool)```: Returns a list of tuple with the format (chain:residue, (phi, psi))
- ```print_ignored (bool)```: Print a table of ignored residues to console
- ```ignore_pdb_warnings (bool)```: Turn off all PDB structure parser warnings
- ```Returns```: Dictionary with keys as amino acid residues and values as (phi, psi) angle values.

### Ramachandran plot

Makes use of the [matplotlib](https://matplotlib.org/) module to draw a highly customizable Ramachandran plot.

#### Arguments

```
plot(pdb_file, cmap='viridis', alpha=0.75, dpi=100, save=True, show=False, out='plot.png', ignore_pdb_warnings=False)
```

- ```pdb_file (str|list)```: PDB id(s) corresponding to the PDB entry to be downloaded.
- ```cmap (str)```: colormap to be used (from matplotlib) for the density of the favoured ("allowed") regions; default
  is <em>viridis</em>.
- ```alpha (float)```: sets the opacity of the colormap (value between 0-1); default is 0.75.
- ```dpi (int)```: resolution (<em>dots per inch</em>); default is 100.
- ```save (bool)```:
    - ```True```: saves the plot locally; default is True.
- ```show (bool)```:
    - ```True```: shows the plot using the Qt5Agg backend; default is False.
- ```out (str)```: filename to be used in case the plot is saved (i.e. ```save=True```); default is <em>plot.png</em>.
- ```ignore_pdb_warnings (bool)```: Turn off all PDB structure parser warnings
- ```Returns```: Ramachandran plot (can be saved locally) and dictionary of all angles per PDB file

## Example

Herein you will find an example from the PDB id corresponding to the myoglobin entry
- [1MBN](https://www.ebi.ac.uk/pdbe/entry/pdb/1mbn/index) - in the Protein Data Bank.

```
from RamachanDraw import fetch, phi_psi, plot

# PDB id to be downloaded
PDB_id = '1MBN'

# Drawing the Ramachandran plot
plot(fetch(PDB_id))

# Generating a dictionary to store the phi and psi angles
# And returning the ignored aminoacid residues
phi_psi_dict, ignored_res = phi_psi(fetch(PDB_id), return_ignored=True)
```

## Contributing

Feedback and constructive criticism is welcome. If necessary, open an issue in the *issues* tab.

## License

[MIT](https://choosealicense.com/licenses/mit/)
