#CONFIGURAZIONI
#print(pylab.sqrt(costanti.Nstep))
#import librerie #non capisco perchè non funziona senza
from lib import *

grafici_calibrazione = False

Nstep = 20

# i dati filtrati sono messi in questa cartella temporanea
tmp_folder = "tmp/"

# se non vi piace odificate questi nomi
file2CName = "file2C.txt"
file2PyName = "file2Py.txt"
maxRatio = 3.0
minV = 0.2

# file di dati (da modificare)#!!
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
    200e3,#!!
    22e3,#!!
    2.2021e3,
    216.22,
    21.86,
    2.212,
    0.226
    ])
dRs = np.array([
    10e3,#!!
    1e3,#!!
    0.4,
    0.07,
    0.01,
    0.008,
    0.008
    ])
