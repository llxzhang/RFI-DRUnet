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

# parameter pulse
# pulse_time_min = 100
# pulse_time_max = 200

# pulse_snr_min = 0.01
# pulse_snr_max = 20

## pulse profile

# sigma_min = 0.01
# sigma_max = 0.04

# amp_min = 0.2
# amp_max = 1.0

# sigma_range = [sigma_min,sigma_max]
# amp_range   = [amp_min,amp_max]


# pulsar full 
def pulse_freq_time(DM, pulse_time_range):
    t_shift_max = int(4148.79* DM * np.power(freq_array[0],-2)//time_resol)

    t_shift_min = int(4148.79* DM * np.power(freq_array[-1],-2)//time_resol)

    pulse_time_width = random.randint(pulse_time_range[0], pulse_time_range[1])
    # pulse_time_start = random.randint(0, pulse_time_width + t_shift_max)
    pulse_time_start = random.randint(0, pulse_time_width)    
    return(pulse_time_start, pulse_time_width, t_shift_max, t_shift_min)

# have pulsar
def pulse_freq_time2(DM, pulse_time_range):
    t_shift_max = int(4148.79* DM * np.power(freq_array[0],-2)//time_resol)

    t_shift_min = int(4148.79* DM * np.power(freq_array[-1],-2)//time_resol)

    pulse_time_width = random.randint(pulse_time_range[0], pulse_time_range[1])
    pulse_time_start = random.randint(0, pulse_time_width + t_shift_max)
    # pulse_time_start = random.randint(0, pulse_time_width)    
    return(pulse_time_start, pulse_time_width, t_shift_max, t_shift_min)

def pulse_profile(pluse_time_width, sigma_range, amp_range):
    
    phases = np.linspace(0,1, pluse_time_width)
    ndim = random.randint(1,2)
    pos = np.random.uniform(0.1,0.9,ndim)
    
    widths = np.random.uniform(sigma_range[0], sigma_range[1],ndim)
    
    amps = np.random.uniform(amp_range[0],amp_range[1] ,ndim)
    
    prof = (amps[:, np.newaxis] * np.exp(-0.5 * ((phases[np.newaxis,:]
                                         -pos[:,np.newaxis])
                                         /widths[:,np.newaxis])**2))
    return np.sum(prof, axis=0)

def simulate_pulse(snr, DM, profile, pulse_time_array, pulse_time_start, pulse_time_width, shape):
	
    X = freq_array
    Y = pulse_time_array[pulse_time_start: pulse_time_start + pulse_time_width]
    Z = np.zeros(shape)
    M = np.zeros(shape)

    profile = snr * profile
    for i in range(n_freq_bins):
        f = X[i]
        t_shift = int(4148.79* DM * np.power(f,-2)//time_resol)
        
        Z[i, pulse_time_start + t_shift : pulse_time_start+pulse_time_width+t_shift] =  profile
        M[i, pulse_time_start + t_shift] = 1
    return Z


def simulate_pulse2(snr, DM, profile, pulse_time_array, pulse_time_start, pulse_time_width, shape):
	
    X = freq_array
    Y = pulse_time_array[pulse_time_start: pulse_time_start + pulse_time_width]
    Z = np.zeros(shape)
    M = np.zeros(shape)
    S = np.zeros(shape)

    profile = snr * profile
    for i in range(n_freq_bins):
        f = X[i]
        t_shift = int(4148.79* DM * np.power(f,-2)//time_resol)
        
        Z[i, pulse_time_start + t_shift : pulse_time_start+pulse_time_width+t_shift] =  profile
        M[i, pulse_time_start + t_shift] = 1
        S[i, pulse_time_start + t_shift] =  snr
    return Z,M,S



#for evualation toas
def pulse_profile2(pluse_time_width, sigma_range, amp_range):
    info = {}
    phases = np.linspace(0,1, pluse_time_width)
    #ndim = random.randint(1,2)
    ndim =1
    pos = np.random.uniform(0.25,0.75,ndim)
    
    widths = np.random.uniform(sigma_range[0], sigma_range[1],ndim)
    
    amps = np.random.uniform(amp_range[0],amp_range[1] ,ndim)
    
    prof = (amps[:, np.newaxis] * np.exp(-0.5 * ((phases[np.newaxis,:]
                                         -pos[:,np.newaxis])
                                         /widths[:,np.newaxis])**2))
    info['ndim'] = ndim
    info['pos'] = pos
    info['widths'] = widths
    info['amps'] = amps
    
    return info, np.sum(prof, axis=0)