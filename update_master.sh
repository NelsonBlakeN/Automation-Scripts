#!/bin/bash

date '+[ %m/%d/%Y %H:%M:%S ]'
echo "Updating all master branches..."

# Start in development directory
cd ~/Dropbox/DevWork

# Loop through each project folder
for folder in */; do
    # Switch to current directory
    cd "$folder"

    git status &> /dev/null
    if [[ $? -eq 0 ]]; then
        # Folder is a repository
        echo "Updating repo: $folder"

        # Store branch
        orig_branch=$(git status | awk '$1=="On"{print $3}')
        echo "Current branch is $orig_branch"

        # Switch to master
        git checkout master &> /dev/null
        if [[ $? -ne 0 ]]; then
            echo "A problem occured when checking out master. Skipping"
            continue
        fi

        # Pull in staging, or fail silently
        output="$(git merge staging 2>&1)"
        if [[ $? -eq 0 ]]; then
            echo "$output"
        else
            # Check for merge conflicts
            error_msg=$(echo $output | grep -oP '(; fix)\s+\K\S+')
            if [[ $error_msg == "conflicts" ]]; then
                echo "Merge conflicts occured:"
                echo $output
            else
                echo "No staging branch found."
            fi
        fi

        # Switch back to current branch
        git checkout $orig_branch

        # Continue
    fi

    cd ..
done

echo "Complete."
