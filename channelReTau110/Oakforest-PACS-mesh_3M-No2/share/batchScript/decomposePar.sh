#!/bin/bash

if [ "$PJM_ENVIRONMENT" = "INTERACT" ];then
    mpi=1
    MPLIB=OPENMPI
else
    if [ -z "${PJM_JOBID+x}" ] ; then
	PJM_JOBID=$1
	mpi=1
	MPLIB=OPENMPI
    else
	export HOME=/work/$(id -gn)/$(id -un)
	cd $PJM_O_WORKDIR
	mpi=${PJM_MPI_PROC}
	MPLIB=INTELMPI
    fi
fi

# OpenFOAM-v1612+, ThirdParty Gcc, INTELMPI 2017.1.132
module purge
module load gcc/4.8.5
module unload impi
if [ "$MPLIB" = "INTELMPI" ];then
    module load impi/2017.1.132
    export MPI_ROOT=$I_MPI_ROOT
fi
export I_MPI_DEBUG=5
. ${HOME}/OpenFOAM/OpenFOAM-v1612+/etc/bashrc \
    WM_COMPILER_TYPE=ThirdParty \
    WM_COMPILER=Gcc \
    WM_MPLIB=$MPLIB \
    WM_LABEL_SIZE=32

# Application name
application=decomposePar.sh

# Log file
log=log.${application}.${PJM_JOBID}
batchFileDone=${application}.done

env > $log 2>&1 
if [ $mpi -eq 1 ];then
    decomposePar >> $log 2>&1
else
    unset FOAM_SIGFPE
    mpirun redistributePar -overwrite -decompose -parallel >> $log 2>&1 
fi
grep "^End" $log >& /dev/null && touch $batchFileDone

#------------------------------------------------------------------------------
