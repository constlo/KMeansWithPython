import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from itertools import chain
import pandas as pd



#lue putty.log tiedosto ja muokkaa se numpy arrayksi
#Käytetään squeeze-metodia, jolla isnompiulotteinen array muokataan peinemmäksi
mydf = np.loadtxt('putty.log', dtype= int)
print(mydf.size)
numberOfRows = 0
arraySize = mydf.size
threeDivisible = mydf.size % 3
if(threeDivisible != 0):
    #jos arrayn koko ei ole kolmella jaollinen, täytyy loput alkiot leikata pois.
    #Tässä tapauksessa 119 - 2 = 117 -> jaollinen kolmella
    arraySize -= threeDivisible
#Leikataan 2 viimeistä alkiota pois.
handledArray = np.copy(mydf[0:arraySize])
lastIndex = int(arraySize / 3)
#Muokataan vielä jonosta 2d-array
twoDarray = handledArray.reshape(int(handledArray.size / 3), 3)

#Viikko 5, vaihe 2: Keskipisteiden arpominen
#luodaan x, y, ja z-arvoparit
x_ax = twoDarray[0:40, 0]
y_ax = twoDarray[0:40, 1]
z_ax = twoDarray[0:40, 2]

#luodaan myös lista, jossa säilytetään akselien maksimiarvot
maxVals = [x_ax.max(), y_ax.max(), z_ax.max()]

#Tämän jälkeen luodaan (4x3) matriisi, jossa säilytetään 4 satunnaista pistettä.
keskipisteet = np.zeros(12, dtype=int).reshape((4, 3))
#sijoita satunnaisarvot matriisiin
for i in keskipisteet:
    for j in range(0,3):
        i[j] = np.random.randint(0, maxVals[j])
Distances = np.zeros(4, dtype=float)
dataFromLoop = np.reshape(np.zeros(1200), [100, 4, 3])

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

            
ax.scatter(x_ax, y_ax, z_ax, alpha=0.1)
ax.scatter(keskipisteet[0][0], keskipisteet[0][1], keskipisteet[0][2], marker='+', color='r')
ax.scatter(keskipisteet[1][0], keskipisteet[1][1], keskipisteet[1][2], marker='+', color='r')
ax.scatter(keskipisteet[2][0], keskipisteet[2][1], keskipisteet[2][2], marker='+', color='r')
ax.scatter(keskipisteet[3][0], keskipisteet[3][1], keskipisteet[3][2], marker='+', color='r')
plt.show()


for iterations in range(100):
    if iterations == 5:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

                    
        ax.scatter(x_ax, y_ax, z_ax, alpha=0.1)
        ax.scatter(keskipisteet[0][0], keskipisteet[0][1], keskipisteet[0][2], marker='+', color='r')
        ax.scatter(keskipisteet[1][0], keskipisteet[1][1], keskipisteet[1][2], marker='+', color='r')
        ax.scatter(keskipisteet[2][0], keskipisteet[2][1], keskipisteet[2][2], marker='+', color='r')
        ax.scatter(keskipisteet[3][0], keskipisteet[3][1], keskipisteet[3][2], marker='+', color='r')
        plt.show()
    #print("Uudet keskipisteet: {}".format(keskipisteet))
    centerPointCumulativeSum = np.zeros(12, dtype=int).reshape((4, 3))
    Counts = np.zeros(4, dtype=int)
    smallestIndex = 0
    for piste in twoDarray:
        Distances = np.zeros(4, dtype=float)
        #Valitaan sellainen etäisyys, joka on suurempi kuin kaikki mahdolliset etäisyydet. 
        pienin = 1000.0
        for i in range(4):
            #Laske etäisyys
            Distances[i] = np.linalg.norm(keskipisteet[i] - piste)
            #Jos löytyy pienempi etäisyys kuin pienin etäisyys, sijoita muuttujaan ja tallenna millä indeksillä löytyi
            if (Distances[i] < pienin):
                smallestIndex = i
                pienin = Distances[i]
        #Lisää kumulatiiviseen summaan pienimmän pisteen arvot, ja lisää Counts-taulukkoon yksi
        centerPointCumulativeSum[smallestIndex] += piste
        Counts[smallestIndex] += 1
    """
    Seuraavaksi centerPointCumulativeSum ja count muuttujan avulla pitää laskea uudet keskipisteet. 
    Huomaa jos joku keskipiste ei saanut yhtään ”voittoa” edellisessä vaiheessa, niin tälle keskipisteelle arvotaan uusi lähtöarvo.

    Toteuta algoritmiin vielä yksi ulompi luuppirakenne, joka tekee tämän kalvon vaiheet 1 ja 2 esim 10 kertaa.

    Toteuta edellisen kohdan luuppirakenteen sisälle jonkinlainen datarakenne, johon keräät keskipisteiden arvot jokaiselta iteraatiokerralta.

    Visualisoi algoritmin suppeneminen kohti oikeita keskipisteitä plottaamalla tai tulostamalla edellisessä vaiheessa keräämäsi keskipisteiden arvot.
    Testaa algoritmia. Algoritmin pitäisi aina päätyä tilanteeseen, missä kullekin keskipisteelle tulee 10 data pistettä. Kun algoritmi toimii varmasti, 
    vie syntynyt koodi githubiin ja viimeistele readme dokumentin K-means algoritmikuvaus

    """
    #Valitaan uudelleen ne pisteet, joihin ei tullut voittoa, ja arvotaan niihin uudet arvot
    for i in range(4):
        if(Counts[i] == 0):
            for k in range(0, 3):
                keskipisteet[i][k] = np.random.randint(0, maxVals[j])
                #print("index {} has 0 counts. New point is {}".format(i, keskipisteet[i]))
        else:
            keskipisteet[i] = centerPointCumulativeSum[i, :] / Counts[i]
    dataFromLoop[iterations] = keskipisteet

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

            
ax.scatter(x_ax, y_ax, z_ax, alpha=0.1)
ax.scatter(dataFromLoop[-1][0][0], dataFromLoop[-1][0][1], dataFromLoop[-1][0][2], marker='+', color='r')
ax.scatter(dataFromLoop[-1][1][0], dataFromLoop[-1][1][1], dataFromLoop[-1][1][2], marker='+', color='r')
ax.scatter(dataFromLoop[-1][2][0], dataFromLoop[-1][2][1], dataFromLoop[-1][2][2], marker='+', color='r')
ax.scatter(dataFromLoop[-1][3][0], dataFromLoop[-1][3][1], dataFromLoop[-1][3][2], marker='+', color='r')
plt.show()
  