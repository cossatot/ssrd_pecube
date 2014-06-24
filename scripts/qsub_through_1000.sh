#!/bin/bash

run_ids=($(cat run_id_heat_list.txt))

for run in ${run_ids[@]:1:1000} ; do
    qsub -v run_id=$run run_pecube_job.pbs
    sleep 30s

done
