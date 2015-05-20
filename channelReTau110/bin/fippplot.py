#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import pylab
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

data=np.genfromtxt("fipptable.csv", names=True, delimiter=',', dtype=None)

pp = PdfPages('fipp.pdf')

mpl.rcParams.update({'font.size': 12})

nCellsArray=np.unique(data['nCells'])
LESModelArray=np.unique(data['LESModel'])
solverArray=np.unique(data['solver'])
nProcsArray=np.unique(data['nProcs'])

pylab.subplots_adjust(bottom=0.5)

for nCells in nCellsArray:
    for LESModel in LESModelArray:
        for nProcs in nProcsArray:
            idx=np.where(
                (data['nCells']==nCells)
                & (data['LESModel']==LESModel)
                & (data['nProcs']==nProcs)
                )

            solver=data['solver'][idx]
            preconditioner=data['preconditioner'][idx]
            solvers=np.core.defchararray.add(np.core.defchararray.add(solver, "-"),preconditioner)

            y=data['MFLOPSPEAK'][idx]

            sn,index0 = np.unique(solvers, return_index=True)
            index1=index0[1:]
            index1=np.append(index1,len(y))
            MFLOPSPerPeakAve=np.zeros(len(sn))
            MFLOPSPerPeakSTD=np.zeros(len(sn))
            for i in range(len(sn)):
                MFLOPSPerPeak=y[index0[i]:index1[i]]
                MFLOPSPerPeakAve[i]=np.average(MFLOPSPerPeak)
                MFLOPSPerPeakSTD[i]=np.std(MFLOPSPerPeak)

            base=str(nCells)+"cells-"+LESModel+"-"+str(nProcs)+"MPI-performance"
            print base

            x=np.arange(len(sn))

            offset=(x[len(x)-1]-x[0])*0.05
            xmin=x[0]-offset
            xmax=x[len(x)-1]+offset

            plt.title("MFLOPS per peak\n("+
                      str(nCells/1e+6)+"M cells, "+LESModel+" ,"+str(nProcs)+" MPI)")
            plt.plot(x,MFLOPSPerPeakAve, label="MFLOPS per peak [%]", linewidth=1)
            plt.errorbar(x, MFLOPSPerPeakAve, yerr=MFLOPSPerPeakSTD, fmt='.', linewidth=2)
            plt.xlabel('Matrix solver for pressure equation')
            plt.xticks(x,sn, rotation=-90)
            plt.ylabel('MFLOPS per peak [%]')
            ymin, ymax = plt.ylim()
            ymin=0
            plt.xlim(xmin, xmax)
            plt.ylim(ymin,ymax*1.1)
            plt.legend(loc='lower left')
            plt.grid()
            pp.savefig()
            plt.clf()

pylab.subplots_adjust(bottom=0.1)

for nCells in nCellsArray:
    for LESModel in LESModelArray:
        for solver in solverArray:
            idxSolver=np.where(data['solver']==solver)
            preArray=np.unique(data['preconditioner'][idxSolver])
            for pre in preArray:
                idx=np.where(
                    (data['nCells']==nCells)
                    & (data['LESModel']==LESModel)
                    & (data['solver']==solver)
                    & (data['preconditioner']==pre)
                    )
                x=data['nProcs'][idx]
                y=data['MFLOPSPEAK'][idx]

                mpi,index0 = np.unique(x, return_index=True)
                index1=index0[1:]
                index1=np.append(index1,len(y))
                MFLOPSPerPeakAve=np.zeros(len(mpi))
                MFLOPSPerPeakSTD=np.zeros(len(mpi))
                for i in range(len(mpi)):
                    MFLOPSPerPeak=y[index0[i]:index1[i]]
                    MFLOPSPerPeakAve[i]=np.average(MFLOPSPerPeak)
                    MFLOPSPerPeakSTD[i]=np.std(MFLOPSPerPeak)

                base=str(nCells)+"cells-"+LESModel+"-"+solver+"-"+pre
                print base

                offset=(mpi[len(mpi)-1]-mpi[0])*0.05
                xmin=mpi[0]-offset
                xmax=mpi[len(mpi)-1]+offset

                plt.title("MFLOPS per peak\n("+
                          str(nCells/1e+6)+"M cells, "+LESModel+" ,"+solver+"-"+pre+")")
                plt.xlabel('Number of MPI processes')
                plt.xticks(mpi)
                plt.grid()
                plt.plot(mpi,MFLOPSPerPeakAve, label="MFLOPS per peak [%]", linewidth=1)
                plt.errorbar(mpi, MFLOPSPerPeakAve, yerr=MFLOPSPerPeakSTD, fmt='.', linewidth=2)
                plt.ylabel('MFLOPS per peak [%]')
                ymin, ymax = plt.ylim()
                ymin=0
                plt.xlim(xmin, xmax)
                plt.ylim(ymin,ymax*1.1)
                plt.legend(loc='upper right')
                pp.savefig()
                plt.clf()

pp.close()