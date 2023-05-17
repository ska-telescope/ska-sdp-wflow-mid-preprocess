import numpy as np
import dp3
import argparse
import sys
import ms_operations
import pickle
import json
from dp3 import steps

parser = argparse.ArgumentParser(description='pipeline settings')
parser.add_argument('--msloc', type=str, nargs=1, help='location of the measurementset')
parser.add_argument('--maskloc', type=str, nargs=1, help='location of the RFI mask file')
parser.add_argument('--paramsloc', type=str, nargs=1, help='location of the parameters file')
parser.add_argument('--outloc', type=str, nargs=1, help='location of output')

args = parser.parse_args()

ms_loc = args.msloc
mask_loc = args.maskloc
params_loc = args.paramsloc
output_loc = args.outloc


with open(params_loc[0], 'r') as params_file:
    params = json.load(params_file)
    
print("\nPreflagger: ", params['preflagger'][0]) 
print("\nAOflagger: ", params['aoflagger'][0])
print("\nAveraging: ", params['averaging'][0]['freqstep'])

timestep = 1
freqstep = 1

try:
  freqstep = params['averaging'][0]['freqstep']
except Exception:
  print('No frequency step for averaging provided. Default value 1 will be used')

  
try:
  timestep = params['averaging'][0]['timestep']
except Exception:
  print('No time step for averaging provided. Default value 1 will be used')

parset = dp3.parameterset.ParameterSet()

preflagger_parameters = params['preflagger'][0]
for key in preflagger_parameters:
    my_str = "preflag."+key
    parset.add(my_str, str(preflagger_params[key]))

aoflagger_parameters = params['aoflagger'][0]
for key in aoflagger_parameters:
    my_str = "aoflag."+key
    parset.add(my_str, str(aoflagger_parameters[key]))

averaging_parameters = params['averaging'][0]
for key in averaging_parameters:
    my_str = "average."+key
    parset.add(my_str, str(averaging_parameters[key]))


measurementSet = ms_operations.ReadMS(ms_loc)

vis_ms = measurementSet.GetMainTableData('DATA')
flags_ms = measurementSet.GetMainTableData('FLAG')

chan_freq = measurementSet.GetFreqTableData('CHAN_FREQ')[0]
chan_width = measurementSet.GetFreqTableData('CHAN_WIDTH')[0]

time = measurementSet.GetMainTableData('TIME')
intervals = measurementSet.GetMainTableData('INTERVAL')
phase_center = measurementSet.GetFieldTableData('PHASE_DIR')


uvw_ms = measurementSet.GetMainTableData('UVW')

ant_name = measurementSet.GetAntennaTableData('NAME')
ant_pos  = measurementSet.GetAntennaTableData('POSITION')
ant_diameter = measurementSet.GetAntennaTableData('DISH_DIAMETER')
antenna1 = measurementSet.GetMainTableData('ANTENNA1')
antenna2 = measurementSet.GetMainTableData('ANTENNA2')

num_ants = len(ant_name)
num_baselines = int(num_ants * (num_ants + 1)/2)
num_freqs = len(chan_freq)
num_times = int(vis_ms.shape[0]/num_baselines)
vis_ms_dims = vis_ms.shape
num_pols = vis_ms_dims[2]



scan_num = measurementSet.GetMainTableData('SCAN_NUMBER')
field_id = measurementSet.GetMainTableData('FIELD_ID')

scan_num_reshaped = scan_num.reshape([num_times, num_baselines]) 
field_id_reshaped = field_id.reshape([num_times, num_baselines])
time_reshaped = time.reshape([num_times, num_baselines])
intervals_reshaped = intervals.reshape([num_times, num_baselines])

scan_jumps = np.array([0])

for t in range(1, num_times):
   if scan_num_reshaped[t, 0] != scan_num_reshaped[t-1, 0] or field_id_reshaped[t, 0] != field_id_reshaped[t-1, 0]:
      print(t)
      scan_jumps = np.append(scan_jumps, t)

if scan_jumps[-1] != num_times-1:
   scan_jumps = np.append(scan_jumps, num_times-1)

num_jumps = len(scan_jumps)      
print(scan_jumps)
print(num_jumps)


# RFI mask for preflagger

rfi_file = open(mask_loc[0], "rb")
rfi_mask = pickle.load(rfi_file)

mychan = np.where(rfi_mask)
chan = mychan[0].tolist()
parset.add("preflag.chan", str(chan))

weights = np.ones([num_times, num_baselines, num_freqs, num_pols], dtype="float32")
uvw = uvw_ms.reshape([num_times, num_baselines, 3])

vis = vis_ms.reshape([num_times, num_baselines, num_freqs, num_pols])
flags = np.zeros([num_times, num_baselines, num_freqs, num_pols], dtype=bool)


output_flags = np.zeros((int(num_times/timestep), num_baselines, int(num_freqs/freqstep), num_pols),  np.bool8)
output_visibilities = np.zeros((int(num_times/timestep), num_baselines, int(num_freqs/freqstep), num_pols), np.complex)
#output_uvw = np.zeros((int(num_times/timestep), num_baselines)


start_point = 0
for i in range(num_jumps - 1):
   t_begin = scan_jumps[i]
   t_end = scan_jumps[i + 1]
   first_time = time_reshaped[t_begin, 0]
   last_time = time_reshaped[t_end, 0]
   interval = intervals_reshaped[t_begin, 0] 
   dpinfo = dp3.DPInfo(num_pols)
   dpinfo.set_antennas(ant_name, ant_diameter, ant_pos, antenna1[0: num_baselines], antenna2[0: num_baselines])
   dpinfo.set_channels(chan_freq, chan_width)       
   dpinfo.set_times(first_time, last_time , interval)


   preflag_step = dp3.make_step("preflag", parset,"preflag.", dp3.MsType.regular)
   average_step = dp3.make_step("average", parset, "average.", dp3.MsType.regular)
   aoflag_step = dp3.make_step("aoflag", parset, "aoflag.", dp3.MsType.regular)
   null_step = dp3.make_step("null", parset, "", dp3.MsType.regular)
   
   queue_step = steps.QueueOutput(parset, "")   

   preflag_step.set_next_step(aoflag_step) 
   aoflag_step.set_next_step(average_step)
   average_step.set_next_step(queue_step)
   
   preflag_step.set_info(dpinfo)
   
   for t in range(t_begin, t_end):
       print(t)
       dpbuffer = dp3.DPBuffer()
       dpbuffer.set_weights(weights[t, :, :, :])
       dpbuffer.set_flags(flags[t, :, :, :])
       dpbuffer.set_data(vis[t, :, :, :])
       dpbuffer.set_uvw(uvw[t, :, :])
       preflag_step.process(dpbuffer)   
   preflag_step.finish()    
   
   queue_size = queue_step.queue.qsize()
   for j in range(queue_size):
        dpbuffer_from_queue = queue_step.queue.get()
        output_flags [start_point + j,:,:,:] = np.array(dpbuffer_from_queue.get_flags(), copy=False) 
        output_visibilities[start_point + j,:,:,:]= np.array(dpbuffer_from_queue.get_data(),copy=False)  

   start_point = start_point + queue_size
   print('start_point: ', str(start_point))
