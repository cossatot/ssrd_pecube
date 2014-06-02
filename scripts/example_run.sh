#!/bin/bash

 bsub -q compute_medium -o run_pecube_job-%J.out  \
      -e run_pecube_job-%J.err ./run_pecube_job.sh fb7f0
