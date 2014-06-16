#!/bin/bash

for run in $(cat finish_1000_runs.txt) ; do
    qsub -v run_id=$run run_pecube_job.pbs
    sleep 10s

done

logout
