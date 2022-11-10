import os
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from Bio.PDB import PDBParser, PPBuilder
from pkg_resources import resource_stream
from math import pi


def plot(pdb_file, cmap='viridis', alpha=0.75, dpi=100, save=True, show=False, out='plot.png'):
    batch_mode = [True if type(pdb_file) is list else False][0]

    def get_ignored_res(file: str):
        x, y, ignored, output = [], [], [], {}
        for model in PDBParser().get_structure(id=None, file=file):
            for chain in model:
                peptides = PPBuilder().build_peptides(chain)
                for peptide in peptides:
                    for aa, angles in zip(peptide, peptide.get_phi_psi_list()):
                        residue = aa.resname + str(aa.id[1])
                        output[residue] = angles

        for key, value in output.items():
            # Only get residues with both phi and psi angles
            if value[0] and value[1]:
                x.append(value[0] * 180 / pi)
                y.append(value[1] * 180 / pi)
            else:
                ignored.append((key, value))

        return output, ignored, x, y

    size = [(8.5, 5) if batch_mode else (5.5, 5)][0]
    plt.figure(figsize=size, dpi=dpi)
    ax = plt.subplot(111)
    ax.set_title("".join(["Batch" if batch_mode else pdb_file]))

    # Import 'density_estimate.dat' data file
    Z = np.fromfile(resource_stream('RamachanDraw', 'data/density_estimate.dat'))
    Z = np.reshape(Z, (100, 100))

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
    data = np.log(np.rot90(Z))
    ax.imshow(data, cmap=plt.get_cmap(cmap), extent=[-180, 180, -180, 180], alpha=alpha)

    # Fit contour lines correctly
    data = np.rot90(np.fliplr(Z))
    ax.contour(data, colors='k', linewidths=0.5,
               levels=[10 ** i for i in range(-7, 0)],
               antialiased=True, extent=[-180, 180, -180, 180], alpha=0.65)

    def start(fp, color=None):
        assert os.path.exists(fp), \
            'Unable to fetch file: {}. PDB entry probably does not exist.'.format(pdb_file)
        phi_psi_data, ignored_res, x, y = get_ignored_res(file=fp)
        ax.scatter(x, y, marker='.', s=3, c="".join([color if color else 'k']), label=fp)
        return phi_psi_data, ignored_res, x, y

    if batch_mode:
        file_output_map = {key: None for key in pdb_file}
        for _, file in enumerate(pdb_file):
            file_output_map[file] = start(fp=file, color=list(mcolors.BASE_COLORS.keys())[_])
        ax.legend(bbox_to_anchor=(1.04, 1), loc='upper left')
    else:
        output = start(fp=pdb_file)

    if save:
        plt.savefig(out)
    if show:
        plt.show()
    
    #return params
    if batch_mode:
        return ax, file_output_map
    else:
        return ax, output
