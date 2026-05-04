import numpy as np
import random
import os

from scipy import stats
import scipy.io

import create_database.mutils as mutils
import create_database.simulation_pulse as simulation_pulse
import create_database.simulation_rfi as simulation_rfi


#path
save_path = '/root'
database_pl = '/database/pl_rfi'

Nb = 40

#parameters
n_time_bins  = 1024
n_freq_bins  = 1024
time_resol = 5e-2 # Time resolution of data (s)
freq_start = 35 # Frequency (MHz) at lower edge of bandpass.
freq_stop = 85 # Frequency (MHz) at upper edge of bandpass.
tot_time = time_resol*n_time_bins # Total duration (ms) of data set.
bandwidth = freq_start - freq_stop # Total bandwidth (MHz) of data set.
chan_bandwidth = (freq_stop - freq_start)*1e3/n_freq_bins # Channel bandwidth (kHz)
# Array of frequencies corresponding to spectral channels.
freq_array = np.linspace(freq_start,freq_stop,n_freq_bins) # MHz
# Array of time stamps for each pixel of the dynamic spectrum.
time_array = np.linspace(0,tot_time,n_time_bins) # ms


#Plusar parameters
#DM
DM_min = 5
DM_max = 40
#snr
pulse_snr_min = 0.01
pulse_snr_max = 20
# parameter pulse
pulse_time_min = 64
pulse_time_max = 64
pulse_time_range = [pulse_time_min, pulse_time_max]
# pulse profile
sigma_min = 0.06
sigma_max = 0.06
amp_min = 0.8
amp_max = 1.0
sigma_range = [sigma_min,sigma_max]
amp_range   = [amp_min,amp_max]
#parameters rfi
nb_rfi_max = 10
#nb rfi
rfi_nb_freq_min = 1
rfi_nb_freq_max = 10
rfi_nb_time_min = 600
rfi_nb_time_max = 1024
rfi_nb = [rfi_nb_freq_min, rfi_nb_freq_max, rfi_nb_time_min, rfi_nb_time_max]
#sl rfi
rfi_sl_freq_min = 600
rfi_sl_freq_max = 1024 
rfi_sl_time_min = 1
rfi_sl_time_max = 10
rfi_sl = [rfi_sl_freq_min, rfi_sl_freq_max, rfi_sl_time_min, rfi_sl_time_max]
#snr
rfi_snr_min = 1
rfi_snr_max = 10
rfi_snr_range = [rfi_snr_min, rfi_snr_max]

isExist = os.path.exists(save_path)
if not isExist: 
    os.makedirs(save_path)
    print('The directory is created!')


for i in range(Nb):
    #generate pulsar
    # DM = random.uniform(DM_min,DM_max)    #need to save
    DM = i+1
    ptc = simulation_pulse.pulse_freq_time(DM, pulse_time_range)  #need to save

    pulse_time_start = ptc[0]
    pulse_time_width = ptc[1]

    para_pulsar, profile = simulation_pulse.pulse_profile2(pulse_time_width, sigma_range, amp_range)
    para_pulsar['DM'] = DM
    para_pulsar['pulse_time_start'] = pulse_time_start
    para_pulsar['pulse_time_width'] = pulse_time_width
    para_pulsar['profile'] = profile
    para_pulsar['t_shift_max'] = ptc[2]
    para_pulsar['t_shitft_min'] = ptc[3]

    t_shift_max = ptc[2]
    pulsar_tem = np.zeros((n_freq_bins, n_time_bins+ pulse_time_width*2 + t_shift_max*2))
    mask = np.zeros((n_freq_bins, n_time_bins+ pulse_time_width*2 + t_shift_max*2))
    snr = np.zeros((n_freq_bins, n_time_bins+ pulse_time_width*2 + t_shift_max*2))
    
    shape  = pulsar_tem.shape
    pulse_time_array = np.linspace(0, shape[1] * time_resol, shape[1])

    pulse_time = np.arange(pulse_time_start,  n_time_bins + pulse_time_width+t_shift_max, pulse_time_width )
    para_pulsar['pulse_time'] = pulse_time

    if pulse_time.any():
    	for pulse_time_index in enumerate(pulse_time):
                pulse_snr = mutils.loguniform(pulse_snr_min,pulse_snr_max,1)
                Z,M,S = simulation_pulse.simulate_pulse2(pulse_snr, DM, profile, pulse_time_array, int(pulse_time_index[1]),pulse_time_width,shape)
                pulsar_tem = pulsar_tem+Z
                mask = mask + M
                snr = snr + S

    pulsar = np.zeros((n_freq_bins,n_time_bins))
    mask_s = np.zeros((n_freq_bins,n_time_bins))       
    pulsar = pulsar_tem[:, pulse_time_width+ t_shift_max: pulse_time_width+ t_shift_max +n_time_bins]
    mask_s = mask[:, pulse_time_width+ t_shift_max: pulse_time_width+ t_shift_max +n_time_bins]
    snr_s = snr[:, pulse_time_width+ t_shift_max: pulse_time_width+ t_shift_max +n_time_bins]
    para_pulsar['mask']=mask_s
    para_pulsar['snr_map'] = snr_s
    
    
    #generate rfi
    rfi1 = simulation_rfi.get_rfi_dim()
    rfi2 = simulation_rfi.get_rfi_dim()
    nb_rfi = random.randint(1, nb_rfi_max)
    for j in range(nb_rfi):
        ftc = simulation_rfi.rfi_information(rfi_nb, rfi_snr_range)
        Z = mutils.gaussian2d(ftc[0],ftc[1],ftc[4])
        rfi1[ftc[2]:ftc[0]+ftc[2], ftc[3]:ftc[1]+ftc[3]] += Z
    
    sl_rfi = random.randint(1, nb_rfi_max)
    for k in range(sl_rfi):
        ftc2 = simulation_rfi.rfi_information(rfi_sl, rfi_snr_range)
        Z = mutils.gaussian2d(ftc[0],ftc[1],ftc[4])
        rfi2[ftc[2]:ftc[0]+ftc[2], ftc[3]:ftc[1]+ftc[3]] += Z
    list = os.listdir(database_pl)
    n = random.randint(0,len(list)-1)
    filename = list[n]
    pl_rfi = scipy.io.loadmat(database_pl + '/' + filename)['mapres']
    rfi = rfi1 + rfi2 + pl_rfi

    noise = np.random.randn(n_freq_bins, n_time_bins)

    data = pulsar + rfi + noise

    #save data
    np.save(os.path.join(save_path,f"data_{i}.npy"), data)
    np.save(os.path.join(save_path,f"pulsar{i}.npy"), pulsar+noise)
    np.save(os.path.join(save_path,f"dic_{i}.npy"), para_pulsar)