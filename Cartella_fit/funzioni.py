from config import *
from calibrazione import matrixADC1, matrixADC0, parADC1, parADC0, legge, leggesumerror_model

def ADC02Voltage(ADCvalue, ADCstd):
    return legge(ADCvalue, *parADC0),\
           pylab.sqrt((leggesumerror_model(ADCvalue, *parADC0, matrixADC0[0][0],\
                                           matrixADC0[1][1], matrixADC0[0][1]))**2  \
                      +(ADCstd*parADC0[0])**2)

def ADC12Voltage(ADCvalue, ADCstd):##cambiare nome?
    return legge(ADCvalue, *parADC1),\
           pylab.sqrt((leggesumerror_model(ADCvalue, *parADC1, matrixADC1[0][0],\
                              matrixADC1[1][1], matrixADC1[0][1]))**2\
                      +(ADCstd*parADC0[1])**2)

def V2I(V, R, dV, dR):
    return V / R, pylab.sqrt((dV / R)**2 + (dR * V / R**2)**2)

#...
