#!/bin/bash

date '+[ %m/%d/%Y %H:%M:%S ]'

echo "Updating pip requirements for all projects"

# Switch to dev directory
cd /home/blake/Dropbox/DevWork/

# Loop through each project
for proj in */; do
    # Switch to current project
    cd $proj

    # If $proj has python env, continue
    if [[ -f .pyenv ]]; then
        echo Updating $proj

        # Obtain env name and activate
        env=$(head -n 1 .pyenv)
        echo Activating $env
        source /home/blake/Py3Envs/$env/bin/activate

        # Obtain list of outdated packages and update
        outdated_list=$(pip list --outdated | awk '!/Package|----/ { print $1}')
        pip install -U $outdated_list

        # Update requirements.txt
        pip freeze > requirements.txt

        # Clean up
        deactivate
    fi

    cd ..
done

echo Complete.
echo

