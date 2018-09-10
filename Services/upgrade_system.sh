#!/bin/bash

# Print datetime for logging
dt=$(date '+%m/%d/%Y %H:%M:%S');
echo "[ $dt ]"
echo "Updating system..."

# Root validation and upgrade execution
if [[ $EUID -ne 0 ]]; then
    printf "\nThis script must be run as root. Exiting\n"
else
    echo "y" | pacman -Syu
fi

echo "Upgrade complete."
echo
