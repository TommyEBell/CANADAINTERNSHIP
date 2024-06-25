# This file Contains the workflow for using REINVENT4 with AutoDock Vina as a scoring component (on Compute Canada).

## Workflow:
<b/> 1. Clone the repo </b>
```shell
git clone https://github.com/TommyEBell/CANADAINTERNSHIP
```
<b/> 2. Install all software </b>
```shell
chmod +x reinvent_install.sh
./reinvent_install.sh
```
<b/> 3. Test run to ensure all software installations were successful </b>
```shell
cd /$SCRATCH
sbatch /$HOME/CANADAINTERNSHIP/job_script_test.sh
```
Once this has finished running (takes no more than 10 minutes), nano the slurm file to check for any errors. Given there is none, the software is successfully installed for use.

## Worflow to reproduce REINVENT article: 
Article link: https://link.springer.com/article/10.1186/s13321-024-00812-5#MOESM1



## Workflow for general use:

In your job scripts, you use always include the code below which activates the virtual environments required to run REINVENT4 and DockStream. 

```shell
cd /home/tommyell/REINVENT4/

source venv/bin/activate
source activate DockStream

cd /$SCRATCH

module reset
module load StdEnv/2023 cuda/12.2 python/3.11.5 rdkit
```

### (Target) preperation

To convert your protein targets file from pdb to pdbqt run the following command:
```shell
/$HOME/miniconda/envs/DockStream/bin/python /$HOME/DockStream/target_preparator.py -conf {target_prep_path}
```
An example of a target preparation configuration file is CANADAINTERNSHIP/2xch_target_preperation.json, which is set up for the 2xch.pdb file (used in the REINVENT4 article). In the majority of cases only the locations of the files should be changed in the target preparation file.

Target preparation also finds the location of the ligand inputted in the configuration file, where the centre co-ordinates and 'box' of the ligand are given in the target preparation log file. Here is an example:
```
2024-06-10 03:32:40 - DockStream version used: 1.0.0
2024-06-10 03:32:41 - Warning: importing 'simtk.openmm' is deprecated.  Import 'openmm' instead.
2024-06-10 03:32:57 - Started preparation run number 0.
2024-06-10 03:32:58 - Ligand from file /content/drive/MyDrive/Colab_Notebooks/DockStream-master/case_study_files/2xch_ligand.pdb has the following dimensions:
X coordinates: min=-45.16, max=-34.03, mean=-39.69
Y coordinates: min=13.09, max=21.75, mean=17.02
Z coordinates: min=10.83, max=14.81, mean=12.63
2024-06-10 03:32:58 - Wrote AutoDock Vina target to file /content/ADV_receptor.pdbqt.
2024-06-10 03:32:58 - Completed target preparation run number 0.
```
From this information you would then input the data into the docking configuration file (e.g. CANADAINTERNSHIP/2xch_docking_config.json):
```
  "search_space": {
    "--center_x": -39.7,
    "--center_y": 17,
    "--center_z": 12.6,
    "--size_x": 15,
    "--size_y": 10,
    "--size_z": 10
```
Again, like the target preparation configuration file, for the docking one, largely it should just be the file paths that are changed with the exception of the search space of a different protein is being used and number_cores <b/>(VERY IMPORTANT)</b>.

### TL

To run transfer learning simply run the code:
```shell
reinvent /$HOME/CANADAINTERNSHIP/TL_setup.toml
```
This is currently configured following previously mentioned articles parameters. Only the SMILES and prior used can be changed here. 

### RL
To run reinforcement learning run the code:
```shell
reinvent /$HOME/CANADAINTERNSHIP/RL_setup_2xch.toml
```
This example is also configured for 2xch (used in the article). In this configuration file, commonly altered variables include:
* agent_file - ##################################
* prior_file - ##################################
* batch_size - The number of SMILES being generated for each step/epoch.
* sigma - The scaling factor of the score in the calculation of the augmented NLL (see article).
* rate - learning rate.
* bucket_size - The number of SMILES allowed to have a similar scaffold/structure.
* max_steps - The number of steps/epoch in the RL run.
Also ensure the file location paths are correct before running.

<b/> NOTE: </b> When running RL this takes a significant amount of time, for the configuration used in the article (RL_setup_2xch.toml) it required 20-30hrs with 100CPUs, when changing the number of CPUs in the sbatch file, they will not be utilised unless number_cores is altered in the docking configuration file.

## Specific workflow to reproduce the article data



### For other run modes see the REINVENT4 github repo for examples (https://github.com/MolecularAI/REINVENT4). 
