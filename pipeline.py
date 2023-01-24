import numpy as np
import dp3
import argparse


parser = argparse.ArgumentParser(description='extracted data location')
parser.add_argument('--dataloc', type=str, nargs=1, help='the location of data files')
args = parser.parse_args()
data_dir = args.dataloc

vis_loc = data_dir[0] + "/vis.npy"
chan_freq_loc = data_dir[0] + "/chan_freq.npy"
chan_width_loc = data_dir[0]+"/chan_width.npy"

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

