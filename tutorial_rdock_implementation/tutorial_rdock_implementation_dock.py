#!/usr/bin/env python

__author__ = 'j5wagner@ucsd.edu'


from d3r.celppade.custom_dock import Dock


import commands


class rdock(Dock):
    """Abstract class defining methods for a custom docking solution
    for CELPP
    """
    Dock.SCI_PREPPED_LIG_SUFFIX = '_prepared.sdf'
    Dock.SCI_PREPPED_PROT_SUFFIX = '_prepared.mol2'


    def ligand_technical_prep(self, sci_prepped_lig, targ_info_dict = {}):
        """
        'Technical preparation' is the step immediate preceding
        docking. During this step, you may perform any file
        conversions or processing that are specific to your docking
        program. Implementation of this function is optional.
        :param sci_prepped_lig: Scientifically prepared ligand file
        :param targ_info_dict: A dictionary of information about this target and the candidates chosen for docking.
        :returns: A list of result files to be copied into the
        subsequent docking folder. The base implementation merely
        returns the input string in a list (ie. [sci_prepped_lig]) 
        """
        return super(rdock,
                     self).ligand_technical_prep(sci_prepped_lig,
                                                 targ_info_dict = targ_info_dict)

    def receptor_technical_prep(self, sci_prepped_receptor, pocket_center, targ_info_dict = {}):
        """
        'Technical preparation' is the step immediately preceding
        docking. During this step, you may perform any file
        conversions or processing that are specific to your docking
        program. Implementation of this function is optional.
        :param sci_prepped_receptor: Scientifically prepared receptor file
        :param targ_info_dict: A dictionary of information about this target and the candidates chosen for docking.
        :returns: A list of result files to be copied into the
        subsequent docking folder. This implementation merely
        returns the input string in a list (ie [sci_prepped_receptor])
        """

        #####################################################
        ### rbcavity  -was  -d  -r  rDockGridGenInput.prm ###
        #####################################################
        
        # Make a generic grid gen prm file, with keys for replacement
        grid_gen_text = '''RBT_PARAMETER_FILE_V1.00
TITLE tech_prep

RECEPTOR_FILE !!!SCI_PREPPED_RECEPTOR!!!
RECEPTOR_FLEX 3.0

##################################################################
### CAVITY DEFINITION: REFERENCE LIGAND METHOD
##################################################################
SECTION MAPPER
    SITE_MAPPER RbtSphereSiteMapper
    CENTER (!!!X!!!,!!!Y!!!,!!!Z!!!)
    RADIUS 10.0
    SMALL_SPHERE 1.0
    MIN_VOLUME 100
    MAX_CAVITIES 1
    VOL_INCR 0.0
    GRIDSTEP 0.35
END_SECTION

#################################
#CAVITY RESTRAINT PENALTY
#################################
SECTION CAVITY
    SCORING_FUNCTION RbtCavityGridSF
    WEIGHT 1.0
END_SECTION
'''
        # Replace keys based on this structure's information
        grid_gen_text = grid_gen_text.replace('!!!SCI_PREPPED_RECEPTOR!!!',
                                              sci_prepped_receptor)
        grid_gen_text = grid_gen_text.replace('!!!X!!!', str(pocket_center[0]))
        grid_gen_text = grid_gen_text.replace('!!!Y!!!', str(pocket_center[1]))
        grid_gen_text = grid_gen_text.replace('!!!Z!!!', str(pocket_center[2]))

        # Write the prm text to a file
        with open('rDockGridGenInput.prm','wb') as of:
            of.write(grid_gen_text)

        # Run the grid generation
        grid_gen_cmd = 'rbcavity  -was  -d  -r  rDockGridGenInput.prm 1> gridGen.stdout 2> gridGen.stderr'
        commands.getoutput(grid_gen_cmd)

        # Return a list of files to be copied over for docking
        return ['rDockGridGenInput.as',
                'rDockGridGenInput.prm',
                sci_prepped_receptor]



    def dock(self, 
             tech_prepped_lig_list, 
             tech_prepped_receptor_list, 
             output_receptor_pdb, 
             output_lig_mol, 
             targ_info_dict={}):
        """
        This function is the only one which the contestant MUST
        implement.  The dock() step runs the actual docking
        algorithm. Its first two arguments are the return values from
        the technical preparation functions for the ligand and
        receptor. These arguments are lists of file names (strings),
        which can be assumed to be in the current directory. 
        If prepare_ligand() and ligand_technical_prep() are not
        implemented by the contestant, tech_prepped_lig_list will
        contain a single string which names a SMILES file in the
        current directory.
        If receptor_scientific_prep() and receptor_technical_prep() are not
        implemented by the contestant, tech_prepped_receptor_list will
        contain a single string which names a PDB file in the current
        directory.
        The outputs from this step must be two files - a pdb with the
        filename specified in the output_receptor_pdb argument, and a
        mol with the filename specified in the output_ligand_mol
        argument.
        :param tech_prepped_lig_list: The list of file names resturned by ligand_technical_prep. These have been copied into the current directory.
        :param tech_prepped_receptor_list: The list of file names resturned by receptor_technical_prep. These have been copied into the current directory.
        :param output_receptor_pdb: The final receptor (after docking) must be converted to pdb format and have exactly this file name.
        :param output_lig mol: The final ligand (after docking) must be converted to mol format and have exactly this file name.
        :param targ_info_dict: A dictionary of information about this target and the candidates chosen for docking.
        :returns: True if docking is successful, False otherwise. Unless overwritten, this implementation always returns False
        """
        
        ligand_sdf = tech_prepped_lig_list[0]
        receptor_as = tech_prepped_receptor_list[0]
        grid_gen_input = tech_prepped_receptor_list[1]
        receptor_mol2 = tech_prepped_receptor_list[2]
        # origdir = os.getcwd()
        try:
            # os.chdir(os.path.dirname(grid_gen_input))
            ######################################################################
            ### $ rbdock  -i  ligand.sdf  -o  output  -r  rDockGridGenInput.prm  -p  dock.prm  -n  50
            ######################################################################
            dock_cmd = 'rbdock  -i  ' + ligand_sdf + '  -o  output  -r  ' + os.path.basename(grid_gen_input) + ' -p  dock.prm  -n  50  1>  dock.stdout  2>  dock.stderr'
            commands.getoutput(dock_cmd)

            ######################################################################
            ### $ sdsort -n -fSCORE output.sd 1> output_sorted.sd
            ######################################################################
            sort_cmd = 'sdsort -n -fSCORE output.sd 1> output_sorted.sd 2> sdsort.stderr'
            commands.getoutput(sort_cmd)
        
            ######################################################################
            ### $ babel  -l  1  -isdf  best_ligand_pose.sd  -omol  docked_ligand.mol
            ######################################################################
            lig_babel_cmd = 'babel  -l  1  -isdf  output_sorted.sd  -omol ' + output_lig_mol + ' 1> lig_babel.stdout 2> lig_babel.stderr'
            commands.getoutput(lig_babel_cmd)
        
            ######################################################################
            ### $ babel -imol2  clean_receptor.mol2 -opdb  docked_receptor.pdb ###
            ######################################################################
            receptor_babel_cmd = 'babel  -imol2 ' + receptor_mol2 + '  -opdb ' + output_receptor_pdb + ' 1> recep_babel.stdout 2> recep_babel.stderr'
            commands.getoutput(receptor_babel_cmd)
        finally:
	    pass

        return True

        
