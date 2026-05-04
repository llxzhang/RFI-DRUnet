import numpy as np

Extensions = ['.npy', '.mat']


def is_read_file(filename):
    return ant(filename.endswith(extension) for extension in Extensions)


# Simulate Gaussian random noise with zero mean and unit variance.
def noise_std_normal(n_freq_bins,n_time_bins):
	noise = np.random.randn(n_freq_bins,n_time_bins)
	return noise


# Sample from a log-uniform distribution.
def loguniform(low_limit,high_limit,n_samples):
	log_low_limit = np.log(low_limit)
	log_high_limit = np.log(high_limit)
	log_samples = np.random.uniform(log_low_limit,log_high_limit,n_samples)
	samples = np.exp(log_samples)
	return samples

def is_in_extension(filename,Extension):
	return any(filename.endswith(extension) for extension in Extension)


def gaussian2d(freq, time, amp):
    Z =np.zeros((freq,time))
    tc = time/2
    fc = freq/2
    freqa = np.arange(freq)
    timea = np.arange(time)
    for i in range(freq):
        f = freqa[i]
        for j in range(time):
            t = timea[j]
            #Z[i,j] = amp*np.exp(-0.5*((t-tc)/(time*sigmat))**4)*np.exp(-0.5*((f-fc)/(freq*sigmaf))**2)
            Z[i,j] = amp*np.exp(-0.5*((t-tc)/(time))**2)*np.exp(-0.5*((f-fc)/(freq))**2)
    return Z