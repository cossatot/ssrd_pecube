
import numpy as np
import pandas as pd
import subprocess, shutil


def make_history_df_cols(fault, num_times, param='both'):
    
    time_cols = ['t{}{}'.format(fault, interval) 
                 for interval in (np.arange(num_times+1) + 1)]
    
    rate_cols = ['r{}{}'.format(fault, interval)
                 for interval in (np.arange(num_times) + 1)]
    
    if param=='time':
        return time_cols
    
    elif param=='rate':
        return rate_cols
    
    elif param=='both':
        return time_cols + rate_cols
    

def sample_histories(num_samps=None, num_times=None, age_max=None, 
                     age_min=None, rate_max=None, rate_min=None, 
                     zero_to_modern=False, fault='A'):
    
    time_df = make_time_df(age_min, age_max, num_samps, num_times, fault)
    
    
    rate_df = make_rate_df(rate_min, rate_max, num_samps, num_times,
                           fault, zero_to_modern)
    
    return pd.concat([time_df, rate_df], axis=1)
    
    
def make_time_df(age_min, age_max, num_samps, num_times, fault):
    
    time_array = np.random.uniform(low=age_min, high=age_max,
                                   size=[num_samps, num_times])
    
    time_array = np.fliplr( np.sort(time_array, axis=1) )

    time_array = np.hstack([time_array, np.zeros([num_samps, 1])])
    
    
    time_cols = make_history_df_cols(fault, num_times, 'time')
    
    return pd.DataFrame(data=time_array, columns=time_cols)
    

def make_rate_df(rate_min, rate_max, num_samps, num_times, 
                 fault, zero_to_modern):
    
    rate_array = np.random.uniform(low=rate_min, high=rate_max,
                                   size=[num_samps, num_times])
    
    if zero_to_modern:
        rate_array[:,-1] = 0.
        
    rate_cols = make_history_df_cols(fault, num_times, param='rate')
    
    return pd.DataFrame(data=rate_array, columns=rate_cols)


def calc_net_extension(init, accel, sr1, sr2, fault_dip):
    """
    imports fault slip information and calculates net slip and extension.

    Obsolete, use 'calc_horiz_fault_strain() instead
    """
    slip1 = (init - accel) * sr1
    slip2 = accel * sr2
    net_slip = slip1 + slip2
	
    net_extension = net_slip * np.cos(fault_dip)

    return net_extension
    

def calc_net_shortening(init, accel, sr1, sr2, fault_dip):
    """
    imports fault slip information and calculates net slip and shortening

    Obsolete, use 'calc_horiz_fault_strain()' instead
    """
    slip1 = (init - accel) * sr1 * -1
    slip2 = accel * sr2 * -1
    net_slip = slip1 + slip2
	
    net_shortening = net_slip * np.cos(fault_dip)

    return net_shortening


def calc_horiz_fault_strain(fault_param_dict, timesteps = [1], fault = 'A', 
                            fault_dip = 0):
    slip = 0
    
    fpd = fault_param_dict
                            
    for time_int in timesteps:
        t_int = time_int
        time_1 = fpd[ 't{}{}'.format(fault, t_int) ]
        time_2 = fpd[ 't{}{}'.format(fault, t_int + 1) ]
        rate = fpd[ 'r{}{}'.format(fault, t_int) ]
        
        slip_step = (time_1 - time_2) * rate
        slip = slip + slip_step
    
    horiz_strain = slip * np.cos(fault_dip)
    
    return horiz_strain   
        
        
def modify_fault_history_old(init, accel, sr1, sr2, end = 0, 
                             fault_hist_line_1 = 0, fault_hist_line_2 = 1, 
                             input_file = [], output_file = [], save = True):
    """
    Takes Pecube fault_parameters.txt and modifies the parameters for fault
    slip through time, for a single fault.  Should be run in a loop for each
    fault as necessary.  Currently only for 2 phase histories per fault.  This
    needs to be generalized in the future.
    
    Returns new fault_parameters.txt
    """    
    #slip interval 1
    start_age = '{} '.format(init)
    accel_age = '{} '.format(accel)
    rate_1 = '{} \n'.format(sr1)
    
    #slip interval 2
    accel_age = '{} '.format(accel)
    end_age = '{} '.format(end)
    rate_2 = '{} \n'.format(sr2)
     
    input_file = open(input_file, 'r')
    output_file = open(output_file, 'w+')
    
    start_pt = 0
    line_no = 0
    
    while 1:
        line = input_file.readline()
        
        if not line:
            break
        
        line_no = line_no + 1
        
        if line_no == fault_hist_line_1:
            mod_line = line[:start_pt] + start_age + accel_age + rate_1
            output_file.write(mod_line)
        
        elif line_no == fault_hist_line_2:
            mod_line = line[:start_pt] + accel_age + end_age + rate_2
        
        else:
            output_file.write(line)
    
    input_file.close()
    output_file.close()

    if save == True:
        #shutil.copy(input_file, output_file)
        rename_fault_params_old(input_file, output_file)


