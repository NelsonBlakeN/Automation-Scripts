#!/bin/bash

date '+[ %m/%d/%Y %H:%M:%S ]'

echo "* Updating pip requirements for all projects"
echo "----------------------------"

# Switch to dev directory
cd /home/blake/Dropbox/DevWork/

# Loop through each project
for proj in */; do
    # Switch to current project
    cd "$proj"

    # If $proj has python env, continue
    if [[ -f .pyenv ]]; then
        echo "* Updating $proj"

        # Obtain env name and activate
        env=$(head -n 1 .pyenv)
        echo "* Activating $env"
        source /home/blake/Py3Envs/$env/bin/activate

        # Obtain list of outdated packages and update
        echo "* Updating outdated packages"
        outdated_list=$(pip list --outdated | awk '!/Package|----/ { print $1}')
        if [[ -z "$outdated_list" ]]; then
            echo "* Nothing to update."
        else
            pip install -U $outdated_list

            # Update requirements.txt
            echo "* Updating requirements file"
            pip freeze > requirements.txt

            echo "* Committing changes"
            git add requirements.txt
            git commit -m "Committing requirements changes. This is an automated command."
            git push
        fi

        # Clean up
        deactivate

        echo "* Finished with $proj ($env)"
        echo "----------------------------"
    fi

    cd ..
done

echo Complete.
echo

