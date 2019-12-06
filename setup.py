import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RamachanDraw",
    version="0.1.16",
    author="Alexandre D. Cirilo",
    author_email="a.dias.cirilo@umail.leidenuniv.nl",
    description="Ramachandran plotting tool",
    long_description=long_description,
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
