import setuptools

setuptools.setup(
    name="tutorial_rdock_implementation",
    version="0.1.0",
    url="https://github.com/drugdata/custom_celpp_contestant",

    author="Jeff Wagner",
    author_email="j5wagner@ucsd.edu",

    description="An implementation of rDock for CELPP using Chimera DockPrep for protein prep and RDKit for 3D ligand conformer generation.",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=["d3r"],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
     scripts = ['tutorial_rdock_implementation/tutorial_rdock_implementation_dock.py',
                'tutorial_rdock_implementation/tutorial_rdock_implementation_ligand_prep.py', 
                'tutorial_rdock_implementation/tutorial_rdock_implementation_protein_prep.py']
)
