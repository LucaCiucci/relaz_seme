from matplotlib import pyplot as plt
import numpy as np

Nskip = 1;
0
v, dv, sv, i, di, si = np.loadtxt("../file2Py.txt", unpack=True)
plt.errorbar(v[0::Nskip], i[0::Nskip], si[0::Nskip], sv[0::Nskip],
             ls='', marker='.')

v, dv, sv, i, di, si = np.loadtxt("../file2Py.txt.bad", unpack=True)
plt.errorbar(v[0::Nskip], i[0::Nskip], si[0::Nskip], sv[0::Nskip], ls='',
             marker='.', color="r")

plt.yscale('log')
plt.show()
 
