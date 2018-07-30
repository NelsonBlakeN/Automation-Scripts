#!/bin/bash

date '+[ %m/%d/%Y %H:%M:%S ]'
echo -n "* Reviewing old files..."

MAIL=/home/blake/scripts/Automation/cleanup_review/cleanup_review.py

# Save and count number of old Downloads files
downloads="$(find /home/blake/Downloads/ -mtime +19 -print)"
num_downloads="$(find /home/blake/Downloads/ -mtime +19 -print | wc -l)"

# Count number of files in trash
trash="$(find /home/blake/.local/share/Trash/ -mtime +19 -print)"
num_trash="$(find /home/blake/.local/share/Trash/ -mtime +19 -print | wc -l)"
echo "complete."

echo -n "* Running python script..."
# Pass all data into the python script, which will send the notification
$MAIL $num_downloads "$downloads" $num_trash "$trash"
[[ $? -eq 0 ]] && echo "complete."

if [[ $num_downloads -ne 0 ]]; then
   echo "* Found $num_downloads impending Downloads deletion(s): "
   echo "$downloads" | awk '{print "\t"$0 }'
   echo
fi

if [[ $num_trash -ne 0 ]]; then
   echo "* Found $num_trash impending Trash deletion(s): "
   echo "$trash" | awk '{print "\t"$0 }'
fi

echo Complete.
echo
