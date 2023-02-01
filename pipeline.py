import numpy as np
import dp3
import argparse


parser = argparse.ArgumentParser(description='extracted data location')
parser.add_argument('--dataloc', type=str, nargs=1, help='the location of data files')
parser.add_argument('--maskloc', type=str, nargs=1, help='the location of RFI mask file')
args = parser.parse_args()
data_dir = args.dataloc
mask_loc = args.maskloc

parset = dp3.parameterset.ParameterSet()

parset.add("freqstep", 8)


vis_loc = data_dir[0] + "/vis.npy"
chan_freq_loc = data_dir[0] + "/chan_freq.npy"
chan_width_loc = data_dir[0] + "/chan_width.npy"
ant_name_loc = data_dir[0] + "/ant_name.npy"
ant_pos_loc = data_dir[0] + "/ant_pos.npy"
ant_diameter_loc = data_dir[0] + "/ant_diameter.npy"
antenna1_loc = data_dir[0] + "/antenna1.npy"
antenna2_loc = data_dir[0] + "/antenna2.npy"
uvw_loc = data_dir[0] + "/uvw.npy"
flag_loc = data_dir[0] + "/flag.npy"


vis = np.load(vis_loc)
vis_dims = vis.shape

chan_freq = np.load(chan_freq_loc)
chan_width = np.load(chan_width_loc)



print(vis_dims)

num_correlations = vis_dims[2] 



dpinfo = dp3.DPInfo(num_correlations)

dpinfo.set_channels(chan_freq, chan_width)
print("frequencies: ", dpinfo.channel_frequencies)
print("widths: ", dpinfo.channel_widths)


ant_name = np.load(ant_name_loc)
ant_pos = np.load(ant_pos_loc)
ant_diameter = np.load(ant_diameter_loc)
antenna1 = np.load(antenna1_loc)
antenna2 = np.load(antenna2_loc)

dpinfo.set_antennas(ant_name, ant_diameter, ant_pos, antenna1, antenna2)

print(dpinfo.antenna_names)
print(dpinfo.antenna_positions)

