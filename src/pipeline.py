import numpy as np
import dp3
import argparse
import sys
import ms_operations
import pickle
from dp3 import steps

parser = argparse.ArgumentParser(description='pipeline settings')
parser.add_argument('--msloc', type=str, nargs=1, help='location of the measurementset')
parser.add_argument('--maskloc', type=str, nargs=1, help='location of the RFI mask file')
parser.add_argument('--outloc', type=str, nargs=1, help='location of output')

args = parser.parse_args()

ms_loc = args.msloc
mask_loc = args.maskloc
output_loc = args.outloc

parset = dp3.parameterset.ParameterSet()

parset.add("freqstep", str(8))


measurementSet = ms_operations.ReadMS(ms_loc)

vis_ms = measurementSet.GetMainTableData('DATA')
flags_ms = measurementSet.GetMainTableData('FLAG')

chan_freq = measurementSet.GetFreqTableData('CHAN_FREQ')[0]
chan_width = measurementSet.GetFreqTableData('CHAN_WIDTH')[0]

time = measurementSet.GetMainTableData('TIME')
interval = measurementSet.GetMainTableData('INTERVAL')
phase_center = measurementSet.GetFieldTableData('PHASE_DIR')


# define DPInfo
vis_ms_dims = vis_ms.shape
num_correlations = vis_ms_dims[2]
dpinfo = dp3.DPInfo(num_correlations)
print("number of correlations: " + str(num_correlations)) 
print()


# DPInfo: phase center
#dpinfo.phase_center = phase_center
print("phase center: " + str(phase_center))
print()

# DPInfo: antenna information

ant_name = measurementSet.GetAntennaTableData('NAME')
ant_pos  = measurementSet.GetAntennaTableData('POSITION')
ant_diameter = measurementSet.GetAntennaTableData('DISH_DIAMETER')
antenna1 = measurementSet.GetMainTableData('ANTENNA1')
antenna2 = measurementSet.GetMainTableData('ANTENNA2')

num_ants = len(ant_name)
num_baselines = int(num_ants * (num_ants + 1)/2)
num_freqs = len(chan_freq)


dpinfo.set_antennas(ant_name, ant_diameter, ant_pos, antenna1[0: num_baselines], antenna2[0: num_baselines])

scan_num = measurementSet.GetMainTableData('SCAN_NUMBER')
field_id = measurementSet.GetMainTableData('FIELD_ID')

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
print(chan_freq)
print(chan_width)
dpinfo.set_channels(chan_freq, chan_width)


# RFI mask for preflagger

rfi_file = open(mask_loc[0], "rb")
rfi_mask = pickle.load(rfi_file)

mychan = np.where(rfi_mask)
chan = mychan[0].tolist()
parset = dp3.parameterset.ParameterSet()

weights = np.ones([num_times, num_baselines, num_freqs, num_correlations], dtype="float32")



#print(str(chan))

parset.add("preflag.chan", str(chan))
parset.add("average.freqstep", str(8))
parset.add("aoflag.autocorr", str(True))


preflag_step = dp3.make_step("preflag", parset,"preflag.", dp3.MsType.regular)
average_step = dp3.make_step("average", parset, "average.", dp3.MsType.regular)
aoflag_step = dp3.make_step("aoflag", parset, "aoflag.", dp3.MsType.regular)
null_step = dp3.make_step("null", parset, "", dp3.MsType.regular)

queue_step = steps.QueueOutput(parset, "")
#queue_step.set_info(dpinfo)

#preflag_step.set_info(dpinfo)
#aoflag_step.set_info(dpinfo)
#average_step.set_info(dpinfo)

preflag_step.set_next_step(aoflag_step) 
aoflag_step.set_next_step(average_step)
average_step.set_next_step(queue_step)

preflag_step.set_info(dpinfo)


vis = vis_ms.reshape([num_times, num_baselines, num_freqs, num_correlations])
#flags = flags_ms.reshape([num_times, num_baselines, num_freqs, num_correlations])
flags = np.zeros([num_times, num_baselines, num_freqs, num_correlations], dtype=bool)

for t in range(num_times):
    print(t)
    dpbuffer = dp3.DPBuffer()
    dpbuffer.set_weights(weights[t, :, :, :])
    dpbuffer.set_flags(flags[t, :, :, :])
    dpbuffer.set_data(vis[t, :, :, :])
    preflag_step.process(dpbuffer)

preflag_step.finish()

output_flags = np.zeros((num_times, num_baselines, int(num_freqs/8), num_correlations),  np.bool8)

for i in range(num_times):
        print(i)
        dpbuffer_from_queue = queue_step.queue.get()
        output_flags [i,:,:,:] = np.array(dpbuffer_from_queue.get_flags(), copy=False) 





out_vis_loc = output_loc[0] + "/vis.npy"
out_old_flg_loc = output_loc[0] + "/old_flags.npy"
out_new_flg_loc = output_loc[0] + "/new_flags.npy"
ant1 = output_loc[0] + "/antenna1.npy"
ant2 = output_loc[0] + "/antenna2.npy"
fld_id = output_loc[0] + "/field_id.npy"
sc_num = output_loc[0] + "/scan_number.npy"

field_id2 = field_id.reshape(num_times, num_baselines)
scan_num2 = scan_num.reshape(num_times, num_baselines)

np.save(out_vis_loc, vis)
np.save(out_old_flg_loc, flags)
np.save(out_new_flg_loc,  output_flags)
np.save(ant1, antenna1)
np.save(ant2, antenna2)
np.save(fld_id, field_id2)
np.save(sc_num, scan_num2)
