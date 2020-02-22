#================================================================
#                       CHIAMA L'ESEGUIBILE ESTERNO
#================================================================


from load_data import *

file2C = open('filetestoC/file2C.txt', 'w')

file2C.write("#V    dV    I    dI")

for i in range(len(voltages)):
    for j in range(len(voltages[i])):
        ##dovrebbero essere sei gli elementi ma ora non ricordo come si chiamano
        ##dell variabili... da chiedere a Luca
        file2C.write("%f    %f    %f    %f\n" \
                     %(voltages[i][j], voltageStds[i][j],\
                       currents[i][j], currentStds[i][j]))
    file2C.write("#================================")
file2C.close()

#os.system('filetestoC/fileprova')

import subprocess

subprocess.call('filetestoC/fileprova')

##serve per assicurarsi che l'eseguibile abbia finito a scrivere su file
time.sleep(10) ##da modificare una volta che si ha il programma in C++

#il file di testo finale sarà coi numeri giusti una volta che si è scritto il
#file in C++. Questo è di prova
V, dV, I, dI = pylab.loadtxt("filetestoC/filefromC.txt", unpack = True)
