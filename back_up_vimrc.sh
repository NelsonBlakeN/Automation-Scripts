#!/bin/bash
# Back up vimrc file

date '+[ %m/%d/%Y %H:%M:%S ]'
echo -n "* Calculating checksums..."

home=/home/blake

vimrc_backup=$(md5sum $home/Dropbox/DevWork/vimrc/.vimrc | awk '{print $1}')
vimrc_current=$(md5sum $home/.vimrc | awk '{print $1}')
echo "done."

echo "* Comparing..."
if [[ $vimrc_backup -ne $vimrc_current ]]; then
    echo "* Current vimrc file is different than the backup."
    echo -n "* Syncing..."
    cp $home/.vimrc $home/Dropbox/DevWork/vimrc/
    echo "done."
else
    echo "* Backup is up to date."
fi

echo "* Complete."
