#!/bin/bash

if [ -z "${PBS_JOBID+x}" ] ; then
    PBS_JOBID=$1
else
    cd $PBS_O_WORKDIR
fi

module purge;module load openmpi/1.8.1-gnu;unset FOAM_INST_DIR;. $HOME/OpenFOAM/OpenFOAM-4.1/etc/bashrc WM_COMPILER=Gcc WM_MPLIB=SYSTEMOPENMPI;export PATH=/opt/openmpi-1.8.1-gnu-3.5-1-MIC-beta1+mpss32/bin${PATH:+:$PATH}
application=decomposePar.sh

log=log.${application}.${PBS_JOBID}
(
    env
    decomposePar -cellDist
    rbstat -s ${PBS_JOBID}    
) >& $log 

grep "^End" $log >& /dev/null
[ $? -eq 0 ] && touch ${application}.done
