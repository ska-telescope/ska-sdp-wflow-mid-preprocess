import numpy as np
import dp3
import argparse
import sys
import ms_operations



parser = argparse.ArgumentParser(description='pipeline settings')
parser.add_argument('--msloc', type=str, nargs=1, help='location of the measurementset')
parser.add_argument('--maskloc', type=str, nargs=1, help='location of the RFI mask file')

args = parser.parse_args()

data_dir = args.msloc
mask_loc = args.maskloc

parset = dp3.parameterset.ParameterSet()

parset.add("freqstep", str(8))


measurementSet = ms_operations.ReadMS(msFileName)

vis_ms = measurementSet.GetMainTableData('DATA')
flags_ms = measurementSet.GetMainTableData('FLAG')

chan_freq = measurementSet.GetFreqTableData('CHAN_FREQ')[0]
chan_width = measurementSet.GetFreqTableData('CHAN_WIDTH')[0]

time = measurementSet.GetMainTableData('TIME')
interval = measurementSet.GetMainTableData('INTERVAL')
phase_center = measurementSet.GetFieldTableData('PHASE_DIR')

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

ant_name = measurementSet.GetAntennaTableData('NAME')
ant_pos  = measurementSet.GetAntennaTableData('POSITION')
ant_diameter = measurementSet.GetAntennaTableData('DISH_DIAMETER')
antenna1 = measurementSet.GetMainTableData('ANTENNA1')
antenna2 = measurementSet.GetMainTableData('ANTENNA2')
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

rfi_file = open(mask_loc[0], "rb")
rfi_mask = pickle.load(rfi_file)

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

