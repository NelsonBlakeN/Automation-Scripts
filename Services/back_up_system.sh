#!/bin/bash
# Full System Backup

date '+[ %m/%d/%Y %H:%M:%S ]'

distro=arch
type=full
date=$(date '+%F')

# Check that the USB is present
if [ -d /run/media/blake/94D6-BB20 ]; then
    BACKUP_LOC=/run/media/blake/94D6-BB20/$distro-$type-$date.tar.gz
else
    echo "Backup location not found; exiting."
    exit 1
fi

# Check if user is root
if [[ $EUID -ne 0 ]]; then
    printf "This script must be run as root; exiting.\n"
    exit 2
fi

# Delete old backups (only one will realistically fit)
echo "Removing old backups..."
if [ -f /run/media/blake/94D6-BB20/arch-full-* ]; then
    rm -f /run/media/blake/94D6-BB20/arch-full-*
fi

# Create the backup
echo "Creating backup..."

tar --exclude={"/dev/*","/proc/*","/sys/*","/tmp/*","/run/*","/mnt/*","/media/*","/lost+found/*","/home/blake/VirtualBox*","/home/images/*"} --xattrs -czpvf $BACKUP_LOC /

printf "Complete.\n"

: <<'RESTORE'
To restore from this backup, mount all relevant partitions,
change the current working directory to the root directory,
then run:
    tar --xattrs -xpf $backupfile
where $backupfile is the backup archive.
RESTORE

: <<'TAR OPTIONS'
Option explanations:
-c : Create a new archive
-z : Filter the archive through gzip (compress)
-p : Preserve permissions
-v : Verbose
-f : Use archive file
--xattrs : Enable extended attributes support
--exclued : Exclude certain files/directories
TAR OPTIONS
