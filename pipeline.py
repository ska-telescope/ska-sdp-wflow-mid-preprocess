import numpy as np
import dp3
import argparse

parser = argparse.ArgumentParser(description='extracted data location')
parser.add_argument('--dataloc', type=str, nargs=1, help='the location of data files')


args = parser.parse_args()

data_dir = args.dataloc

parset = dp3.parameterset.ParameterSet()

parset.add("freqstep", str(8))


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
mask_loc = data_dir[0] + "/rfi_mask.npy"


vis_ms = np.load(vis_loc)
flags_ms = np.load(flag_loc)



chan_freq = np.load(chan_freq_loc)
chan_width = np.load(chan_width_loc)

vis_ms_dims = vis_ms.shape
print(vis_ms_dims)

num_correlations = vis_ms_dims[2] 



dpinfo = dp3.DPInfo(num_correlations)

dpinfo.set_channels(chan_freq, chan_width)


ant_name = np.load(ant_name_loc)
ant_pos = np.load(ant_pos_loc)
ant_diameter = np.load(ant_diameter_loc)
antenna1 = np.load(antenna1_loc)
antenna2 = np.load(antenna2_loc)
num_ants = len(ant_name)
num_baselines = int(num_ants * (num_ants + 1)/2)
num_freqs = len(chan_freq)
num_times = int(vis_ms.shape[0]/num_baselines)
print(num_times)

rfi_mask = np.load(mask_loc)
chan = np.array([])

vis = vis_ms.reshape([num_times, num_baselines, num_freqs, num_correlations])
flags = flags_ms.reshape([num_times, num_baselines, num_freqs, num_correlations])

for freq in range(num_freqs):
    if rfi_mask[freq]:
       chan = np.append(chan, freq)


parset.add("preflagger.chan", str(chan))


dpinfo.set_antennas(ant_name, ant_diameter, ant_pos, antenna1, antenna2)

preflagger_step = dp3.make_step("preflagger", parset,"preflagger.", dp3.MsType.regular)
#aoflagger_step = dp3.make_step("aoflagger", parset, "aoflagger.", dp3.MsType.regular)
#averaging_step = dp3.make_step("averaging", parset, "averaging.", dp3.MsType.regular)
#null_step = dp3.make_step("null", parset, "", dp3.MsType.regular)

#preflagger_step.set_next_step(aoflagger_step)
#aoflagger_step.set_next_step(null_step)

#preflagger_step.set_next_step(aoflagger_step)
#aoflagger_step.set_next_step(averaging_step)

 
def flags_ratio(flags):
    tot = flags.shape[0] * flags.shape[1] * flags.shape[2]  
    flag_sum = np.sum(np.sum(np.sum(np.sum(flags))))
    return 100 * (flag_sum/tot)

for time in range(num_times):
    dpbuffer = dp3.DPBuffer()
    print(flags_ratio(flags[time, :, :, :]))
    dpbuffer.set_flags(flags[time, :, :, :])
    preflagger_step.process(dpbuffer)
    myflags = dpbuffer.get_flags()

preflagger_step.finish()









