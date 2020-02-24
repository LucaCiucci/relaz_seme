#================================================================
#                       PROCEDE COL FIT
#================================================================

from filtro import *

##FIT
print("\n GRAFICO:")
print(voltages)
print(currentErrs)
gridsize = (3, 1)
grafico1 = g1 = pylab.subplot2grid(gridsize,(0,0),colspan = 1, rowspan = 2)
grafico2 = g2 = pylab.subplot2grid(gridsize,(2,0), colspan = 2)
g1.errorbar(voltages, currents, linestyle = '', color = 'black', marker = '.')
init = [1./10**7, 52/10**3, 0.1]
popt, pcov = curve_fit(curr, voltages, currents, init, currentErrs, absolute_sigma = False)
a1, a2, a3= popt
da1, da2, da3= pylab.sqrt(pcov.diagonal())
print("I0 = %.11f +- %.11f" %(a1, da1))
print("nVt = %f +- %f" %(a2, da2))
print("Rd = %f +- %f" %(a3, da3))
dw = numpy.zeros(len(currentErrs))
for i in range(5):
    for j in range(len(currentErrs)):
        dw[j] = pylab.sqrt(currentErrs[j]**2 + (curr(voltages[j] + voltageErrs[j], *popt)- curr(voltages[j], *popt))**2)
    popt, pcov = curve_fit(curr, voltages, currents, init, dw, absolute_sigma = False)
a1, a2, a3= popt
da1, da2, da3= pylab.sqrt(pcov.diagonal())
print("I0 = %.11f +- %.11f" %(a1, da1))
print("nVt = %f +- %f" %(a2, da2))
print("Rd = %f +- %f" %(a3, da3))

bucket = numpy.linspace(1./1000000, max(voltages)+0.01, 1000)
ordinate = curr(bucket, *popt)
g1.plot(bucket, ordinate, color = 'red')

g1.minorticks_on()
g1.set_title("Corrente vs tensione")
g1.set_xlabel("ddp [V]")#vedi se devi cambiare ordine di grandezza
g1.set_ylabel("I [A]")#vedi se devi cambiare ordine di grandezza
g1.grid(color = "gray")
g1.grid(b=True, which='major', color='#666666', linestyle='-')
g1.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
currXlim = [0.2, max(voltages)+0.01]
g1.set_xlim(currXlim[0], currXlim[1])
currYlim = [min(currents), max(currents)]
#g1.set_ylim(currYlim[0], currYlim[1])


residui =  numpy.zeros(len(voltages))
for i in range(len(voltages)):
    residui[i] = currents[i] - curr(voltages[i], *popt)

g2.minorticks_on()
g2.plot(bucket, bucket*0., color = 'black')
g2.errorbar(voltages, residui, color = 'black', marker = '.', linestyle = '')
g2.set_xlabel("ddp [V]")
g2.set_ylabel("Residui [A]")
g2.grid(color = "gray")
g2.grid(b=True, which='major', color='#666666', linestyle='-')
g2.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
g2.set_xlim(currXlim[0], currXlim[1])
chi_aspettato = len(voltages) - len(popt)
chi = ((residui**2)/dw**2).sum()
print("chi aspettato = %f" % chi_aspettato)
print("chi calcolato = %f" %chi)
pylab.show()


print("\n GRAFICO in carta semilogaritmica:")

gridsize = (3, 1)
pylab.errorbar(voltages, currents, linestyle = '', color = 'black', marker = '.')

bucket = numpy.linspace(0.5, max(voltages)+0.0001, 1000)
ordinate = curr(bucket, *popt)
pylab.plot(bucket, ordinate, color = 'red')

pylab.minorticks_on()
pylab.title("Grafico in scala semilogaritmica")#da cambiare
pylab.xlabel("ddp [V]")#vedi se devi cambiare ordine di grandezza
pylab.ylabel("I [A]")#vedi se devi cambiare ordine di grandezza
pylab.grid(color = "gray")
pylab.grid(b=True, which='major', color='#666666', linestyle='-')
pylab.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
currXlim = [0.2, max(voltages)+0.01]
pylab.xlim(currXlim[0], currXlim[1])
currYlim = [min(currents)-0.1, max(currents)+0.1]
#pylab.ylim(currYlim[0], currYlim[1])

pylab.semilogy()
pylab.show()
