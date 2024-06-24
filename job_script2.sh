#!/bin/bash
#SBATCH --mem=3900M
#SBATCH --nodes=5
#SBATCH --ntasks-per-node=20
#SBATCH --gres=gpu:p100:1
#SBATCH --time=40:00:00
#SBATCH --mail-user=tommyell@ualberta.ca
#SBATCH --mail-type=ALL

# setup

cd /home/tommyell/REINVENT4/

source venv/bin/activate
source activate DockStream

cd /$SCRATCH

module reset
module load StdEnv/2023 cuda/12.2 python/3.11.5 rdkit

# command
reinvent /home/tommyell/CANADAINTERNSHIP/RL_direct_for_upload2.toml





