import os


stream = os.popen('filetestoC\fileprova.exe')
output = stream.read()
print(output)
