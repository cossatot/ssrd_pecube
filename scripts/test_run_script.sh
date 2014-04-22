#!/bin/bash

cd ~eqsarah

job_id = 45LM3

pecube_dir = pecube_temps/$job_id/Pecube




# make temp directory for running Pecube, copy relevant stuff
mkdir pecube_temps/$job_id

mkdir $pecube_dir/data
mkdir $pecube_dir/input
mkdir $pecube_dir/bin
mkdir $pecube_dir/$job_id

cp src/bin/Pecube $pecube_dir/bin
cp src/bin/Pecube/data/*.* $pecube_dir/data/*.*
cp src/bin/Pecube/input/*.* $pecube_dir/input/*.*

# run Pecube
cd $pecube_dir
ipython test_run_pecube.py $job_id


# clean up
cd ~/eqarah
rm -rf $pecube_dir

exit 0
