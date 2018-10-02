#!/usr/bin/env python

__author__ = 'j5wagner@ucsd.edu'


import commands
from d3r.celppade.custom_protein_prep import ProteinPrep


class chimera_dockprep(ProteinPrep):
    """Abstract class defining methods for a custom docking solution
    for CELPP
    """

    ProteinPrep.OUTPUT_PROTEIN_SUFFIX = '.mol2'

        
    def receptor_scientific_prep(self, 
                                 protein_file, 
                                 prepared_protein_file, 
                                 targ_info_dict={}):
        """
        Protein 'scientific preparation' is the process of generating
        a dockable representation of the candidate protein from a
        single-chain PDB file.
        :param protein_file: PDB file containing candidate protein.  
        :param prepared_protein_file: The result of preparation should have this file name.  
        :param targ_info_dict: A dictionary of information about this target and the candidates chosen for docking.  
        :returns: True if preparation was successful. False otherwise.
        """

        #####################################################################
        ### $ python  clean_receptor.py  receptor.pdb  clean_receptor.pdb ###
        #####################################################################

        # Implements the logic that was formerly in clean_receptor.py
        orig_pdb = open(protein_file).readlines()
        with open('clean_receptor.pdb','wb') as of:
            for line in orig_pdb:
                if len(line) > 4:
                    if line[:4] == 'ATOM':
                        of.write(line)
    

        #####################################################################
        ### $ chimera  --nogui  --script  "chimeraPrep.py  clean_receptor.pdb  prepared_receptor.mol2"
        #####################################################################

        # Write the chimera-interpreted code to a script file
        chimera_prep_text = '''import chimera
import sys
opened = chimera.openModels.open(sys.argv[1])
mol = opened[0]

import DockPrep

DockPrep.prep([mol])
from WriteMol2 import writeMol2
with open(sys.argv[2],'wb') as of:
    writeMol2([mol], of)
'''
        with open('chimera_prep.py','wb') as of:
            of.write(chimera_prep_text)

        # Run chimera with the script as an input
        prep_cmd = 'chimera  --nogui  --script  "chimera_prep.py  clean_receptor.pdb ' + prepared_protein_file + ' " 1> prep.stdout 2> prep.stderr'
        commands.getoutput(prep_cmd)

        return True
    
                        

    
if ("__main__") == (__name__):
    import logging
    import os
    import shutil
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-p", "--pdbdb", metavar = "PATH", help = "PDB DATABANK which we will dock into")
    parser.add_argument("-c", "--challengedata", metavar="PATH", help = "PATH to the unpacked challenge data package")
    parser.add_argument("-o", "--prepdir", metavar = "PATH", help = "PATH to the output directory")
    logger = logging.getLogger()
    logging.basicConfig( format  = '%(asctime)s: %(message)s', datefmt = '%m/%d/%y %I:%M:%S', filename = 'final.log', filemode = 'w', level = logging.INFO )
    opt = parser.parse_args()
    pdb_location = opt.pdbdb
    challenge_data_path = opt.challengedata
    prep_result_path = opt.prepdir

    #running under this dir
    abs_running_dir = os.getcwd()
    log_file_path = os.path.join(abs_running_dir, 'final.log')
    log_file_dest = os.path.join(os.path.abspath(prep_result_path), 'final.log')

    prot_prepper = chimera_dockprep()
    prot_prepper.run_scientific_protein_prep(challenge_data_path, pdb_location, prep_result_path)

    #move the final log file to the result dir
    shutil.move(log_file_path, log_file_dest)
