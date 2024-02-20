from RamachanDraw import fetch, phi_psi, plot

# Local file
file = './RamachanDraw/data/4hhb.pdb'
# Plot from local file and show
plot(pdb_file=file, show=True, ignore_pdb_warnings=True)
# Plot from downloaded file and save with alpha argument set to 0.5
plot(pdb_file=fetch('2bxc'), show=False, save=True, alpha=0.5, ignore_pdb_warnings=True)
# Plot from PDB identifier with alpha set to 1
plot(pdb_file='2bxc', show=True, save=False, alpha=1, ignore_pdb_warnings=True)
# Get phi and psi angles
print(phi_psi(pdb_file=file, ignore_pdb_warnings=False))  # will result in many warnings

# Batch of PDB ids
batch = ['1mbn', '4hhb', '1aoi', '2jip']
# Get phi and psi angles for each pdb in the batch
phi_psi(pdb_file=fetch(batch), return_ignored=True, ignore_pdb_warnings=True, print_ignored=True)
# Plot from downloaded files and show
plot(pdb_file=fetch(batch), show=True, save=False)
