#================================================================
#                       PROCEDE COL FIT
#================================================================

from filtro import *

##FIT
print("\n GRAFICO:")
gridsize = (3, 1)
grafico1 = g1 = pylab.subplot2grid(gridsize,(0,0),colspan = 1, rowspan = 2)
grafico2 = g2 = pylab.subplot2grid(gridsize,(2,0), colspan = 2)

if plot_points:
    if plot_errors:
        g1.errorbar(voltages, currents, currentErrs, voltageErrs, linestyle = '', color = 'black', marker = '.', alpha=scatterAlpha)
    else:
        g1.errorbar(voltages, currents, linestyle = '', color = 'black', marker = '.', alpha=scatterAlpha)

if plot_errors:
    g1.errorbar(voltages_bad, currents_bad, currentErrs_bad, voltageErrs_bad, linestyle = '', color = 'red', marker = '.', alpha=scatterAlpha)
else:
    g1.errorbar(voltages_bad, currents_bad, linestyle = '', color = 'black', marker = '.', alpha=scatterAlpha)

if plot_sigma_zone:
    xx = pylab.linspace(min(voltages), max(voltages), 1000)
    yy, syy = order0fit(xx, voltages, currents, voltageStds)
    g1.fill_between(xx, yy + 2.0*syy, yy - 2.0*syy, color = 'b', alpha = sigma_zone_alpha)
    g1.fill_between(xx, yy + syy, yy - syy, color = 'b', alpha = sigma_zone_alpha)

if offset_fit:
    init = [4.3/10**9, 47.5/10**3, 0.046, 0.0]
else:
    init = [1./10**7, 52/10**3, 0.1]
    
popt, pcov = curve_fit(curr, voltages, currents, init, currentErrs, absolute_sigma = False)
a = popt
da = pylab.sqrt(pcov.diagonal())
print("I0 = %g +- %g" %(a[0], da[0]))
print("nVt = %g +- %g" %(a[1], da[1]))
print("Rd = %f +- %f" %(a[2], da[2]))
if offset_fit:
    print("offset = %g +- %g" %(a[3], da[3]))

dw = numpy.zeros(len(currentErrs))
for i in range(iterazioni_fit):
    for j in range(len(currentErrs)):
        dw[j] = pylab.sqrt(currentErrs[j]**2 + (curr(voltages[j] + voltageErrs[j], *popt)- curr(voltages[j], *popt))**2)
    popt, pcov = curve_fit(curr, voltages, currents, init, dw, absolute_sigma = False)

a = popt
da = pylab.sqrt(pcov.diagonal())
print("I0 = %g +- %g" %(a[0], da[0]))
print("nVt = %g +- %g" %(a[1], da[1]))
print("Rd = %f +- %f" %(a[2], da[2]))
if offset_fit:
    print("offset = %g +- %g" %(a[3], da[3]))

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
g2.plot(bucket, bucket*0., color = 'red')
if plot_points:
    if plot_errors:
        g2.errorbar(voltages, residui, dw, color = 'black', marker = '.', linestyle = '', alpha=scatterAlpha)
    else:
        g2.errorbar(voltages, residui, color = 'black', marker = '.', linestyle = '', alpha=scatterAlpha)
if plot_sigma_zone:
    xx = pylab.linspace(min(voltages), max(voltages), 1000)
    yy, syy = order0fit(xx, voltages, currents, voltageStds)
    g2.fill_between(xx, yy + 2.0*syy - curr(xx, *popt), yy - 2.0*syy - curr(xx, *popt), color = 'b', alpha = sigma_zone_alpha)
    g2.fill_between(xx, yy + syy - curr(xx, *popt), yy - syy - curr(xx, *popt), color = 'b', alpha = sigma_zone_alpha)
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

bucket = numpy.linspace(0.2, max(voltages)+0.0001, 1000)
ordinate = curr(bucket, *popt)

if offset_fit:
    p_offset = a[3]
else:
    p_offset = 0

if plot_points:
    if plot_errors:
        pylab.errorbar(voltages, currents - p_offset, currentErrs, voltageErrs, linestyle = '', color = 'black', marker = '.', alpha=scatterAlpha)
    else:
        pylab.errorbar(voltages, currents - p_offset, linestyle = '', color = 'black', marker = '.', alpha=scatterAlpha)
        
if plot_bad_points:
    if plot_errors:
        pylab.errorbar(voltages_bad, currents_bad - p_offset, currentErrs_bad, voltageErrs_bad, linestyle = '', color = 'red', marker = '.', alpha=scatterAlpha)
    else:
        pylab.errorbar(voltages_bad, currents_bad - p_offset, linestyle = '', color = 'red', marker = '.', alpha=scatterAlpha)

if plot_sigma_zone:
    xx = pylab.linspace(min(voltages), max(voltages), 1000)
    yy, syy = order0fit(xx, voltages, currents, voltageStds)
    pylab.fill_between(xx, yy + 2.0*syy, yy - 2.0*syy, color = 'b', alpha = sigma_zone_alpha)
    pylab.fill_between(xx, yy + syy, yy - syy, color = 'b', alpha = sigma_zone_alpha)

pylab.plot(bucket, ordinate - p_offset, color = 'red')
    

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
