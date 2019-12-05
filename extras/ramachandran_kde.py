"""
Extracts torsion angles (phi, psi) from top 8000 PDB structures and generates a PDF using a Gaussian kernel
"""

from Bio.PDB import PDBParser, Polypeptide, PPBuilder
from math import pi
import os
import numpy as np
from scipy.stats import gaussian_kde

phi_psi_dict = {}
residue = 0
for root, dirs, files in os.walk('top8000_chains_70/top8000_chains_70'):
	for i, filename in enumerate(files):
		print(str(round(i/len(files)*100, 1)) + '%...\t' + filename)
		for model in PDBParser().get_structure(id=None, file='top8000_chains_70/top8000_chains_70//{}'.format(filename)):
			for chain in model:
				peptides = PPBuilder().build_peptides(chain)
				for peptide in peptides:
					phi_psi = peptide.get_phi_psi_list()
					for index, aminoacid in enumerate(peptide):
						residue += 1
						phi_psi_dict[residue] = phi_psi[index]

x = []
y = []
residues = []
for key, value in phi_psi_dict.items():
	# print(key, value)
	if value[0] == None or value[1] == None:
		pass
	else:
		residues.append(key)
		x.append(value[0] * 180 / pi)
		y.append(value[1] * 180 / pi)
names = np.array(residues)

print('Calculating point density...')
x = np.asarray(x)
y = np.asarray(y)
xmin = x.min()
xmax = x.max()
ymin = y.min()
ymax = y.max()
print('Creating grid...')
X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
print(type(X))
print('Writing to file...')
X.tofile('X.dat', sep='')
Y.tofile('Y.dat', sep='')
print('Done!')

# print('Vstack...')
# positions = np.vstack([X.ravel(), Y.ravel()])
# print('Values...')
# values = np.vstack([x, y])
# print('Gaussian kernel...')
# kernel = gaussian_kde(values)
# print('Reshaping array...')
# Z = np.reshape(kernel(positions).T, X.shape)
# print('Writing to file...')
# Z.tofile('density_estim.dat', sep='')
# print('Done!')