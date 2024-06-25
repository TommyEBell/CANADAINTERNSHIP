#!/bin/bash
#SBATCH --mem=3900M
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=5
#SBATCH --gres=gpu:p100:1
#SBATCH --time=00:10:00
#SBATCH --account=def-barakat
#SBATCH --mail-type=ALL

# setup

cd /$HOME/REINVENT4/

source venv/bin/activate
source activate DockStream

cd /$SCRATCH

module reset
module load StdEnv/2023 cuda/12.2 python/3.11.5 rdkit

# command
reinvent /$HOME/CANADAINTERNSHIP/RL_setup_test.toml





