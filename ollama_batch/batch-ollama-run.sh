#!/bin/bash
#SBATCH --qos turing
#SBATCH --time 0:30:0
#SBATCH --nodes 1
#SBATCH --gpus 1
#SBATCH --mem 32768
#SBATCH --job-name ollama-setup

# Execute using:
# sbatch ./batch-ollama-run.sh

module purge
module load baskerville
module load bask-apps/live
module load Python/3.11.3-GCCcore-12.3.0

set -e

cd /bask/projects/path/to/your/directory

VENV_PATH="./venv"

if [ -d "$VENV_PATH" ]; then
    echo "Virtual environment exists, activating"
    . "${VENV_PATH}"/bin/activate
else
    echo "Please sbatch the setup script before running this."
    exit 1
fi

echo "Configuring ollama"
export PATH=${PATH}:${PWD}/ollama_install/usr/bin
export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${PWD}/ollama_install/usr/lib
export OLLAMA_MODELS=${PWD}/ollama_install/models

# Want to avoid port conflicts
export OLLAMA_GAME_PORT=$((21000 + ($RANDOM % 500)))
export OLLAMA_HOST=127.0.0.1:${OLLAMA_GAME_PORT}

echo "Ollama host is ${OLLAMA_HOST}"

echo
echo "######################################"
echo "Starting"
echo "######################################"
echo

pushd ollama_example
echo "Starting ollama server"
ollama serve &

echo "Waiting for the server to inialise"
sleep 10

echo "Starting script"
python3 script/score_pizza.py "--host_port ${OLLAMA_HOST}" "--model llama3.2:1b"
popd

echo
echo "######################################"
echo "Done"
echo "######################################"
echo

echo "Stopping ollama"
pkill ollama

echo "Deactivating virtual environment"
deactivate
popd
