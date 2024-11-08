#!/bin/bash
#SBATCH --qos turing
#SBATCH --time 0:30:0
#SBATCH --nodes 1
#SBATCH --gpus 0
#SBATCH --cpus-per-task 5
#SBATCH --mem 32768
#SBATCH --job-name ollama-setup

# Execute using:
# sbatch ./batch-ollama-setup.sh

module purge
module load baskerville
module load bask-apps/live
module load Python/3.11.3-GCCcore-12.3.0

set -e

cd /bask/projects/path/to/your/directory

VENV_PATH="./venv"

if [ -d "$VENV_PATH" ]; then
    echo "Already set up. You should only run this once."
    exit 1
fi

echo
echo "######################################"
echo "Starting"
echo "######################################"
echo

echo "Unpacking example"
unzip ollama_example.zip

echo "Installing ollama"
mkdir ollama_install
pushd ollama_install
curl -L https://ollama.com/download/ollama-linux-amd64.tgz -o ollama-linux-amd64.tgz
mkdir usr
tar -C usr -xvf ollama-linux-amd64.tgz 
popd

echo "Starting ollama server"
export PATH=${PATH}:${PWD}/ollama_install/usr/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${PWD}/ollama_install/usr/lib
export OLLAMA_MODELS=${PWD}/ollama_install/models
ollama serve &
sleep 10

echo "Getting ollama model"
ollama pull llama3.2:1b
ollama list
sleep 1
pkill ollama

echo "Creating virtual environment"
python3 -m venv "${VENV_PATH}"
. "${VENV_PATH}"/bin/activate
echo "Installing requirements"
pip install pip --upgrade
pip install ollama

echo
echo "######################################"
echo "Done"
echo "######################################"
echo

echo "Deactivating virtual environment"
deactivate
popd
