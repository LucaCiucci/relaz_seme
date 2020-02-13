# questo script è (una bozza di) quello che credo potrebbe essere definitivo.
# qui dentro inseriamo i vari progressi fatti negli altri script (o eventualmente
# li richiamiamo)

# SCOPO:
#   - leggere flie di dati e corregere le righe sbagliate,
#     i dati corretti sono messi in una cartella temporanea
#   - convertire i dati nelle unità desiderate
#   - analisi varie (ancora tutto da fare)


# INDICE:
#   - CONFIGURAZIONI: contiene i parametri di configurazione
#   - FUNZIONI: contiene le definizioni di funzioni varie
#   - OPERAZIONI: contiene il corpo dello script!!!


import pylab
import numpy as np
numpy = np # così è più facile fare copia e incolla dia vari scripts
import math
from scipy.optimize import curve_fit
from statistics import *
import os # operazioni su file
import shutil # operazioni su file

#================================================================
#                          CONFIGURAZIONI
#================================================================

Nstep = 20

# i dati filtrati sono messi in questa cartella temporanea
tmp_folder = "tmp/"

# file di dati (da modificare)
data_folder = "data/"
data_files = [
    "dati_220k.txt",
    "dati_22k.txt",
    "dati_2.2k.txt",
    "dati_220.txt",
    "dati_22.txt",
    "dati_2.2.txt",
    "dati_0.22.txt"
    ]
Nruns = len(data_files) # numero di files (runs)

# valori resistenze (da modificare)
Rs = np.array([
    200e3,
    22e3,
    2.2e3,
    220.,
    22.,
    2.2,
    0.22
    ])
dRs = np.array([
    10e3,
    1e3,
    0.1e3,
    10.,
    1.,
    0.1,
    0.01
    ])


# calibrazione ADC
# NOTA: valori di test
# TODO non trovo lo script di calibraizone

#================================================================
#                             FUNZIONI
#================================================================
# TODO non trovo lo script per le calibrazioni

# ADC02Voltage prende le letture (in ADC) e le converte in volt
# secondo la calibrazione eseguita
# parametri:
#   - ADCvalue è la lettura da convertire
#   - ADCstd (opzionale) è la deviazione standard (campione) della lettura
# return
#   - il valore centrale (Volt)
#   - errore (Volt)
#TODO sostituire con la vera funzione di calibrazione
def ADC02Voltage(ADCvalue, ADCstd = 0.):
    return ADCvalue / 4096. * 3.3, pylab.sqrt(ADCstd**2 + 1) / 4096. * 3.3

def ADC12Voltage(ADCvalue, ADCstd = 0.):
    return ADCvalue / 4096. * 3.3, pylab.sqrt(ADCstd**2 + 1) / 4096. * 3.3

# V2A prende le tensioni e le converte in corrente sapendo la resistenza
# parametri
#   - V tensione (Volt)
#   - R reistenza (Ohm)
#   - dV errore su V (Volt)
#   - dR errore su R (Ohm)
# return
#   - corrente (Ampere)
#   - errore su corrente (Ampere)
def V2I(V, R, dV = 0., dR = 0.):
    return V / R, pylab.sqrt((dV / R)**2 + (dR * V / R**2)**2)

#================================================================
#                            OPERAZIONI
#================================================================

#================================
#     operazioni preliminari
#================================
print("\npreparazione...")

# operazioni con cartelle temporanee
try:
    shutil.rmtree(tmp_folder) #rimuove l'evetuale cartella temporane che potrebbe essere rimasta
except OSError as e:
    pass;#  NOP

try:
    os.remove(".gitignore") # rimuovi il vecchio gitignore
except OSError as e:
    pass;#  NOP

# il file gitignore serve a dire a github di non caricare online la cartella temporanea
gitinoreF = open(".gitignore", 'w')
gitinoreF.write(tmp_folder);
gitinoreF.close();

os.mkdir(tmp_folder)

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

# elimina i dati senza senso
for i in range(Nruns):
    for j in range(len(ADC1datas[i])):
        # se un numero è maggiore di 4095, allora elimina la coppia
        if (ADC0datas[i][j] > 4095 or ADC0datas[i][j] < -4095 or ADC1datas[i][j] > 4095 or ADC1datas[i][j] < -4095):
            np.delete(ADC0datas[i], j)
            np.delete(ADC1datas[i], j)
            np.delete(ADC0stds[i], j)
            np.delete(ADC1stds[i], j)


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
    Nskip = 1
    pylab.errorbar(voltages[i][0::Nskip], currents[i][0::Nskip], currentStds[i][0::Nskip], voltageStds[i][0::Nskip], linestyle = '', marker = '.');
pylab.semilogy()
pylab.show()


#================================
#             END
#================================

shutil.rmtree(tmp_folder) # rimuove la cartella temporanea
