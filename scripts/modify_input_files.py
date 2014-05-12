import sys
#import json
import pandas as pd
import pecube_tools as pt


# filenames and arguments
run_id = sys.argv[0]

input_fault_file = '~eqsarah/src/pecube/input/fault_parameters.ssrd.txt'

output_fault_file = ('~eqsarah/pecube_temps/{}/Pecube/input/'
                     + 'fault_parameters.txt'.format(run_id) )

input_topo_file = '~eqsarah/src/pecube/input/topo_parameters.ssrd.txt'

output_topo_file = ('~eqsarah/pecube_temps/{}/Pecube/input/'
                     + 'topo_parameters.txt'.format(run_id) )

# other fixed parameters
fault_list = ['A', 'B']

fault_fld = {'flA' : 31, 'flB' : 58 }      # first lines in fault_params.txt

time_int_dict = {'A' : 4, 'B' : 3}         # number of time intervals per fault

topo_fld  = {'run_dir' : 7 }               # first line in topo_params.txt

topo_param_dict = {'run_dir' : {'fl' : 7,
                                'value' : run_id}
                  }

# open pandas df and get run parameters
rp = pd.read_csv('run_params.csv', index_col=0)

run_params_dict = rp[rp.run_id == run_id]

# modify the files
pt.modify_fault_history(run_params_dict, fault_list, fault_fld, time_int_dict,
                        input_fault_file, output_fault_file)

#pt.modify_topo_parameters(topo_param_dict, input_topo_file, output_topo_file)



