import os
vsroot = os.getcwd()
outputs_dir = os.path.join(vsroot, 'outputs')
os.makedirs(outputs_dir, exist_ok=True)
home_dir = /$HOME
# SO DO I WANT THEM AS PDB FILES- IF PREPARED BEFORE HAND JUST NEED RECEPTOR.pdbqt and search site
receptor_file = input('What is the name of the receptor (e.g. receptor.pdb): ')

try:
	if os.path.isfile(receptor_file)==True:
		if receptor_file.endswith('.pdb')==True:
			print(f'File recognised, using "{receptor_file}" as the receptor.')
		elif receptor_file.endswith('.pdb')==False:
			print('Please ensure the file is a .pdb')
	elif os.path.isfile(receptor_file)==False:
		print('File not recognised, ensure the file is located in this current working directory and try again')
except Exception as e:
	print(f"An error occurred: {e}")

ligand_file =input('What is the name of the ligand (e.g. ligand.pdb): ')
try:
        if os.path.isfile(ligand_file)==True:
                if ligand_file.endswith('.pdb')==True:
                        print(f'File recognised, using "{ligand_file}" as the ligand.')
                elif ligand_file.endswith('.pdb')==False:
                        print('Please ensure the file is a .pdb')
        elif os.path.isfile(ligand_file)==False:
                print('File not recognised, ensure the file is located in this current working directory and try again')
except Exception as e:
        print(f"An error occurred: {e}")





print('Stage 1: Preparing the docking configuration file')
# LABEL ALL OF THE PARAMETERS ADN PROPABABLY EACH LINE
log_file_docking = output_dir + "/ADV_docking.log"
binary_dir = home_dir + "/miniconda/bin/"
recetor_dir = vsroot + "/" + receptor_file
docking_file = vsroot + "/docking_configuration.json"

num_cores = # can made just have this 200 and it would be fine?
print('Please input the search space parameters.')
center_x = input('Input the x co-ordinate of the ligands centre: ')
center_y = input('Input the y co-ordinate of the ligands centre: ')
center_z = input('Input the z co-ordinate of the ligands centre: ')
size_x = input("Input the length of the box's x-dimenesion: ")
size_y = input("Input the length of the box's y-dimenesion: ")
size_z = input("Input the length of the box's z-dimenesion: ")


# specify the embedding and docking JSON file as a dictionary and write it out
ed_dict = {
  "docking": {
    "header": {                                         # general settings
      "logging": {                                      # logging settings (e.g. which file to write to)
        "logfile": log_file_docking
 }
    },
    "ligand_preparation": {                             # the ligand preparation part, defines how to build the pool
      "embedding_pools": [
        {
          "pool_id": "RDkit_pool",                     # here, we only have one pool
          "type": "RDKit",
	},
          "input": {
            "standardize_smiles": False,
          }
       ]
    },
    "docking_runs": [
    {
      "backend": "AutoDockVina",
      "run_id": "AutoDockVina",
      "input_pools": ["RDKit_pool"],
      "parameters": {
        "binary_location": binary_dir,    # absolute path to the folder, where the "vina" binary
                                                               # can be found
        "parallelization": {
          "number_cores": num_cores
        },
        "seed": 42,                                     # use this "seed" to generate reproducible results; if
                                                        # varied, slightly different results will be produced
        "receptor_pdbqt_path": receptor_dir,     # paths to the receptor files
        "number_poses": 2,                              # number of poses to be generated
        "search_space": {                               # search space (cavity definition); see text
          "--center_x": center_x,
          "--center_y": center_y,
          "--center_z": center_z,
          "--size_x": size_x,
          "--size_y": size_y,
          "--size_z": size_z
        }
      },
      "output": {
        "poses":{
            "poses_path": "/home/tommyell/outputs/2xch_ligands_docked.sdf",
            "overwrite": false
          },
          "scores": {
            "scores_path": "/home/tommyell/outputs/2xch_scores.csv",
            "overwrite": false
          }

}}]}}

with open(docking_file, 'w') as f:
	json.dump(ed_dict, f, indent=2)




print('Stage 2: Creating the reinforcement learning configuration file')

RL_dict = {
version = 4 # REINVENT4, do not recommend changing
run_type = "staged_learning" 
use_cuda = true
output_csv = ".csv"
tb_logdir = "/home/tommyell/outputs/2xch_rl"

[parameters]
use_checkpoint = false
summary_csv_prefix = "/home/tommyell/outputs/2xch_rl"
agent_file = "/home/tommyell/REINVENT4/priors/reinvent.prior"
prior_file = "/home/tommyell/REINVENT4/priors/reinvent.prior"

batch_size = 50
uniquify_smiles = true
randomize_smiles = true

[learning_strategy]

type = "dap"
sigma = 128
rate = 0.0005

[diversity_filter]

type = "IdenticalMurckoScaffold"
bucket_size = 50
minscore = 0.4

[[stage]]
chkpt_file = '/home/tommyell/CANADAINTERNSHIP/rl_direct.chkpt'
termination = "simple"
max_steps = 50

[stage.scoring]
type = "geometric_mean"

[[stage.scoring.component]]
[[stage.scoring.component.DockStream.endpoint]]
name = "Docking into 2XCH grid"
weight = 1
params.configuration_path = "/home/tommyell/CANADAINTERNSHIP/2xch_docking_config.json"
params.docker_script_path = "/home/tommyell/DockStream/docker.py"
params.docker_python_path =  "/home/tommyell/miniconda/envs/DockStream/bin/python"
transform.type = "reverse_sigmoid"
transform.high = -7
transform.low = -13.5
transform.k = 0.2

[[stage.scoring.component]]
[stage.scoring.component.QED]
[[stage.scoring.component.QED.endpoint]]
name = "QED"
weight = 1








}


