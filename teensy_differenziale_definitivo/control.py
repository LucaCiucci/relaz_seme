####CONTROLLO
import pylab
import numpy

Directory = '../data_did/'
FileName = Directory+ 'dati_2.2_1.txt'
Directory2 = '../data_elaborati/'
FileName2 = Directory2+ 'dati_2.2_1el.txt'
Directory3 = '../tmp/'
FileName3 = Directory2+ 'tmp2.2_1.txt'


x = []
y = []

f = open(FileName, 'r')
f2 = open(FileName3, 'w')
lines = f.readlines()
for i in range(len(lines)):
    if len(lines[i]) <= 14:
        f2.write(lines[i])
        f2.write("\n")
f.close()
f2.close()
x, y = pylab.loadtxt(FileName3, unpack = True)
pylab.errorbar(x, y, linestyle = '', marker = '.')
pylab.show()


t = []
v = []
for i in range(len(x)):
    if(x[i]<4100):
        t.append(x[i])
        v.append(y[i])

x = numpy.array(t)
y = numpy.array(v)

pylab.errorbar(x, y, linestyle = '', marker = '.')
pylab.show()

f3 = open(FileName2, 'w')
for i in range(len(x)):
    f3.write("%f    %f\n" % (x[i], y[i]))

f3.close()
