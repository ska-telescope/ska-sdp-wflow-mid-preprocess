import visualisation
import numpy as np

parser = argparse.ArgumentParser(description='visualisation selection')
parser.add_argument('--dataloc', type=str, nargs=1, help='location of the data')
parser.add_argument('--datatype', type=str, nargs=1, help='data type: flag or visibility')
parser.add_argument('--output', type=str, nargs=1, help='output directory')
parser.add_argument('--ant1', type=int, nargs=1, help='first antenna index')
parser.add_argument('--ant2', type=int, nargs=1, help='second antenna index')
parser.add_argument('--scan', type=int, nargs=1, help='scan id')
parser.add_argument('--field', type=int, nargs=1, help='field number')

args = parser.parse_args()

data_loc = args.dataloc
data_type = args.datatype
output_loc = args.output
antenna1 = args.ant1
antenna2 = args.ant2
scan_id = args.scan
field_num = args.field


  

