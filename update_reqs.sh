#!/bin/bash

date '+[ %m/%d/%Y %H:%M:%S ]'

echo "Updating requirements for all projects"

# Obtain list of outdated packages
$outdated_list=$(pip list --outdated | awk '!/Package|----/ { print $1}')
