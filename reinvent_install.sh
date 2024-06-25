#!/bin/bash

cd ~/


wget -qO- https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh > miniconda.sh
bash miniconda.sh -b -p ~/miniconda

# Update PATH environment variable to include conda
export PATH=~/miniconda/bin:$PATH

# Verify conda installation
conda --version

# Install Vina
conda install -c bioconda autodock-vina -y


# Install DockStream
git clone https://github.com/MolecularAI/DockStream.git

cd ~/DockStream/

pip install .

conda env create -f environment.yml

conda init bash

source activate DockStream

cd ~/

# Install REINVENT4
git clone https://github.com/MolecularAI/REINVENT4.git

cd ~/REINVENT4

module reset
module load StdEnv/2023 cuda/12.2 python/3.11.5 rdkit

virtualenv --no-download venv
source venv/bin/activate
pip install --upgrade pip

pip install chemprop hyperopt molvs mmpdb openeye-toolkits

pip install --no-index python_dotenv torch==2.2.1 torchvision==0.17.1 torchaudio==2.2.1 tensorboard absl-py tomli pathos xxhash pydantic==2.7.3

pip install --no-index --no-deps .

cd ~/

# check installs

reinvent --help

vina --version

# clone REPO CONTAINING MOCK CONFIG FILES
git clone https://github.com/TommyEBell/CANADAINTERNSHIP

# Edit a file

rm ~/REINVENT4/venv/lib/python3.11/site-packages/reinvent/runmodes/RL/reports/tensorboard.py

mv ~/CANADAINTERNSHIP/tensorboard.py ~/REINVENT4/venv/lib/python3.11/site-packages/reinvent/runmodes/RL/reports/

# make outputs directory

mkdir outputs

# Make all the config files with your username 

# Get the full path to the home directory
home_dir=$(echo $HOME)

# Find all files in the current directory and its subdirectories
find /$HOME/CANADAINTERNSHIP/ -type f -exec grep -l '/home/tommyell/' {} \; | while read file
do
  # Use sed to replace /home/tommyell/ with the home directory
  sed -i "s|/home/tommyell/|$home_dir/|g" "$file"
done

