#================================
#        correzione dati
#================================
print("\nlettura file originali...")

# legge i dati e mette nella cartella temporanea quelli corretti (copiato da control.py)
for _name in data_files:
    name = data_folder + _name
    print(name)
    data_file = open(name, 'r')
    tmp_file = open(tmp_folder + _name, 'w')
    lines = data_file.readlines()
    for i in range(len(lines)):
        if len(lines[i]) <= 14:
            tmp_file.write(lines[i])
            #tmp_file.write("\n")
    data_file.close()
    tmp_file.close()

#================================
#         lettura dati
#================================
print("\nlettura file temporanei...")

# leggi dati ADC0 e ADC1 dalla cartella temporanea

# vettori di vettori delle letture acquisite
ADC0datas = []
ADC1datas = []

# vettori di vettori degli errori delle letture acquisite
ADC0stds = []
ADC1stds = []

for _name in data_files:
    name = tmp_folder + _name
    print(name)
    _x, _y = np.loadtxt(name, unpack = True)
    _x = np.array(_x)
    _y = np.array(_y)
    ADC0datas.append(_x);
    ADC1datas.append(_y);

    # grossolani, eventualmente da modificare/togliere
    ADC0stds.append(_x * 0. + 4.);
    ADC1stds.append(_y * 0. + 4.);

# converte le liste? in array numpy per comodità
ADC0datas = np.array(ADC0datas)
ADC1datas = np.array(ADC1datas)
ADC0stds = np.array(ADC0stds)
ADC1stds = np.array(ADC1stds)

<<<<<<< HEAD
k = 0

# elimina i dati senza senso
=======
>>>>>>> 744009577df0ca0e5f301f1b849642e4166774bc
for i in range(Nruns):
    j = 0
    while(k < len(ADC0datas[i])):
        # se un numero è maggiore di 4095, allora elimina la coppia
        if ((ADC0datas[i][j] > 4095) or (ADC0datas[i][j] < -4095) or (ADC1datas[i][j] > 4095) or (ADC1datas[i][j] < -4095)):
            ADC0datas[i] = np.delete(ADC0datas[i], j)
            ADC1datas[i] = np.delete(ADC1datas[i], j)
            ADC0stds[i] = np.delete(ADC0stds[i], j)
            ADC1stds[i] = np.delete(ADC1stds[i], j)
            j = j - 1
        j = j +1
        k = k + 1

#================================
#          conversioni
#================================

# valori convertiti da ADC in volts
voltages0s = []
voltages1s = []
voltages0stds = []# errori
voltages1stds = []
for i in range(Nruns):
    _vs, _stds = ADC02Voltage(ADC0datas[i], ADC0stds[i])
    voltages0s.append(_vs)
    voltages0stds.append(_stds)
    _vs, _stds = ADC12Voltage(ADC1datas[i], ADC1stds[i])
    voltages1s.append(_vs)
    voltages1stds.append(_stds)

voltages0s = np.array(voltages0s)
voltages1s = np.array(voltages1s)
voltages0stds = np.array(voltages0stds)
voltages1stds = np.array(voltages1stds)

# valori convertiti da volts in valori utilizzabili nei dati
voltages = voltages0s
voltageStds = voltages0stds
currents = []
currentStds = []
for i in range(Nruns):
    _I, _dI = V2I(voltages1s[i], Rs[i], voltages1stds[i], dRs[i])
    currents.append(_I)
    currentStds.append(_dI)
    
currents = np.array(currents)
currentStds = np.array(currentStds)

# NOTA: da qui in poi sono solo test a caso, il programma dovrà continuare...
for i in range(Nruns):
    #disegna un punto ogni Nskip, solo per vedere come sono fatti i dati
    Nskip = 100
    Nskip = 1
    pylab.errorbar(voltages[i][0::Nskip], currents[i][0::Nskip], currentStds[i][0::Nskip], voltageStds[i][0::Nskip], linestyle = '', marker = '.');
pylab.semilogy()
pylab.show()
