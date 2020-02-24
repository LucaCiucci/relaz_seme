import pylab

Nskip = 1;
0
v, dv, sv, i, di, si = pylab.loadtxt("../file2Py.txt", unpack=True)
pylab.errorbar(v[0::Nskip], i[0::Nskip], si[0::Nskip], sv[0::Nskip], ls='', marker='.')

v, dv, sv, i, di, si = pylab.loadtxt("../file2Py.txt.bad", unpack=True)
pylab.errorbar(v[0::Nskip], i[0::Nskip], si[0::Nskip], sv[0::Nskip], ls='', marker='.', color="r")

pylab.yscale('log')
pylab.show()
 