if ("__main__") == (__name__):
    import os
    import logging
    import shutil
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("-l", "--ligsciprepdir", metavar="PATH", help = "PATH where we can find the scientific ligand prep output")
    parser.add_argument("-p", "--protsciprepdir", metavar="PATH", help = "PATH where we can find the scientific protein prep output")
    parser.add_argument("-o", "--outdir", metavar = "PATH", help = "PATH where we will put the docking output")
    # Leave option for custom logging config here
    logger = logging.getLogger()
    logging.basicConfig( format  = '%(asctime)s: %(message)s', datefmt = '%m/%d/%y %I:%M:%S', filename = 'final.log', filemode = 'w', level   = logging.INFO )
    opt = parser.parse_args()
    lig_sci_prep_dir = opt.ligsciprepdir
    prot_sci_prep_dir = opt.protsciprepdir
    dock_dir = opt.outdir
    #running under this dir
    abs_running_dir = os.getcwd()
    log_file_path = os.path.join(abs_running_dir, 'final.log')
    log_file_dest = os.path.join(os.path.abspath(dock_dir), 'final.log')
    docker = rdock()
    docker.run_dock(prot_sci_prep_dir,
                    lig_sci_prep_dir,
                    dock_dir)
    #move the final log file to the result dir
    shutil.move(log_file_path, log_file_dest)
