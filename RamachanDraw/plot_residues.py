from Bio.PDB import PDBParser, PPBuilder
from math import pi
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import os

matplotlib.use('Qt5Agg')


def plot(pdb_file, cmap='viridis', alpha=0.75, dpi=100, save=True, show=False, out='plot.png'):
    # Initialize variables
    x, y = [], []
    # Initialize dictionary which holds the values of the torsion angles
    #   - Keys: residues
    #   - Values: torsion angles
    phi_psi_dict = {}
    figure, axes = plt.subplots(figsize=(5.5, 5), dpi=dpi)
    axes.set_title(pdb_file)

    assert os.path.exists(pdb_file), 'Unable to fetch file: {}. PDB entry probably does not exist.'.format(pdb_file)

    for model in PDBParser().get_structure(id=None, file=pdb_file):
        # Create dictionary to store parsed values
        for chain in model:
            peptides = PPBuilder().build_peptides(chain)
            for peptide in peptides:
                phi_psi = peptide.get_phi_psi_list()
                for aminoacid, angles in zip(peptide, phi_psi):
                    residue = aminoacid.resname + str(aminoacid.id[1])
                    phi_psi_dict[residue] = angles

    ignored_res = []
    for key, value in phi_psi_dict.items():
        # Only get residues with both phi and psi angles
        if value[0] and value[1]:
            x.append(value[0] * 180 / pi)
            y.append(value[1] * 180 / pi)
        else:
            ignored_res.append((key, value))

    # Calculate the point density
    X, Y = np.mgrid[min(x):max(x):100j, min(y):max(y):100j]

    # Import 'density_estimate.dat' data file
    from pkg_resources import resource_stream
    Z = np.fromfile(resource_stream('RamachanDraw', 'data/density_estimate.dat'))
    # Z = np.fromfile('data/density_estimate.dat') # Debug only
    Z = np.reshape(Z, X.shape)

    axes.set_aspect('equal')
    axes.set_xlabel('\u03C6')
    axes.set_ylabel('\u03C8')
    axes.set_xlim(-180, 180)
    axes.set_ylim(-180, 180)
    axes.set_xticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
    axes.set_yticks([-180, -135, -90, -45, 0, 45, 90, 135, 180], minor=False)
    plt.axhline(y=0, color='k', lw=0.5)
    plt.axvline(x=0, color='k', lw=0.5)
    plt.grid(b=None, which='major', axis='both', color='k', alpha=0.2)
    # Normalize data
    data = np.log(np.rot90(Z))
    axes.imshow(data, cmap=plt.get_cmap(cmap), extent=[-180, 180, -180, 180], alpha=alpha)
    # Fit contour lines correctly
    data = np.rot90(np.fliplr(Z))
    axes.contour(data, colors='k', linewidths=0.5,
                 levels=[10**i for i in range(-7, 0)],
                 antialiased=True, extent=[-180, 180, -180, 180], alpha=0.65)
    sc = plt.scatter(x, y, marker='.', s=3, c='k')

    if save:
        plt.savefig(out)
    if show:
        plt.show()