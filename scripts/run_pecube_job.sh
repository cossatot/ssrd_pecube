#!/bin/bash

cd ~eqsarah

#run_id=7a80c
run_id=$1
pecube_dir=pecube_temps/$run_id/Pecube
script_dir=~eqsarah/src/Pecube/scripts

mkdir -p ssrd_pecube/comparisons

# make temp directory for running Pecube, copy relevant stuff
mkdir -p pecube_temps/$run_id

mkdir -p $pecube_dir/data
mkdir -p $pecube_dir/input
mkdir -p $pecube_dir/bin
mkdir -p $pecube_dir/$run_id

cp -R src/Pecube/bin $pecube_dir
cp -R src/Pecube/data $pecube_dir
cp -R src/Pecube/input $pecube_dir



ipython script_dir/modify_input_files.py $run_id

cd $pecube_dir
bin/Pecube

cp $run_id/Comparison.txt ~eqsarah/ssrd_pecube/comparisons/Comparison.$run_id.txt

ipython script_dir/parse_results.py $run_id

cd ~eqsarah
rm -rf $pecube_dir

exit 0
