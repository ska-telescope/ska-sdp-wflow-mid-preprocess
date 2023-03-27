import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

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
      self.num_freqs = visbilities.shape[2]
      self.num_pols = visibilities.shape[3] 


    def find_the_baseline(self, ant1, ant2):
        index = 0
        for i in range(num_baselines):
           if antenna1 == ant1 and antenna2 == ant2:
              index = i
              break
        return index


     def find_time_range_with_scan_field(self, sc, fld)
         begin = 0
         end = 0
         for i in range(num_times):
            if scan[i, 0] = sc and field[i, 0] = fld:
               begin = i
               break
          
         k = begin
         while scan[k, 0] == sc and field[k, 0] == fld:
               k = k + 1
         end = k
         sc_fld_range = [begin, end]
         return  sc_fld_range

     def illustrate(self, the2darray, type, where):
         if type == "flags":
            cmap = sns.cubehelix_palette(start=1.8, rot=1.1, light=0.7, n_colors=2)
            ticks = np.array([0, 1])
            ax = sns.heatmap(flags_2sm, cmap=ListedColormap(cmap), cbar_kws={"ticks": [0, 1]})
            plt.title('flags')
            plt.xlabel('channels')
            plt.ylabel('time')
            plt.show()
            plt.savefig(where)
         if type == "visibilities":
            cmap = sns.cubehelix_palette(start=1.8, rot=1.1, light=0.7, n_colors=1000)
            ax = sns.heatmap(flags_2sm, cmap=ListedColormap(cmap))
            plt.title('visibilities')
            plt.xlabel('channels')
            plt.ylabel('time')
            plt.show()
            plt.savefig(where)

 



          
