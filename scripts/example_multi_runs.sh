#!/bin/bash

 bsub -q compute_medium -o run_pecube_job-%J.out  \
      -e run_pecube_job-%J.err ./run_pecube_job.sh fb7f0

 bsub -q compute_medium -o run_pecube_job-%J.out  \
      -e run_pecube_job-%J.err ./run_pecube_job.sh b0889

 bsub -q compute_medium -o run_pecube_job-%J.out  \
      -e run_pecube_job-%J.err ./run_pecube_job.sh 569ed

 bsub -q compute_medium -o run_pecube_job-%J.out  \
      -e run_pecube_job-%J.err ./run_pecube_job.sh 72abc

 bsub -q compute_medium -o run_pecube_job-%J.out  \
      -e run_pecube_job-%J.err ./run_pecube_job.sh ace83
