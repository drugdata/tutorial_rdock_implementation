tutorial_rdock_implementation
=============================

.. image:: https://img.shields.io/pypi/v/tutorial_rdock_implementation.svg
    :target: https://pypi.python.org/pypi/tutorial_rdock_implementation
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/cookiecutter/cookiecutter-pycustomdock.png
   :target: https://travis-ci.org/cookiecutter/cookiecutter-pycustomdock
   :alt: Latest Travis CI build status

An implementation of rDock for CELPP using Chimera DockPrep for protein prep and RDKit for 3D ligand conformer generation.

Creation of this package was documented in the CELPPade video tutorial: https://www.youtube.com/watch?v=btf77rNU1PY

More information on CELPPade is available at the project homepage: https://github.com/drugdata/D3R/wiki/CELPPade 

Usage
-----

.. code-block:: bash
   # This example assumes you have cloned and built the image
   # as described in building container below and that
   # you are in the tutorial_rdock_implementation directory
   # and you have exited the vagrant VM
   mkdir tmp
   cd tmp
   # get challenge data
   challdir="1-get_challenge_data/"
   mkdir -p $challdir
   singularity run ../build/tutorialrdock.img getchallengedata.py --unpackdir $challdir -f ~/ftp.config

   # protein prep
   protdir="2-protein_prep/"
   mkdir $protdir
   singularity run ../build/tutorialrdock.img tutorial_rdock_implementation_protein_prep.py --challengedata $challdir --prepdir $protdir
   
   # ligand prep
   ligdir="3-ligand_prep/"
   mkdir $ligdir
   singularity run ../build/tutorialrdock.img tutorial_rdock_implementation_ligand_prep.py --challengedata $challdir --prepdir $ligdir

   #dock
   dockdir="4-docking/"
   mkdir $dockdir
   singularity run ../build/tutorialrdock.img tutorial_rdock_implementation_dock.py --protsciprepdir $protdir --ligsciprepdir $ligdir --outdir $dockdir

   #upload results
   packdir="5-pack_docking_results"
   mkdir $packdir
   singularity run ../build/tutorialrdock.img packdockingresults.py --dockdir $dockdir --packdir $packdir --challengedata $challdir -f ~/ftp.config

Building the container
----------------------

Build Requirements
^^^^^^^^^^^^^^^^^^

* Vagrant https://www.vagrantup.com/

* Virtual Box https://www.virtualbox.org/

* Binary of 64-bit Linux distribution of Chimera (tested with version `1.13 <https://www.cgl.ucsf.edu/chimera/cgi-bin/secure/chimera-get.py?file=linux_x86_64/chimera-1.13-linux_x86_64.bin>`_) https://www.cgl.ucsf.edu/chimera

The following commands spin up a `Virtual Box <https://www.virtualbox.org>`_ virtual machine via `Vagrant <https://www.vagrantup.com>`_ with `Singularity <https://www.sylabs.io>`_ installed. A `Makefile <https://www.gnu.org/software/make/manual/make.html>`_ is then used to create the `Singularity <https://www.sylabs.io>`_ Container runnable on any machine that can run `Singularity <https://www.sylabs.io>`_.


.. code-block:: bash

   git clone https://github.com/drugdata/tutorial_rdock_implementation.git
   cd tutorial_rdock_implementation
   #
   # Be sure to download 64-bit Linux version of Chimera and put binary
   # in source tree directory
   #
   vagrant up
   vagrant ssh
   cd /vagrant
   make singularity

Compatibility
-------------

License
-------

See LICENSE.txt_

Authors
-------

`tutorial_rdock_implementation` was written by `Jeff Wagner <j5wagner@ucsd.edu>`_.

.. _LICENSE.txt: https://github.com/drugdata/tutorial_rdock_implementation/blob/master/LICENSE.txt
