import numpy as np
import pandas as pd
import pecube_tools as pt
import hashlib

#setup
np.random.seed(69)
run_params_file = 'run_params.csv'

#run info
num_samples = 1e4
min_runs = 1e3

# geological constraints:  Maybe make JSON/other config file?
min_extension = 15
max_extension = 35

ssrd_dip_deg = 15
ssrd_dip_rad = np.radians(ssrd_dip_deg)
ssrd_n_times = 4
ssrd_age_max = 80
ssrd_age_min=5
ssrd_rate_max=10
ssrd_rate_min=0
#ssrd_extension_min = None
#ssrd_extension_max = None

wpf_dip_deg = 40
wpf_dip_rad = np.radians(wpf_dip_deg)
wpf_n_times = 3
wpf_age_max = 40
wpf_age_min=0
wpf_rate_max=2
wpf_rate_min=0
#wpf_extension_min = None
#wpf_extension_max = None

def make_fault_history_df(): # defined here so all variables can be accessed
    ssrd_df=pt.sample_histories(num_samps=num_samples, num_times=ssrd_n_times, 
                                age_max=ssrd_age_max, age_min=ssrd_age_min,
                                rate_max=ssrd_rate_max, rate_min=ssrd_rate_min,
                                zero_to_modern=True)

    ssrd_df['ssrd_extension'] = pt.calc_horiz_fault_strain(ssrd_df,
                                           timesteps=np.arange(ssrd_n_times)+1,
                                           fault='A', fault_dip=ssrd_dip_rad)

    wpf_df = pt.sample_histories(num_samps=num_samples, num_times=wpf_n_times, 
                                 age_max=wpf_age_max, age_min=wpf_age_min,
                                 rate_max=wpf_rate_max, rate_min=wpf_rate_min,
                                 fault='B', zero_to_modern=False)

    wpf_df['wpf_extension'] = pt.calc_horiz_fault_strain(wpf_df,
                                            timesteps=np.arange(wpf_n_times)+1,
                                            fault='B', fault_dip=wpf_dip_rad)


    new_df = pd.concat( [ssrd_df, wpf_df], axis=1)

    new_df['net_extension'] = (new_df.ssrd_extension 
                               + new_df.wpf_extension)
    
    new_df = new_df[(min_extension <= new_df.net_extension)
                          & (max_extension >= new_df.net_extension)
                          & (new_df.ssrd_extension 
                             >= 2 * new_df.wpf_extension)]
    
    return new_df


ssr_history = make_fault_history_df()  # make initial fault history df
ssr_history = ssr_history.reset_index(drop=True)

# iterate until we have enough runs
while len(ssr_history) < min_runs:

    new_df = make_fault_history_df()
    
    ssr_history = pd.concat([ssr_history, new_df], axis=0 )
    ssr_history.reset_index(inplace=True, drop=True)


# make hash functions for jobids
def job_id_hash(row):
    return hashlib.md5( str (np.random.random() ) ).hexdigest()[:5]

ssr_history['job_id'] = ssr_history.apply(job_id_hash, axis=1)

while len(ssr_history.job_id) > len(ssr_history.job_id.unique() ):

    dups = ssr_history.job_id.duplicated()
    
    ssr_history.loc[dups.index, dups] = dups.apply(hash_row2)

ssr_history.to_csv(run_params_file)