import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RamachanDraw",
    version="0.1.15",
    author="Alexandre D. Cirilo",
    author_email="a.dias.cirilo@umail.leidenuniv.nl",
    description="Ramachandran plotting tool",
    long_description="Draws a Ramachandran plot based on the input PDB file (e.g. 1MBN.pdb). Makes use of a Gaussian "
                     "KDE (kernel density estimation) to plot the density of favoured torsion angles (&phi; and &psi;).",
    long_description_content_type="text/markdown",
    url="https://github.com/alxdrcirilo/RamachanDraw",
    packages=['RamachanDraw'],
    package_data={'RamachanDraw': ['data/density_estimate.dat']},
    # install_requires=[
    #     "biopython==1.75",
    #     "matplotlib==3.1.2",
    #     "PyQt5==5.13.2",
    # ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
