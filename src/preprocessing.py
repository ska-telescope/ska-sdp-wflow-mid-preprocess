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
interval = measurementSet.GetMainTableData('INTERVAL')
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

scan_num = measurementSet.GetMainTableData('SCAN_NUMBER')
field_id = measurementSet.GetMainTableData('FIELD_ID')

