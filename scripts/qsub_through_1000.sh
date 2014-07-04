#!/bin/bash

run_ids=($(cat run_id_heat_list.txt))

for run in ${run_ids[@]:2000:100001} ; do
    qsub -v run_id=$run run_pecube_job.pbs
    sleep 60s

done
