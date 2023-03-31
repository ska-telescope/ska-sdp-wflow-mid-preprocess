import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from dateutil.parser import ParserError
import numpy as np

class visualise:
    ''' 
    This class visualises  the visibilities and flags
    '''
    def __init__(self, visibilities, flags, antenna1, antenna2, scan, field):
      
      self.vis = visibilities
      self.flags = flags
      self.antenna1 = antenna1
      self.antenna2 = antenna2
      self.scan = scan
      self.field = field
      
      self.num_times = visibilities.shape[0]
      self.num_baselines = visibilities.shape[1]
      self.num_freqs = visibilities.shape[2]
      self.num_pols = visibilities.shape[3] 


    def find_the_baseline(self, ant1, ant2):
        a = np.intersect1d(np.where(self.antenna1 == ant1),  np.where(self.antenna2 == ant2))
        index = a[0]
        print("index : " + str(index)) 
        return index


    def find_time_range_with_scan_field(self, sc, fld): 
         a = np.intersect1d(np.where(self.scan[:, 0] == sc), np.where(self.field[:,0] == fld))
         print(a)
         return  a[0], a[-1] + 1

    def illustrate(self, the2darray, type, where):
         if type == "flag":
            cmap = sns.cubehelix_palette(start=1.8, rot=1.1, light=0.7, n_colors=2)
            ticks = np.array([0, 1])
            ax = sns.heatmap(the2darray, cmap=ListedColormap(cmap), cbar_kws={"ticks": [0, 1]})
            plt.title('flags')
            plt.xlabel('channels')
            plt.ylabel('time')
            plt.show()
            plt.savefig(where)
         if type == "vis":
            cmap = sns.cubehelix_palette(start=1.8, rot=1.1, light=0.7, n_colors=1000)
            ax = sns.heatmap(the2darray, cmap=ListedColormap(cmap))
            plt.title('visibilities')
            plt.xlabel('channels')
            plt.ylabel('time')
            plt.show()
            plt.savefig(where)

 



          
