"""
Extracts torsion angles (phi, psi) from top 8000 PDB structures and generates a PDF using a Gaussian kernel
"""

from multiprocessing import Pool, cpu_count
from pathlib import Path

import numpy as np
from scipy.stats import gaussian_kde

from ramachandraw import get_phi_psi


# task executed in a worker process
def run_task(filepath: Path):
    data = get_phi_psi(pdb_filepath=str(filepath))
    return [*data.values()]


def pool_hander():
    cpus = cpu_count()
    print(f"Running with {cpus} cores")
    with Pool(cpus) as p:
        res = p.map(run_task, files)
    return res


if __name__ == "__main__":
    files = [filepath for filepath in Path("dataset").iterdir() if filepath.is_file()]
    res = pool_hander()

    x, y = [], []
    for pdb in res:
        try:
            for [phi, psi] in pdb:
                x.append(phi)
                y.append(psi)
        except:
            print(f"Could not process...")
            pass

    print("Calculating point density...")
    x = np.asarray(x)
    y = np.asarray(y)
    xmin = x.min()
    xmax = x.max()
    ymin = y.min()
    ymax = y.max()
    print("Creating grid...")
    X, Y = np.mgrid[xmin:xmax:100j, ymin:ymax:100j]
    print(type(X))
    print("Writing to file...")
    X.tofile("X.dat", sep="")
    Y.tofile("Y.dat", sep="")
    print("Done!")

    print("Vstack...")
    positions = np.vstack([X.ravel(), Y.ravel()])
    print("Values...")
    values = np.vstack([x, y])
    print("Gaussian kernel...")
    kernel = gaussian_kde(dataset=values)
    print("Reshaping array...")
    Z = np.reshape(kernel(positions).T, X.shape)
    print("Writing to file...")
    Z.tofile("kde.dat", sep="")
    print("Done!")
