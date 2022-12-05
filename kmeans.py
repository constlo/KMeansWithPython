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


Distances = np.zeros(4, dtype=float)

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
dataFromLoop = np.reshape(np.zeros(1200), [100, 4, 3])

for iterations in range(100):

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
        centerPointCumulativeSum[smallestIndex] += keskipisteet[smallestIndex]
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
            keskipisteet[i] = centerPointCumulativeSum[i][:] / Counts[i]
    dataFromLoop[iterations] = keskipisteet
    print(Counts)

    
            
#ax.scatter(x_ax, y_ax, z_ax)
#fig, axes = plt.subplots()
p1_xpoints = dataFromLoop[:, 0, 0]
p1_ypoints = dataFromLoop[:, 0, 1]
p1_zpoints = dataFromLoop[:, 0, 2]

p2_xpoints = dataFromLoop[:, 1, 0]
p2_ypoints = dataFromLoop[:, 1, 1]
p2_zpoints = dataFromLoop[:, 1, 2]

p3_xpoints = dataFromLoop[:, 2, 0]
p3_ypoints = dataFromLoop[:, 2, 1]
p3_zpoints = dataFromLoop[:, 2, 2]

p4_xpoints = dataFromLoop[:, 3, 0]
p4_ypoints = dataFromLoop[:, 3, 1]
p4_zpoints = dataFromLoop[:, 3, 2]



figure, axis = plt.subplots(2, 2)
  
# For Sine Function
axis[0, 0].plot(p1_xpoints)
axis[0, 0].plot(p1_ypoints)
axis[0, 0].plot(p1_zpoints)
axis[0, 0].set_title("Keskipiste 1")
  
# For Cosine Function
axis[0, 1].plot(p2_xpoints)
axis[0, 1].plot(p2_ypoints)
axis[0, 1].plot(p2_zpoints)
axis[0, 1].set_title("Keskipiste 2")
  
# For Tangent Function
axis[1, 0].plot(p3_xpoints)
axis[1, 0].plot(p3_ypoints)
axis[1, 0].plot(p3_zpoints)
axis[1, 0].set_title("keskipiste 3")
  
# For Tanh Function
axis[1, 1].plot(p4_xpoints)
axis[1, 1].plot(p4_ypoints)
axis[1, 1].plot(p4_zpoints)
axis[1, 1].set_title("keskipiste 4")

plt.show()
  