def write_fault_hist_lines(fault_line, fault_line_no, input_file, output_file):
    """
    Opens the fault_parameters.txt file and writes a single fault history line,
    called 'fault_line'.
    
    Saves the result each time if asked.
    """ 
    input_file = open(input_file, 'r')
    output_file = open(output_file, 'w+')
    
    start_pt = 0
    line_no = 0    
    
    while 1:
        line = input_file.readline()
        if not line:
            break
        
        line_no = line_no + 1
        
        if line_no == fault_line_no:
            mod_line = line[:start_pt] + fault_line
            output_file.write(mod_line)
        
        else:
            output_file.write(line)

            
    input_file.close()
    output_file.close()

def write_lines(line_string, line_num, input_file, output_file):
    """
    Opens the fault_parameters.txt file and writes a single fault history line,
    called 'fault_line'.
    
    Saves the result each time if asked.
    """ 
    input_file = open(input_file, 'r')
    output_file = open(output_file, 'w+')
    
    start_pt = 0
    line_no = 0    
    
    while 1:
        line = input_file.readline()
        if not line:
            break
        
        line_no = line_no + 1
        
        if line_no == line_num:
            mod_line = line[:start_pt] + line_str
            output_file.write(mod_line)
        
        else:
            output_file.write(line)

            
    input_file.close()
    output_file.close()


def modify_fault_history(fault_params_dict, fault_list, 
                       fault_hist_first_lines_dict, time_int_dict, 
                       input_file = 'file', output_file = 'file'):
    """
    Takes Pecube fault_parameters.txt and modifies the parameters for fault
    slip through time.  Works for all faults at a time.  Needs a dict of fault
    parameters as key:value pairs, e.g. ('tA1':150), and a dict of fault first
    line numbers, e.g. ('flA': 35)
    
    Returns new faut_parameters.txt
    """
    fpd = fault_params_dict    
    fld = fault_hist_first_lines_dict
    
    for fault in fault_list:
        fault_line_no = fld[ 'fl{}'.format(fault) ]
        num_time_intervals = time_int_dict[fault]

        for time_int in range(num_time_intervals):
            
            t_int = time_int + 1
            time_1 = fpd[ 't{}{}'.format(fault, t_int) ]
            time_2 = fpd[ 't{}{}'.format(fault, t_int + 1) ]
            rate = fpd[ 'r{}{}'.format(fault, t_int) ]
            
            fault_line = '{} {} {} \n'.format(time_1, time_2, rate)
            write_fault_hist_lines(fault_line, fault_line_no, input_file,
                                   output_file)
            rename_fault_params_old(input_file, output_file)            
            fault_line_no += 1


def modify_topo_parameters(topo_param_dict, input_file, output_file):
    """
    Modifies Pecube topo_parameters.txt file.

    Takes 'topo_param_dict', a dictionary of parameters, and replaces lines
    containing each para ... blahh...

    Currently just replaces lines, so '
    """
    for param in topo_param_dict.keys:
        line_num = topo_param_dict[param]['fl']
        line_str = topo_param_dict[param]['value'] 

        write_lines(line_str, line_num, input_file, output_file)


def rename_fault_params_old(input_file, output_file):
    """Replaces old input file with new output file via a terminal call"""
    subprocess.call('cp {} {}'.format(output_file, input_file), shell=True)


def save_output():
    pass


def run_pecube_cloud():
    pecube_print = subprocess.check_output(
      'cd /home/picloud/src/Pecube && bin/Pecube', shell=True)
    
    return pecube_print


def run_pecube_local():
    pecube_print = subprocess.check_output(
      'cd /home/itchy/src/Pecube && bin/Pecube', shell = True)    
    
    return pecube_print


def read_comparison(comp_file, index = None, put_nans='no'):
    """Reads in the Pecube output file 'Comparison.txt', names the columns, and
       returns a Pandas dataframe.
       
       If put_nans == 'yes', default null values in Comparison.txt are given 
       numpy NaN values, so they don't screw up plots and statistics.
       
       Returns: pandas dataframe
    """
    
    cols_list = ['lon','lat','elev_obs','elev_calc','aHe_obs','aHe_calc',
                 'aFt_obs','aFt_calc','zHe_obs','zHe_calc','zFt_obs','zFt_calc',
                 'kspAr_obs','kspAr_calc','biAr_obs','biAr_calc','muAr_obs',
                 'muAr_calc','hbAr_obs','hbAr_calc','aFto1','aFto2','aFto3',
                 'aFto4','aFto5','aFto6','aFto7','aFto8','aFto9','aFto10',
                 'aFto11','aFto12','aFto13','aFto14','aFto15','aFto16','aFto17',
                 'aFtc1','aFtc2','aFtc3','aFtc4','aFtc5','aFtc6','aFtc7',
                 'aFtc8','aFtc9','aFtc10','aFtc11','aFtc12','aFtc13','aFtc14',
                 'aFtc15','aFtc16','aFtc17']
    
    col_widths = [12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12,
                  12, 12, 12, 12, 12, 12, 12, 12, 12,12, 12, 12, 12, 12, 12, 12,
                  12, 12, 12, 12, 12, 12, 12, 12, 12,12, 12, 12, 12, 12, 12, 12,
                  12, 12, 12, 12, 12, 12, 12]
                  
    comp = pd.read_fwf(comp_file, widths = col_widths, skiprows = 1,
                       names = cols_list)
    
    if index != None:
        comp = comp.set_index(index)
    
    if put_nans=='yes':
        comp[comp == -9999.0000] = np.nan
        comp[comp == -1.0000] = np.nan
    
    return comp


