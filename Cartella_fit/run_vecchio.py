#================================================================
#                              RUN
#================================================================


from load_data import *
# queste sono le variabili di dati importate:
#   - voltages
#   - voltageStds
#   - currents
#   - currentStds
for i in range(Nruns * 0):
    print(i)
    #pass;
    filtro(voltages[i], currents[i], voltageStds[i], currentStds[i], 3)

Nskip = 1;
c = currents[4] = currents[4][0::Nskip]
v = voltages[4] = voltages[4][0::Nskip]
dv = voltageStds[4] = voltageStds[4][0::Nskip]
dc = currentStds[4] = currentStds[4][0::Nskip]

v, c, dv, dc = filtro(voltages[4], currents[4], voltageStds[4], currentStds[4], 2)

plt.errorbar(v, c, dc, dv, linestyle = '', marker = '.', color = "black")
ls = np.linspace(min(v), max(v), 1000)
py, spy = order0fit(ls, v, c, dv)
plt.plot(ls, py) # test
plt.plot(ls, py + spy)
plt.plot(ls, py - spy)
plt.minorticks_on()
plt.tick_params(direction='in', length=5, width=1., top=True, right=True)
plt.tick_params(which='minor', direction='in', width=1., top=True, right=True)
plt.show()
