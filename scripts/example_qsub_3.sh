#!/bin/bash

for run in 26dea 9467d 60cd9; do
    qsub -v run_id=$run run_pecube_job.pbs
    sleep 10s

done

