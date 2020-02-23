#================================================================
#                       CHIAMA L'ESEGUIBILE ESTERNO
#================================================================

from load_data import *

os.mkdir(tmp_folder)
file2C = open(tmp_folder + file2C, 'w')

file2C.write("#V    errV    stdV    I    errI    stdI\n")

for i in range(len(voltages)):
    for j in range(len(voltages[i])):
        file2C.write("%.20f    %.20f    %.20f    %.20f    %.20f    %.20f\n" \
                     %(voltages[i][j], voltageErrs[i][j], voltageStds[i][j],\
                       currents[i][j], currentErrs[i][j],  currentStds[i][j]))
    file2C.write("#================================")

file2C.close()

import subprocess

subprocess.call('test_per_Serena')

##serve per assicurarsi che l'eseguibile abbia finito a scrivere su file
time.sleep(10) ##da modificare una volta che si ha il programma in C++

#il file di testo finale sarà coi numeri giusti una volta che si è scritto il
#file in C++. Questo è di prova


#istruzione da rimettere quando si ha il file giusto
#voltages, voltageErrs, voltageStds, currents,\
#          currentErrs, currentStds\
#          = pylab.loadtxt("filetestoC/filefromC.txt", unpack = True)

shutil.rmtree(tmp_folder) # rimuove la cartella temporanea
