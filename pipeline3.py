import numpy as np
import dp3
import argparse
import sys



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
time_loc = data_dir[0] + "/time.npy"
interval_loc = data_dir[0] + "/interval.npy"
phase_center_loc = data_dir[0] + "/phase_center.npy"
flag_loc = data_dir[0] + "/flag.npy"
mask_loc = data_dir[0] + "/rfi_mask.npy"

vis_ms = np.load(vis_loc)
flags_ms = np.load(flag_loc)

chan_freq = np.load(chan_freq_loc)
chan_width = np.load(chan_width_loc)

time = np.load(time_loc)
interval = np.load(interval_loc)
phase_center = np.load(phase_center_loc)[0][0]

rfi_mask = np.load(mask_loc)


# define DPInfo
vis_ms_dims = vis_ms.shape
num_correlations = vis_ms_dims[2]
dpinfo = dp3.DPInfo(num_correlations)
print("number of correlations: " + str(num_correlations)) 
print()


# DPInfo: phase center
dpinfo.phase_center = phase_center
print("phase center: " + str(phase_center))
print()

# DPInfo: antenna information

ant_name = np.load(ant_name_loc)
ant_pos = np.load(ant_pos_loc)
ant_diameter = np.load(ant_diameter_loc)
antenna1 = np.load(antenna1_loc)
antenna2 = np.load(antenna2_loc)
dpinfo.set_antennas(ant_name, ant_diameter, ant_pos, antenna1, antenna2)

num_ants = len(ant_name)
num_baselines = int(num_ants * (num_ants + 1)/2)
num_freqs = len(chan_freq)



# DPInfo: times

first_time = time[0]
last_time = time[-1]
interval = interval[0]
num_times = int(vis_ms.shape[0]/num_baselines)

print("first time:  " + str(first_time))
print("last_time:  " + str(last_time))
print("interval:  " + str(interval))
print()

dpinfo.set_times(first_time, last_time , interval)

# DPInfo: freqeuency information
dpinfo.set_channels(chan_freq, chan_width)


# RFI mask for preflagger

#chan = np.array([])
#for i in range(num_freqs):
#    if rfi_mask[i]:
#       chan = np.append(chan, i)
#print(chan.astype(int))


mychan = np.where(rfi_mask)
chan = mychan[0].tolist()


parset = dp3.parameterset.ParameterSet()

parset.add("preflag.chan", str(chan))
parset.add("average.freqstep", str(8))
parset.add("aoflag.autocorr", str(True))


preflag_step = dp3.make_step("preflag", parset,"preflag.", dp3.MsType.regular)
average_step = dp3.make_step("average", parset, "average.", dp3.MsType.regular)
aoflag_step = dp3.make_step("aoflag", parset, "aoflag.", dp3.MsType.regular)
null_step = dp3.make_step("null", parset, "", dp3.MsType.regular)

preflag_step.set_info(dpinfo)
aoflag_step.set_info(dpinfo)
average_step.set_info(dpinfo)

preflag_step.set_next_step(aoflag_step) 
aoflag_step.set_next_step(average_step)
average_step.set_next_step(null_step)

vis = vis_ms.reshape([num_times, num_baselines, num_freqs, num_correlations])
flags = flags_ms.reshape([num_times, num_baselines, num_freqs, num_correlations])

for time in range(num_times):
    dpbuffer = dp3.DPBuffer()
    dpbuffer.set_flags(flags[time, :, :, :])
    dpbuffer.set_data(vis[time, :, :, :])
    preflag_step.process(dpbuffer)

preflag_step.finish()


output_flags = numpy.zeros((num_times, num_baselines, num_freqs, num_correlations),  numpy.bool8)

for i in numpy.arange(len(num_times)):
        dpbuffer_from_queue = queue_step.queue.get()
        output_flags [i,:,:,:] = numpy.array(dpbuffer_from_queue.get_flags(), copy=False) 

