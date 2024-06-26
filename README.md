# This file Contains the workflow for using REINVENT4 with AutoDock Vina as a scoring component (on Compute Canada).

## Installation:
<b/> 1. Clone the repo </b>
```shell
cd /$HOME
git clone https://github.com/TommyEBell/CANADAINTERNSHIP
```
<b/> 2. Move the installation script </b>
```shell
cd CANADAINTERNSHIP
mv reinvent_install.sh /$HOME
cd /$HOME
```
<b/> 3. Install all software </b>
```shell
chmod +x reinvent_install.sh
./reinvent_install.sh
```
<b/> 4. Test run to ensure all software installations were successful </b>
```shell
cd /$SCRATCH
sbatch /$HOME/CANADAINTERNSHIP/job_script_test.sh
```
Once this has finished running (takes no more than 10 minutes), nano the slurm file to check for any errors. Given there is none, the software is successfully installed for use.

## Workflow for general use:

In your job scripts, you use always include the code below which activates the virtual environments required to run REINVENT4 and DockStream. 

```shell
cd /$HOME/REINVENT4/

source venv/bin/activate
source activate DockStream

cd /$SCRATCH

module reset
module load StdEnv/2023 cuda/12.2 python/3.11.5 rdkit
```
All output files for the runs prepared in this repo have been directed to /$HOME/outputs/ 
### (Target) preperation

To convert your protein targets file from pdb to pdbqt run the following command:
```shell
/$HOME/miniconda/envs/DockStream/bin/python /$HOME/DockStream/target_preparator.py -conf {target_prep_path}
```
An example of a target preparation configuration file is CANADAINTERNSHIP/2xch_target_preperation.json, which is set up for the 2xch.pdb file (used in the REINVENT4 article: https://link.springer.com/article/10.1186/s13321-024-00812-5#MOESM1). In the majority of cases only the locations of the files should be changed in the target preparation file.

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

To run transfer learning (shift a prior to produce molecules more related to a drug target) simply run the code:
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
* agent_file - The model/prior that is being improved.
* prior_file - The base model/prior.
* batch_size - The number of SMILES being generated for each step/epoch.
* sigma - The scaling factor of the score in the calculation of the augmented NLL (see article).
* rate - learning rate.
* bucket_size - The number of SMILES allowed to have a similar scaffold/structure.
* max_steps - The number of steps/epoch in the RL run.
Also ensure the file location paths are correct before running.

<b/> NOTE: </b> When running RL this takes a significant amount of time, for the configuration used in the article (RL_setup_2xch.toml) it required ~25hrs with 100CPUs, when changing the number of CPUs in the sbatch file, they will not be utilised unless number_cores is altered in the docking configuration file.

## Specific workflow to reproduce the article data
<b/> Prefaces: </b> For each of the code given, they should be run in seperate job script files and run via sbatch with at least 1 GPU and CPU (GPU parallelisation not yet avaiable so only increase CPUs for it to run faster), the job_script_test.sh file can be used as an example of what a job script shell file should look like. <b/>V.IMPT:</b> When altering CPU number ensure you change the number of CPUs DockStream can use by changing number_cores in /$HOME/CANADAINTERNSHIP/2xch_docking_config.json.

All file paths should have been automatically altered to match your directory but this should be checked to verify.



<b/> 1. Run RL on reinvent prior </b>
```shell
reinvent /$HOME/CANADAINTERNSHIP/RL_setup_2xch.toml
```
This should take around 25hrs on 100 CPUs.


<b/> 2. Run RL on TL prior </b>
```shell
reinvent /$HOME/CANADAINTERNSHIP/RL_setup_2xch_TL.toml
```
Both these steps can be run at the same time.


Once these runs have finished, the 2 files you need are named 2xch_rl_TL1.csv and 2xch_rl_1.csv as well as the 2 directories 2xch_rl/ and 2xch_rl_TL/. These can be found at /$HOME/outputs/. The rest of the files are outputs from the DockStream calculations. the .csv files contains all the SMILEs as well as their score breakdowns.


To get to compare the cumulative number of hits between the two models run the code given below, ensuring the paths to the two .csv files are altered.
```shell
import pandas as pd
import matplotlib.pyplot as plt

def count_hits(csv_file):
    # Load the data from the CSV file
    df = pd.read_csv(csv_file)

    # Initialize a dictionary to store the counts for each step
    counts = {}

    # Initialize a counter for the cumulative hits
    cumulative_hits = 0

    # Loop over the steps
    for step in range(1, 51):
        # Select the rows for the current step
        df_step = df[df['step'] == step]
    
        # Apply the conditions on 'Docking into 2XCH grid (raw)' and 'QED (raw)'
        condition = (df_step['Docking into 2XCH grid (raw)'] < -8) & (df_step['QED (raw)'] > 0.7)
    
        # Count the number of rows that meet the conditions
        hits = condition.sum()

        # Add the hits to the cumulative hits
        cumulative_hits += hits

        # Store the cumulative hits in the dictionary
        counts[step] = cumulative_hits

    return counts

# Use the function to process the two CSV files - 'your_input' REQUIRED HERE
counts1 = count_hits('PUT_TL_CSV_FILE_PATH_HERE')
counts2 = count_hits('PUT_STANDARD_RL_CSV_FILE_PATH_HERE')

# Convert the dictionaries to lists
steps = list(counts1.keys())
hits_counts1 = list(counts1.values())
hits_counts2 = list(counts2.values())

# Create a bar plot
plt.figure(figsize=(10, 6))
plt.plot(steps, hits_counts1, color='blue', alpha=0.5, label='TL')
plt.plot(steps, hits_counts2, color='red', alpha=0.5, label='base prior')

# Add labels and title
plt.xlabel('Step')
plt.ylabel('Cumulative Number of Hits')
plt.title('Cumulative Number of Hits with Docking < -8 and QED > 0.7 for each step')
plt.legend()

# Show the plot
plt.show()
```
The directories outputed can be used to visualise a variety of data, the code requried to do so is given below (ensure you change the directory path as required):
```shell
# Load the TensorBoard notebook extension
%load_ext tensorboard

# Start TensorBoard within the notebook using magics function
%tensorboard --logdir 'PATH_TO_DIRECTORY/2xch_rl_TL/'
```


### For other run modes see the REINVENT4 github repo for examples (https://github.com/MolecularAI/REINVENT4). 