def read_thermo_data(thermo_file, index = None, put_nans='no'):
    """Reads in a Pecube thermo data file, names the columns, and returns a
       Pandas dataframe
       
       If put_nans == 'yes', default null values in Comparison.txt are given 
       numpy NaN values, so they don't screw up plots and statistics.
       
       Returns: pandas dataframe
    """
    
    cols_list = ['lon','lat','elev','aHe_obs','aHe_err','aFt_obs',
                 'aFt_err','zHe_obs','zHe_err','zFt_obs','zFt_err',
                 'kspAr_obs','kspAr_err','biAr_obs','biAr_err','muAr_obs',
                 'muAr_err','hbAr_obs','hbAr_err','aFto1','aFto2','aFto3',
                 'aFto4','aFto5','aFto6','aFto7','aFto8','aFto9','aFto10',
                 'aFto11','aFto12','aFto13','aFto14','aFto15','aFto16','aFto17',
                 'aFtc1','aFtc2','aFtc3','aFtc4','aFtc5','aFtc6','aFtc7',
                 'aFtc8','aFtc9','aFtc10','aFtc11','aFtc12','aFtc13','aFtc14',
                 'aFtc15','aFtc16','aFtc17']
           
    thermo = pd.read_table(thermo_file, skiprows = 1, names = cols_list)
    
    if index != None:
        thermo = thermo.set_index(index)
    
    if put_nans=='yes':
        thermo[thermo == -9999.0000] = np.nan
        thermo[thermo == -1.0000] = np.nan
    
    return thermo


def make_time_vector(start_time = 150., stop_time = 0., time_step_Ma = 0.01,
                     decimals = 3):
    """Makes a vector of dates in the past.  Default is time range from 20 Ma
        to 0 Ma (present) with a 10 ky time step.  Also round to specified deci-
        mals to avoid problems with floating point errors when endexing, default
        = 3.  For shorter time steps, this should be changed.
        
        Returns a time vector (nd array)"""
    
    # make sure args are floats
    start_time = np.float(start_time)
    stop_time = np.float(stop_time)
    step_time = np.float(time_step_Ma)
    
    # Make vector of times (Ma)
    num = ( (start_time - stop_time) / time_step_Ma) + 1
    time_vector = np.linspace(start_time, stop_time, num = num)
    
    # Rounds to specified precision
    time_vector = np.around(time_vector, decimals = decimals)
    
    return time_vector


def calc_horiz_strain_history(fault_param_dict, timesteps = [1], fault = 'A',
                              fault_dip = 0, time_step_Ma = 1, start_time =
                              None, stop_time = 0, time_vector = None):
    """ Takes a dictionary with fault slip history information, formatted
        similarly to the Pecube input one, and returns a vector of fault
        slip rates through time at specified intervals.
        
        Note that start_time and stop_time are in the past, where start is
        older and therefore a larger number than stop time.  This is the
        opposite of in the numpy arange function used."""
    
    fpd = fault_param_dict
    
    if start_time == None:
        start_num = min(timesteps)
        start_time = fpd[ 't{}{}'.format( fault, start_num) ]
    
    if stop_time != 0:
        stop_num = min(timesteps)
        stop_time = fpd[ 't{}{}'.format( fault, stop_num) ]
    
    # make time vector, which is basically an index for rate and cum rate vecs
    time_vector = make_time_vector(start_time = start_time, stop_time =
                                   stop_time, time_step_Ma = time_step_Ma)
    
    #
    slip_rate_w_time = np.zeros( len( time_vector) )
    
    for time_int in timesteps:
        t_int = time_int
        time_1 = fpd[ 't{}{}'.format(fault, t_int) ]
        time_2 = fpd[ 't{}{}'.format(fault, t_int + 1) ]
        rate = fpd[ 'r{}{}'.format(fault, t_int) ]
        
        t1_index = np.where(time_vector == time_1)
        t2_index = np.where(time_vector == time_2)
        
        t1_index = t1_index[0]
        t2_index = t2_index[0] + 1
        
        slip_rate_w_time[t1_index : t2_index] = rate
    horiz_strain_w_time = slip_rate_w_time * np.cos(fault_dip)
    
    return horiz_strain_w_time
