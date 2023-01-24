import ms_operations
import argparse
import numpy as np

parser = argparse.ArgumentParser(description='location of data')
parser.add_argument('--msloc', type=str, nargs=1, help='location of the MeasurmentSet')
parser.add_argument('--extract', type=str, nargs=1, help='location of the extracted data from the MS')

args = parser.parse_args()
msFileName = args.msloc
measurementSet = ms_operations.ReadMS(msFileName)

vis = measurementSet.GetMainTableData('DATA')
np.save("data/vis", vis)

chan_freq = measurementSet.GetFreqTableData('CHAN_FREQ')[0]
chan_width = measurementSet.GetFreqTableData('CHAN_WIDTH')[0]

np.save("data/chan_freq", chan_freq)
np.save("data/chan_width", chan_width)


