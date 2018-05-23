#!/bin/bash

date '+[ %m/%d/%Y %H:%M:%S ]'

echo Running expense report...
source /home/blake/Py3Envs/cfp/bin/activate

/home/blake/Dropbox/DevWork/CashFlowParser/CFPApp

printf "Complete.\n"
