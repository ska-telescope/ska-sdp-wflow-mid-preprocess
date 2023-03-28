import visualisation
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='visualisation selection')
parser.add_argument('--dataloc', type=str, nargs=1, help='location of the data')
parser.add_argument('--askedfig', type=str, nargs=1, help='figure: old_flags, new_flags, vis')
parser.add_argument('--output', type=str, nargs=1, help='output directory')
parser.add_argument('--ant1', type=int, nargs=1, help='first antenna index')
parser.add_argument('--ant2', type=int, nargs=1, help='second antenna index')
parser.add_argument('--pol', type=int, nargs=1, help='polarisation of interest')
parser.add_argument('--scan', type=int, nargs=1, help='scan id')
parser.add_argument('--field', type=int, nargs=1, help='field number')

args = parser.parse_args()

data_loc = args.dataloc[0]
asked_fig = args.askedfig[0]
output_loc = args.output[0]
ant1 = args.ant1
ant2 = args.ant2
scan_num = args.scan
fld_id = args.field
pol = args.pol

vis = np.load(data_loc + "/vis.npy")
new_flags = np.load(data_loc + "/new_flags.npy")
old_flags = np.load(data_loc + "/old_flags.npy")
antenna1 = np.load(data_loc + "/antenna1.npy")
antenna2 = np.load(data_loc + "/antenna2.npy")
scan_number = np.load(data_loc + "/scan_number.npy")
field_id = np.load(data_loc + "/field_id.npy")

num_antennas = np.unique(antenna1).shape[0]
num_baselines = int(num_antennas * (num_antennas + 1)/2)


myfig = visualisation.visualise(vis, new_flags, antenna1, antenna2, scan_number, field_id)

baseline_idx = myfig.find_the_baseline(ant1, ant2)
period_of_time = myfig.find_time_range_with_scan_field(scan_num, fld_id)
print(baseline_idx)
print(period_of_time)

where = ""
type = ""

if asked_fig == "old_flags":
   where = output_loc + "/old_flags_ant1" + str(ant1) + "_ant2_" + str(ant2) + "_sc_" + str(scan_num) + "_fld_"+ str(fld_id) + ".png"
   type = "flag"
   mydata = old_flags[period_of_time[0]:period_of_time[1], baseline_idx: num_baselines: (period_of_time[1] - period_of_time[0]) * num_baselines, :, pol]

if asked_fig == "new_flags":
   where = output_loc + "/new_flags_ant1" + str(ant1) + "_ant2_" + str(ant2) + "_sc_" + str(scan_num) + "_fld_"+ str(fld_id) + ".png"
   type = "flag"   
   mydata = new_flags[period_of_time[0]:period_of_time[1], baseline_idx: num_baselines: (period_of_time[1] - period_of_time[0]) * num_baselines, :, pol]

if asked_fig == "vis":
   where = output_loc + "/visibility_ant1" + str(ant1) + "_ant2_" + str(ant2) + "_sc_" + str(scan_num) + "_fld_"+ str(fld_id) + ".png"
   type = "vis"
   mydata = vis[period_of_time[0]:period_of_time[1], baseline_idx: num_baselines: (period_of_time[1] - period_of_time[0]) * num_baselines, :, pol]
 
myfig.visualise(mydata, type, where)

