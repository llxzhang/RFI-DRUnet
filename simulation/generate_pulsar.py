import numpy as np
import random
import os

from scipy import stats
import scipy.io

import mutils
import simulation_pulse

#path
pulsar_path = '/root'

Nb = 10

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

#DM
DM_min = 5
DM_max = 40

#snr
pulse_snr_min = 0.01
pulse_snr_max = 20

# parameter pulse
pulse_time_min = 40
pulse_time_max = 100
pulse_time_range = [pulse_time_min, pulse_time_max]

# pulse profile

sigma_min = 0.01
sigma_max = 0.04

amp_min = 0.2
amp_max = 1.0

sigma_range = [sigma_min,sigma_max]
amp_range   = [amp_min,amp_max]


isExist = os.path.exists(pulsar_path)
if not isExist:
	os.makedirs(pulsar_path)
	print('The directory is created!')



for i in range(Nb):
	#generate pulsar signal
	DM  = random.randint(DM_min, DM_max)
	ptc = simulation_pulse.pulse_freq_time(DM, pulse_time_range)

	pulse_time_start = ptc[0]
	pulse_time_width = ptc[1]
	
	profile = simulation_pulse.pulse_profile(pulse_time_width, sigma_range, amp_range)
	t_shift_max = ptc[2]

	pulsar_tem = np.zeros((n_freq_bins, n_time_bins+ pulse_time_width*2 + t_shift_max*2))
	shape  = pulsar_tem.shape
	pulse_time_array = np.linspace(0, shape[1] * time_resol, shape[1])

	pulse_time = np.arange(pulse_time_start,  n_time_bins + pulse_time_width+t_shift_max, pulse_time_width )

	if pulse_time.any():
		for pulse_time_index in enumerate(pulse_time):
			pulse_snr = mutils.loguniform(pulse_snr_min,pulse_snr_max,1)
			Z = simulation_pulse.simulate_pulse(pulse_snr, DM, profile, pulse_time_array, int(pulse_time_index[1]),pulse_time_width,shape)
			pulsar_tem = pulsar_tem+Z

	pulsar = np.zeros((n_freq_bins,n_time_bins))       
	pulsar = pulsar_tem[:, pulse_time_width+ t_shift_max: pulse_time_width+ t_shift_max +n_time_bins]  

	np.save(os.path.join(pulsar_path,f'pulsar_{i}'), pulsar)

print("pulsar generation fini")