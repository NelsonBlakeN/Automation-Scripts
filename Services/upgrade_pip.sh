#!/bin/bash

date '+[ %m/%d/%Y %H:%M:%S ]'

envs=/home/blake/Py3Envs

# Change directory to venvs
cd $envs

# For each folder in dir, check for .pyenv
for env in */; do
    echo "* Updating pip for $env:"

    # Activate env
    source $envs/$env/bin/activate

    # Upgrade pip
    pip install --upgrade pip
done

echo "Complete."
echo
