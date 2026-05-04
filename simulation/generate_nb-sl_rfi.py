import numpy as np
import random
import os
import matplotlib.pyplot as plt
from scipy import stats
import scipy.io
import argparse


import mutils
import simulation_rfi


parser = argparse.ArgumentParser(description = 'case rfi to generate')
parser.add_argument('rfi', type = str, default = None)
parser.add_argument('number', type =int, default = 20)
args= parser.parse_args()


#path
root = '/root'
output_path = os.path.join(root, args.rfi+'_rfi')

isExist = os.path.exists(output_path)
if not isExist:
	os.makedirs(output_path)
	print('The directory is created!')

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
if args.rfi == 'nb':
	rfi_para = rfi_nb
elif args.rfi == 'sl':
	rfi_para = rfi_sl

nb_rfi_max = 10

for i in range(args.number):
	rfi = simulation_rfi.get_rfi_dim()
	nb_rfi = random.randint(1, nb_rfi_max)
	for j in range(nb_rfi):
		ftc = simulation_rfi.rfi_information(rfi_para, rfi_snr_range)
	
		Z = mutils.gaussian2d(ftc[0],ftc[1],ftc[4])

		rfi[ftc[2]:ftc[0]+ftc[2], ftc[3]:ftc[1]+ftc[3]] += Z

	np.save(os.path.join(output_path, f'rfi_{args.rfi}_{i}') ,rfi)