import numpy as np
from matplotlib import pyplot as plt
from scipy.odr import odrpack
import time
import os
from inspect import getsourcefile #serve per ottenere la directory del file

## Presentazione

print("Benvenuto nel programma calcolatore degli indici di rifrazione!")
time.sleep(1.0)

## Cartella corrente

dir_path = os.path.dirname(getsourcefile(lambda:0)) #directory file
os.chdir(dir_path)
print("La cartella corrente è:\n", os.getcwd())
time.sleep(1)

## Importazione indici dal file Lista indici.txt

with open("Lista materiali.txt", "r") as filetesto:
    materiali = list( filetesto.read().split("\n") ) #costruisce una lista e poi spacchetta i materiali con split usando come separatore \n

## Input

obj = input("Inserisci il nome del materiale di cui vuoi calcolare l'indice di rifrazione: ")
time.sleep(1.0)

ai_input = input("Inserisci gli angoli di incidenza in gradi (separati da spazi): ")
ai = np.array( list(map(float, ai_input.split(" "))) ) #spacchettamento angoli di incidenza
time.sleep(1.0)


while min(ai) < 0: #ERRORE DI ANGOLO DI INCIDENZA NEGATIVO
    print("Angoli negativi non sono validi.")
    time.sleep(1.0)

    ai_input = input("Inserisci gli angoli di incidenza in gradi (separati da spazi): ")
    ai = np.array( list(map(float, ai_input.split(" "))) ) #spacchettamento angoli di incidenza
    time.sleep(1.0)


ar_input = input("Inserisci gli angoli di rifrazione in gradi (separati da spazi): ")
ar = np.array( list(map(float, ar_input.split(" "))) ) #spacchettamento angoli di rifrazione
time.sleep(1.0)

while min(ar) < 0: #ERRORE DI ANGOLO DI RIFRAZIONE NEGATIVO
    print("Angoli negativi non sono validi.")
    time.sleep(1.0)

    ar_input = input("Inserisci gli angoli di rifrazione in gradi (separati da spazi): ")
    ar = np.array( list(map(float, ar_input.split(" "))) ) #spacchettamento angoli di rifrazione
    time.sleep(1.0)

while len(ai) != len(ar): #ERRORE DI INPUT PER LUNGHEZZA DIVERSA
    print("Inserire lo stesso numero di angoli di incidenza e di rifrazione, per favore.")
    time.sleep(2.0)

    ai_input = input("Inserisci gli angoli di incidenza in gradi (separati da spazi): ")
    ai = np.array( list(map(float, ai_input.split(" "))) ) #spacchettamento angoli di incidenza
    time.sleep(1.0)


    while min(ai) < 0: #ERRORE DI ANGOLO DI INCIDENZA NEGATIVO (Dopo errore di lunghezza)
        print("Angoli negativi non sono validi.")
        time.sleep(1.0)

        ai_input = input("Inserisci gli angoli di incidenza in gradi (separati da spazi): ")
        ai = np.array( list(map(float, ai_input.split(" "))) ) #spacchettamento angoli di incidenza
        time.sleep(1.0)



    ar_input = input("Inserisci gli angoli di rifrazione in gradi (separati da spazi): ")
    ar = np.array( list(map(float, ar_input.split(" "))) ) #spacchettamento angoli di rifrazione
    time.sleep(1.0)

    while min(ar) < 0: #ERRORE DI ANGOLO DI RIFRAZIONE NEGATIVO (Dopo errore di lunghezza)
        print("Angoli negativi non sono validi.")
        time.sleep(1.0)

        ar_input = input("Inserisci gli angoli di rifrazione in gradi (separati da spazi): ")
        ar = np.array( list(map(float, ar_input.split(" "))) ) #spacchettamento angoli di rifrazione
        time.sleep(1.0)


ai_res = float(input("Inserisci la risoluzione in gradi dello strumento: "))
time.sleep(1.0)

while ai_res < 0:
    print("Risoluzione negativa non è valida.")
    time.sleep(1.0)

    ai_res = float(input("Inserisci la risoluzione in gradi dello strumento: "))
    time.sleep(1.0)

