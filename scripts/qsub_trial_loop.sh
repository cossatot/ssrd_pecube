#!/bin/bash

for run in $(cat trial_id_list.txt) ; do
    qsub -v run_id=$run run_pecube_job.pbs
    sleep 10s

done
