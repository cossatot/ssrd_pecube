import sys
#import json
import pandas as pd
import pecube_tools as pt


# filenames and arguments
run_id = sys.argv[1]
pecube_dir = sys.argv[2]

print("run_id is", run_id)
input_fault_file = '/home/styron/src/Pecube/input/fault_parameters.ssrd.txt'
input_topo_file = '/home/styron/src/Pecube/input/topo_parameters.ssrd.txt'

output_fault_file = ('{}/input/fault_parameters.txt'.format(pecube_dir) )
output_topo_file = ('{}/input/topo_parameters.txt'.format(pecube_dir) )
print("output_fault_file is", output_fault_file)


# other fixed parameters
fault_list = ['A', 'B']

fault_fld = {'flA' : 47, 'flB' : 78 }     # first lines in fault_params.txt

time_int_dict = {'A' : 4, 'B' : 3}        # number of time intervals per fault

topo_fl = 76                              # thermo line in topo_params.txt


# open pandas df and get run parameters
rp = pd.read_csv('/home/styron/src/Pecube/scripts/run_params_heat_mods.csv',
                  index_col=0)

run_params_dict = rp[rp.run_id == run_id].squeeze().to_dict()

# modify the files
pt.modify_fault_history(run_params_dict, fault_list, fault_fld, time_int_dict,
                        input_fault_file, output_fault_file)

pt.modify_topo_parameters(run_params_dict, topo_fl, 
                          input_topo_file, output_topo_file)
