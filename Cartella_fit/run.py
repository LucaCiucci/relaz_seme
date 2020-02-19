#================================================================
#                              RUN
#================================================================


from load_data import *
# queste sono le variabili di dati importate:
#   - voltages
#   - voltageStds
#   - currents
#   - currentStds
for i in range(Nruns):
    pass;
    #filtro(voltages[i], currents[i], voltageStds[i], currentStds[i], 3)

pylab.errorbar(voltages[4], currents[4], currentStds[4], voltageStds[4], linestyle = '', marker = '.', color = "black")
pylab.show()
