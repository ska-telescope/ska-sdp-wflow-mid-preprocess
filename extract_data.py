import ms_operations
import argparse
import numpy as np
import pickle

parser = argparse.ArgumentParser(description='location of data')
parser.add_argument('--msloc', type=str, nargs=1, help='location of the MeasurmentSet')
parser.add_argument('--extract', type=str, nargs=1, help='location of the extracted data from the MS')
parser.add_argument('--maskloc', type=str, nargs=1, help='location of the RFI mask file')

args = parser.parse_args()
msFileName = args.msloc
mask_loc = args.maskloc
measurementSet = ms_operations.ReadMS(msFileName)

vis = measurementSet.GetMainTableData('DATA')
np.save("data/vis", vis)

uvw = measurementSet.GetMainTableData('UVW')
np.save("data/uvw",  uvw)

flag = measurementSet.GetMainTableData('FLAG')
np.save("data/flag", flag)

chan_freq = measurementSet.GetFreqTableData('CHAN_FREQ')[0]
chan_width = measurementSet.GetFreqTableData('CHAN_WIDTH')[0]

np.save("data/chan_freq", chan_freq)
np.save("data/chan_width", chan_width)

ant_name = measurementSet.GetAntennaTableData('NAME')
ant_pos  = measurementSet.GetAntennaTableData('POSITION')
ant_diameter = measurementSet.GetAntennaTableData('DISH_DIAMETER')
antenna1 = measurementSet.GetMainTableData('ANTENNA1')
antenna2 = measurementSet.GetMainTableData('ANTENNA2')

np.save("data/ant_name", ant_name)
np.save("data/ant_pos", ant_pos)
np.save("data/ant_diameter", ant_diameter)
np.save("data/antenna1", antenna1)
np.save("data/antenna2", antenna2)

time = measurementSet.GetMainTableData('TIME')
np.save("data/time", time)
interval = measurementSet.GetMainTableData('INTERVAL')
np.save("data/interval", interval)

phase_center = measurementSet.GetFieldTableData('PHASE_DIR')
np.save("data/phase_center", phase_center)


rfi_file = open(mask_loc[0], "rb")
rfi_mask = pickle.load(rfi_file)
np.save("data/rfi_mask", rfi_mask)

print(rfi_file)

