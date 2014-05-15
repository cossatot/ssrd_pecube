import sys
import pandas as pd
import pecube_tools as pt
from os.path import expanduser

run_id = sys.argv[0]

comparison_file = expanduser( '~eqsarah/ssrd_pecube/comparison/' 
                             +'Comparison.{}.txt'.format(run_id) )

comparison_df_file = expanduser( '~eqsarah/ssrd_runs/'
                                +'{}_comparison_df.csv'.format(job_id) )

master_comp_df = expanduser( '~eqsarah/ssrd_runs/master_df.csv' )

# open pandas df and get run parameters
rp = pd.read_csv('run_params.csv', index_col=0)

run_params_dict = rp[rp.run_id == run_id]

master_df = pd.read_csv(master_comp_df) #index_col ?
# go to work on results

comp_df = pt.read_comparison(comparison_file)


# reshape df
'''
cols = comp_df.columns()
samples = comp_df.index

series_cols = [sample + col for sample in samples for col in cols]
'''



# save results
master_df.append(comp_df)

master_df.to_csv(master_comp_df)
