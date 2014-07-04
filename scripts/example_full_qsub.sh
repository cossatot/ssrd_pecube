#!/bin/bash

qsub -q compute -v run_id=fb7f0 run_pecube_job.pbs
qsub -q compute -v run_id=b0889 run_pecube_job.pbs
qsub -q compute -v run_id=569ed run_pecube_job.pbs
