from config import *
from calibrazione import matrixADC1, matrixADC0, parADC1, parADC0, legge, leggesumerror_model





# ADC02Voltage prende le letture (in ADC) e le converte in Volt
# secondo la calibrazione eseguita
# parametri:
#   - ADCvalue è la lettura da convertire
#   - ADCstd (opzionale) è la deviazione standard (campione) della lettura
# return
#   - il valore centrale (Volt)
#   - errore (Volt)
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




# V2I prende le tensioni e le converte in corrente sapendo la resistenza
# parametri
#   - V tensione (Volt)
#   - R reistenza (Ohm)
#   - dV errore su V (Volt)
#   - dR errore su R (Ohm)
# return
#   - corrente (Ampere)
#   - errore su corrente (Ampere)
def V2I(V, R, dV, dR):
    return V / R, pylab.sqrt((dV / R)**2 + (dR * V / R**2)**2)




# gaussian ritorna il valore della gaussiana centrata in mx e sigma = sx
# serve per il metodo di filtraggio dati
# parametri
#   - x
#   - mx centro x
#   - sx sigma x
# return
#   - valore
def gaussian(x, mx, sx):
    return 1. / np.sqrt(2. * np.pi * sx**2) * pylab.exp(-0.5 * (x - mx)**2 / sx**2)




# esegue un fit di ordine 0 dei dati e restituisce media e varianza campione
# in pratica fa una media pesata secondo la gaussiana, si assume che
# var(x) * df/dx << var(y), questa ipotesi non è verificata nei nostri dati
# ma al massimo ci introduce un fattore di scalatura
#
# parametri
#   - x valore di valutazione
#   - xx ascisse dati
#   - yy ordinate dati
#   - dxx sigmax dei dati
# return
#   - media nell'intorno
#   - varianza campione nell'intorno
def order0fit(x, xx, yy, dxx):
    try:
        my = np.zeros(len(x))
        sy = np.zeros(len(x))
        for i in range(len(x)):
            my[i], sy[i] = order0fit_impl(x[i], xx, yy, dxx)
        return my, sy
    except:
        return order0fit_impl(x, xx, yy, dxx)





# implementazione
def order0fit_impl(x, xx, yy, dxx):
    w = gaussian(x, xx, dxx)
    sum_w = sum(w)
    w = w / sum_w

    my = sum(w * yy)
    var_y = sum((yy - my)**2 * w)
    return my, np.sqrt(var_y)

