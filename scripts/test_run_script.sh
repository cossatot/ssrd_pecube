#!/bin/bash

cd ~eqsarah

job_id=TEST1
pecube_dir=pecube_temps/$job_id/Pecube

mkdir -p ssrd_pecube/comparisons

# make temp directory for running Pecube, copy relevant stuff
mkdir -p pecube_temps/$job_id

mkdir -p $pecube_dir/data
mkdir -p $pecube_dir/input
mkdir -p $pecube_dir/bin
mkdir -p $pecube_dir/$job_id

cp -R src/Pecube/bin $pecube_dir
cp -R src/Pecube/data $pecube_dir
cp -R src/Pecube/input $pecube_dir

# run Pecube
cd $pecube_dir
#ipython test_run_pecube.py $job_id
bin/Pecube

cp $job_id/Comparison.txt ~eqsarah/ssrd_pecube/comparisons/Comparison.$job_id.txt

# clean up
cd ~eqsarah
rm -rf $pecube_dir

exit 0
