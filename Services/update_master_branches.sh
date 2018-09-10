#!/bin/bash

date '+[ %m/%d/%Y %H:%M:%S ]'
printf "* Updating all master branches...\n"

# Start in development directory
cd /home/blake/Dropbox/DevWork

# Loop through each project folder
for folder in */; do
    # Switch to current directory
    cd "$folder"

    git status &> /dev/null
    if [[ $? -eq 0 ]]; then
        # Folder is a repository
        echo "* Updating repo: $folder"

        # Store branch
        orig_branch=$(git status | awk '$1=="On"{print $3}')
        echo "* Current branch is $orig_branch"

        # Switch to master
        git checkout master 2>&1 &> /dev/null
        if [[ $? -ne 0 ]]; then
            echo "- A problem occured when checking out master. Skipping"
            continue
        fi

        # Pull in staging, or fail silently
        echo -n "* Merging..."
        output="$(git merge staging 2>&1)"
        if [[ $? -eq 0 ]]; then
            echo "$output"
        else
            # Check for merge conflicts
            error_msg=$(echo $output | grep -oP '(; fix)\s+\K\S+')
            if [[ $error_msg == "conflicts" ]]; then
                printf "\n- Merge conflicts occured:\n"
                echo $output
            else
                echo "* No staging branch found."
            fi
        fi

        # Switch back to current branch
        current_branch=$(git status | awk '$1=="On"{print $3}')
        if [[ $current_branch != $orig_branch ]]; then
            git checkout $orig_branch
        fi

        # Continue
        echo
    fi

    cd ..
done

printf "Complete.\n\n"
