import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from itertools import chain


#lue putty.log tiedosto ja muokkaa se numpy arrayksi
#Käytetään squeeze-metodia, jolla isnompiulotteinen array muokataan peinemmäksi
mydf = np.asarray(pd.read_csv('putty.log').to_numpy().squeeze(1))
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
"""
Määritellään algoritmissa tarvittavia datarakenteita (keskipisteet):
Keskipisteet, joita on 4 kpl ja kullakin keskipisteellä on x,y,z komponentti. 
Tämä data voidaan siis pitää esim 4 riviä, 3 saraketta käsittävässä numpy matriisissa.
Arvotaan nämä 4 keskipistettä numpyn random.rand() funktion avulla siten, 
että arvottujen satunnaisten lukujen arvot ovat 0 ja suurimman x,y,z arvon välillä. 
Eli satunnaiset arvot skaalataan input datan mukaan.

"""
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


"""
Määritellään algoritmissa tarvittavia datarakenteita 
centerPointCumulativeSum tulee olla keskipisteiden tapaan 4 riviä, 
3 saraketta kokoinen numpy matriisi. 
Tähän summataan aina voittavalle keskipisteelle yhden datapisteen x,y,z komponentit
Counts tulee olla 1 riviä 4 saraketta kokoinen numpy matriisi
ja tänne kasvatetaan aina voittavan keskipisteen datapisteiden lukumäärää yhdellä jokaisen voiton jälkeen.
Distances on myös 1 riviä 4 saraketta kokoinen numpy matriisi 
ja tähän talletetaan laskennan edetessä yksittäisen x,y,z pisteen etäisyys kaikkiin
keskipisteet datarakenteessa oleviin 4 keskipisteeseen ja nuo 4 etäisyysarvoa talletetaan tähän muuttujaan.
"""
centerPointCumulativeSum = np.zeros(12, dtype=int).reshape((4, 3))
Counts = np.zeros(4, dtype=int)
Distances = np.zeros(4, dtype=int)

"""
Opetellaan laskemaan ns euklidinen etäisyys kahden 3D-pisteen välillä. 
Käytä esim np.linalg.norm funktiota. 
Ja tietysti keksit jotkut 2 kpl yksinkertaisia x,y,z pisteitä 3D-avaruudesta, 
joiden etäisyyden varmuudella tiedät tai osaat käsin laskea.

Toteutetaan kahden for luupin rakenne algoritmin ytimeksi:
Ulompi for luuppi ”kiertää” numberOfRows kertaa 
eli käsittelee kaikki tiedostosta löytynee datapisteet. 
Joka luupin kierroksella lasketaan sisäkkäisen luupin avulla tämän kyseisen datapisteen etäisyydet 
ja selvitetään tämän jälkeen minkä keskipisteen etäisyys oli pienin. 
Ja tuon pienimmän etäisyyden keskipisteen count arvoa kasvatetaan yhdellä 
ja  centerPointCumulativeSum muuttujaan summataan x,y,z komponettien arvot.
Sisäkkäinen luuppi laskee yhden datapisteen etäisyyden kaikkiin 4 keskipisteeseen 
ja tallentaa tuloksen distances muuttujaan.
"""



fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(x_ax, y_ax, z_ax)
plt.show()