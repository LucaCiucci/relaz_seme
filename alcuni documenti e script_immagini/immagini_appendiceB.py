import pylab
import numpy
import matplotlib.pyplot as plt

def f(x):
    return x**3
def f_prim(x):
    return 3*(x**2)

gridsize = (3, 1)
pylab.minorticks_on()
pylab.xlabel("x")
pylab.ylabel("y")
pylab.grid(color = "gray")
pylab.grid(b=True, which='major', color='#666666', linestyle='-')
pylab.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
currXlim = [-2., 4.]
currYlim = [-1., f(3.)+1]
pylab.xlim(currXlim[0], currXlim[1])
pylab.ylim(currYlim[0], currYlim[1])

bucket = numpy.linspace(-4., 4., 1000)
pylab.plot(bucket, f(bucket), color = 'black', label = 'f(x)')

pylab.errorbar(3., f(3.), marker = 'o', linestyle = '', color = 'red', label = '(x[i], f(x[i]))')

pylab.plot(bucket, f_prim(3.)*(bucket - 3.) + f(3.) , color = 'red', label = 'tangente in (x[i], f(x[i]))')

print(3. - f(3.)/f_prim(3))

pylab.title("Visualizzazione grafica relativa ad una singola iterazione")

pylab.errorbar(0., 0., marker = 'o', linestyle = '', color = 'black', label = '(v, f(v))')

pylab.errorbar(2., 0., marker = 'o', linestyle = '', color = 'blue', label = '(x[i+1], 0)')

pylab.errorbar(2., f(2.), marker ='o', linestyle = '', color = 'green', label = '(x[i+1],f(x[i+1]))')

retta = []
for i in range(len(bucket)):
    retta.append(0.)
retta = numpy.array(retta)
pylab.plot(bucket, retta, color = 'black', linestyle = '--', label = 'y = 0')

legend = pylab.legend(loc='upper left', shadow=True, fontsize='medium')
pylab.show()

R = 0.0475
I0 = 3.18e-9
nVt = 0.0464

Nstep = 20



def sck(V):
    return I0*(pylab.exp(V/nVt) - 1)

def errFun(V, V0):
    return sck(V) + (V - V0)/R

def deriv_errFun(V):
    return I0 / nVt * pylab.exp(V/nVt) + 1./R;

def curr(V):
    l = []
    b = []
    v = V;
    #l.append(0.)
    #b.append(v)
    for i in range(Nstep):
        a = deriv_errFun(v)
        v = v - errFun(v, V) /a
        b.append(v)
        l.append((V-v)/R)
    return numpy.array(l), numpy.array(b)

def ddp(I):
    return nVt*pylab.log((I0+I)/I0) + R*I

iteration = []
for i in range(Nstep):
    iteration.append(i+1)



I1 = 1.
I2 = 5.
I3 = 7.


gridsize = (1., 1./3)
pylab.title("Convergenza a I col metodo di Newton", size = 12)
pylab.xlabel("Grado di iterazione", size = 11)
pylab.ylabel("I - corrente dalla serie [A]", size = 11)
pylab.grid(color = "gray")
pylab.grid(b=True, which='major', color='#666666', linestyle='-')
pylab.grid(b=True, which='minor', color='#999999', linestyle='-')#, alpha=0.2)
voltage1 = ddp(I1)
l1, a1 = curr(voltage1)
voltage2 = ddp(I2)
l2, a2 = curr(voltage2)
voltage3 = ddp(I3)
l3, a3 = curr(voltage3)
plt.yscale('log')
pylab.errorbar(iteration, abs(l1 - I1), color = 'red', linestyle = '-', marker = 'o', label = 'valori ottenuti dalla serie (1 A)')
pylab.errorbar(iteration, abs(l2 - I2), color = 'black', linestyle = '-', marker = 'o', label = 'valori ottenuti dalla serie (5 A)')
pylab.errorbar(iteration, abs(l3 - I3), color = 'blue', linestyle = '-', marker = 'o', label = 'valori ottenuti dalla serie (7 A)')
pylab.semilogy()
pylab.minorticks_on()
legend = pylab.legend(loc='upper right', shadow=True, fontsize='medium')
pylab.show()

gridsize = (1, 1./3)
pylab.minorticks_on()
pylab.title("Convergenza a v col metodo di Newton", size = 12)
pylab.xlabel("Grado di iterazione", size = 11)
pylab.ylabel("x - v   [V]", size = 11)
voltage1 = ddp(I1)
voltage2 = ddp(I2)
voltage3 = ddp(I3)
variable1 = voltage1 - I1*R
variable2 = voltage2 - I2*R
variable3 = voltage3 - I3*R
l1, a1 = curr(voltage1)
l2, a2 = curr(voltage2)
l3, a3 = curr(voltage3)
pylab.errorbar(iteration, a1 - variable1, color = 'red', linestyle = '-', marker = 'o', label = 'valori ottenuti dalla serie (5 A)')
pylab.errorbar(iteration, a2 - variable2, color = 'black', linestyle = '-', marker = 'o', label = 'valori ottenuti dalla serie (1 A)')
pylab.errorbar(iteration, a3 - variable3, color = 'blue', linestyle = '-', marker = 'o', label = 'valori ottenuti dalla serie (7 A)')
b = numpy.zeros(1000)
plt.yscale('log')
pylab.semilogy()
pylab.grid(color = "gray")
pylab.grid(b=True, which='major', color='#666666', linestyle='-')#, linewidth = 1)#, dashes = (1, 5, 0.1, 0.5))
pylab.grid(b=True, which='minor', color='#999999', linestyle='-')#, linewidth = 1)#, dashes = (1, 1, 0.1, 0.1))
legend = pylab.legend(loc='upper right', shadow=True, fontsize='medium')
pylab.show()
