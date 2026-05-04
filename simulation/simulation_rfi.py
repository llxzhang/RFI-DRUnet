import numpy as np
import random

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


def get_rfi_dim():
	return np.zeros((n_freq_bins,n_time_bins))


def rfi_information(parameters, snr_range):
	#parameters = rfi_parameters(category)
	rfi_freq_min = parameters[0]
	rfi_freq_max = parameters[1]
	rfi_time_min = parameters[2]
	rfi_time_max = parameters[3]
	rfi_snr_min = snr_range[0]
	rfi_snr_max = snr_range[1]

	rfi_freq_width = random.randint(rfi_freq_min, rfi_freq_max)
	rfi_time_width = random.randint(rfi_time_min, rfi_time_max)

	rfi_freq_start = random.randint(0, n_freq_bins-rfi_freq_max)
	rfi_time_start = random.randint(0, n_time_bins-rfi_time_max)

	rfi_snr = random.uniform(rfi_snr_min, rfi_snr_max)

	return rfi_freq_width, rfi_time_width, rfi_freq_start, rfi_time_start, rfi_snr

