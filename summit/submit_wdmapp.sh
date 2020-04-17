#!/bin/bash
#BSUB -nnodes 8
#BSUB -P fus123
#BSUB -W 00:10     # wallclock time
#BSUB -o wdmapp.%J # stdout/stderr goes here

export HDF5_USE_FILE_LOCKING=FALSE
#export SstVerbose=1

mkdir -p coupling
rm -rf coupling/*
mkdir -p GENE/out
mkdir -p XGC/restart_dir

# For whatever reason, if compiling the codes by hand (or using `spack setup`),
# they don't get RPATH set correctly, so won't find libgfortran.so.5 unless we
# load the corresponding gcc module
module load gcc/8.1.1

cd GENE
#jsrun -e prepended -n 16 /ccs/home/kaig1/proj-fus123/kaig1/gene-dev/build-spack/src/gene &
jsrun -e prepended -n 16 $(spack location -i gene@cuth_ecp_2 +adios2 +futils +pfunit +read_xgc +diag_planes +couple_xgc)/bin/gene &

cd ../XGC
#jsrun -e prepended -n 256 /ccs/home/kaig1/proj-fus123/kaig1/xgc1/build-spack-coupling/xgc-es &
jsrun -e prepended -n 256 $(spack location -i xgc1 +coupling_core_edge +coupling_core_edge_field +coupling_core_edge_varpi2)/bin/xgc-es &

wait
