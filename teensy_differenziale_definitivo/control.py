####CONTROLLO
import pylab
import numpy
from matplotlib import pyplot as plt

Directory = '../data_did/'
FileName = 'dati_0.22_1.txt'
Directory2 = '../data_elaborati/'
FileName2 ='dati_0.22_1el.txt'
Directory3 = '../tmp/'
FileName3 = 'tmp0.22_1.txt'


x = []
y = []

f = open(Directory + FileName, 'r')
f2 = open(Directory3 + FileName3, 'w')
lines = f.readlines()
for i in range(len(lines)):
    if len(lines[i]) <= 14:
        f2.write(lines[i])
        f2.write("\n")
f.close()
f2.close()
x, y = numpy.loadtxt(Directory3 + FileName3, unpack = True)
plt.errorbar(x, y, linestyle = '', marker = '.')
plt.show()


t = []
v = []
for i in range(len(x)):
    if(x[i]<4100):
        t.append(x[i])
        v.append(y[i])

x = numpy.array(t)
y = numpy.array(v)

plt.errorbar(x, y, linestyle = '', marker = '.')
plt.show()

f3 = open(Directory2 + FileName2, 'w')
for i in range(len(x)):
    f3.write("%f    %f\n" % (x[i], y[i]))

f3.close()
