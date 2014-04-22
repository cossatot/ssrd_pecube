import sys
import pandas as pd
import numpy as np
import json
#sys.path.append('../scripts/python/')
import pecube_tools as pt


# filenames and arguments
job_id = sys.argv[0]
input_fault_file = 'file'
output_fault_file = 'file'
input_topo_file = 'file'
output_topo_file = 'file'

comparison_df_file = '~eqsarah/ssrd_runs/{}_comparison_df.csv'.format(job_id)
master_comp_df = '~eqsarah/ssrd_runs/master_df.csv'

run_params_dir = '../job_files/{}/'.format(job_id)


run_params_file = run_params_dir + '{}_params.json'.format(job_id)
comparison_file = 'PATH/Comparison.txt'

fault_first_lines_file = 'PATH/fault_first_lines.json'
topo_first_lines_file = 'PATH/topo_first_lines.json'


with open(run_params_file, 'r') as f:
    run_params = json.load(f)

with open(fault_first_lines_file, 'r') as fl:
    fault_fld = json.load(fl)

with open(topo_first_lines_file, 'r') as fl:
    topo_fld = json.load(fl)

fault_list = ['A', 'B']




# run the shit
pt.modify_fault_history(run_params, fault_list, fault_fld, 
                        num_time_intervals=1, input_file = input_fault_file, 
                        output_file = output_fault_file)

pt.modify_topo_file(run_params, topo_p_list, topo_fld,
                    input_file = input_topo_file, 
                    output_file = output_topo_file)

pt.run_pecube()

comp_df = pt.read_comparison(comparison_file)

comp_df.to_csv(comparison_df_file)

master_df = pd.read_csv(master_comp_df, index_col=0)

master_df.append(comp_df)

master_df.to_csv(master_comp_df)


