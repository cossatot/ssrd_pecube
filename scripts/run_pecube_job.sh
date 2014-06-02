#!/bin/bash
module load mpi/openmpi-1.6
cd ~eqsarah

run_id=$1
pecube_dir=pecube_temps/$run_id/Pecube
script_dir=~/src/Pecube/scripts

mkdir -p ssrd_pecube/comparisons

# make temp directory for running Pecube, copy relevant stuff
mkdir -p pecube_temps/$run_id

mkdir -p $pecube_dir/ssrd1
mkdir -p $pecube_dir/VTK
mkdir -p $pecube_dir/data
mkdir -p $pecube_dir/input
mkdir -p $pecube_dir/bin
mkdir -p $pecube_dir/$run_id

cp -R src/Pecube/bin $pecube_dir
cp -R src/Pecube/data $pecube_dir
cp -R src/Pecube/input $pecube_dir

# Modify fault_parameters.txt with a Python script
ipython $script_dir/modify_input_files.py $run_id

# run Pecube
cd $pecube_dir
bin/Pecube

# copy results to persistent directory
cp ssrd1/Comparison.txt ~/ssrd_pecube/comparisons/Comparison.$run_id.txt

# parse results (not ready yet)
#ipython $script_dir/parse_results.py $run_id

# clean up
cd ~eqsarah
rm -rf $pecube_dir