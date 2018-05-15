#!/bin/bash

# echo "$(date)"
date '+[ %m/%d/%Y %H:%M:%S ]'
echo "Cleaning Trash folder..."

files_to_delete="$(find /home/blake/.local/share/Trash/* -mtime +21 -print | wc -l)"
printf "Deleting %s files...\n" "$files_to_delete"

if [[ $files_to_delete -gt 0 ]]
then
    find /home/blake/.local/share/Trash/* -mtime +21 -print0 | xargs -0 rm -r
fi

printf "Complete.\n\n"