## Cambio di directory

print("Vuoi scegliere di salvare i dati in un percorso particolare?")
time.sleep(1.0)
scelta = input("'y' o 'n'? ")
time.sleep(1.0)

while scelta != "y" and scelta != "n" : #ERRORE DI DIGITAZIONE
    scelta = input("'y' o 'n'? ")


if scelta == "y":
    cwd = input("Inserisci il percorso dove vuoi salvare i dati (con doppie slash): ")
    os.chdir(cwd)

if scelta == "n":
    print("Il file verrà salvato nella posizione corrente.")
    time.sleep(2.0)


## Conversione misure degli angoli

ai = np.deg2rad(ai) #conversione in radianti
sigma_ai = np.full(ai.shape, [np.deg2rad(ai_res)])

ar = np.deg2rad(ar) #conversione in radianti
sigma_ar = np.full(ar.shape, [np.deg2rad(ai_res)])



## Calcolo dei seni

sin_ai = np.sin(ai)
sigma_sin_ai = np.cos(ai) * sigma_ai

sin_ar = np.sin(ar)
sigma_sin_ar = np.cos(ar) * sigma_ar


## Modello linare


def line(pars, x):

    return pars[0] * x + pars[1]

## Costruzione grafico

fig = plt.figure("Grafico del fit")
plt.grid(ls='dashed', which='both')
plt.xlabel('Angoli di incidenza [rad]')
plt.ylabel('Angoli di rifrazione [rad]')
plt.xlim(0, 1)
plt.ylim(0, 1)

## Plot dei dati sperimentali

plt.errorbar(sin_ai, sin_ar, sigma_sin_ar, sigma_sin_ai, fmt='.g')

## Fit ODR

model = odrpack.Model(line)
data = odrpack.RealData(sin_ai, sin_ar, sx=sigma_sin_ai, sy=sigma_sin_ar)
odr = odrpack.ODR(data, model, beta0=(1.0, 1.0))
out = odr.run()
rec_n_obj_hat, q_hat = out.beta
rec_n_obj_sigma, sigma_q = np.sqrt(out.cov_beta.diagonal())

chiquadro = out.sum_square
chiquadro_rid = chiquadro / (len(sin_ai) - 2)

xx = np.linspace(0, 1, 101)
plt.plot(xx, xx * rec_n_obj_hat + q_hat)

## Stampe intermedie

print("----------")

print(f"Il reciproco dell'indice di rifrazione è: {rec_n_obj_hat:.3f} ± {rec_n_obj_sigma:.3f}")
print(f"q = {q_hat:.3f} ± {sigma_q:.3f}")
print(f"Chiquadro = {chiquadro:f}")
print(f"Chiquadro ridotto = {chiquadro_rid:f}")

print("----------")

## Risultati finali

n_aria = 1.0 #indice di rifrazione aria

n_obj_hat = n_aria/rec_n_obj_hat
n_obj_sigma =  rec_n_obj_sigma / rec_n_obj_hat**2

print("L'indice di rifrazione del materiale {} vale: ".format(obj) + f"{n_obj_hat:.3f} ± {n_obj_sigma:.3f}")

stampa_testo = "Angoli di incidenza: " + ai_input + "\nAngoli di rifrazione: " + ar_input + "\nL'indice di rifrazione del materiale {} vale: ".format(obj) + f"{n_obj_hat:.3f} ± {n_obj_sigma:.3f}"

stampa_indici = "L'indice di rifrazione del materiale {} vale: ".format(obj) + f"{n_obj_hat:.3f} ± {n_obj_sigma:.3f}"


## Creazione file di testo

with open("Indice_{}.txt".format(obj), "w") as filetesto:
    filetesto.write(stampa_testo)

## Aggiunta al file degli indici

with open("Indici.txt", "a") as filetesto:
    filetesto.write("\n" + stampa_indici)

## Aggiunta alla lista degli indici nel file Lista materiali.txt

with open("Lista materiali.txt", "a") as filetesto:
    filetesto.write("\n" + obj)

## Creazione file png

plt.savefig("Grafico_{}.png".format(obj))

plt.show()