from RamachanDraw import fetch, phi_psi, plot

file = 'data/4hhb.pdb'
plot(pdb_file=file, show=True)

plot(pdb_file=fetch('2bxc'), show=False, save=True, alpha=0.5)

angles = phi_psi(pdb_file=file)