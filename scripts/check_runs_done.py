import os

comp_file_list = os.listdir('/home/styron/pecube_runs/comparisons/')
comp_list = [c.split('.')[1] for c in comp_file_list]

run_list = [line.strip() for line in open('run_id_list.txt', 'r')]

didnt_run = set(run_list) - set(comp_list)
ran = set(run_list) & set(comp_list)

with open('ran_list.txt', 'w') as f:
    for run in ran:
        print>>f, run

with open('not_run_list.txt', 'w') as f:
    for run in didnt_run:
        print>>f, run

