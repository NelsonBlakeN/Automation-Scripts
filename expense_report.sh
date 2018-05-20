#!/bin/bash

date '+[ %m/%d/%Y %H:%M:%S ]'

echo Running expense report...
source $HOME/Py3Envs/cfp/bin/activate

$HOME/Dropbox/DevWork/CashFlowParser/CFPApp

printf "Complete.\n"
