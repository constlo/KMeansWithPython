import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
import pandas as pd

#Haetaan ensin data tietokannasta
mydb = mysql.connector.connect(
  host="172.20.241.9",
  user="dbaccess_ro",
  password="vsdjkvwselkvwe234wv234vsdfas",
  database="measurements"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM rawdata WHERE groupId=66")

myresult = pd.DataFrame(mycursor.fetchall(), columns=['id', 'dateTime', 'groupId', 'a', 'b', 'x', 'y', 'z', 'c', 'flag', 'status'])

#Otetaan talteen x-y-ja z-arvot. Nämä sijoitetaan data2DArray-tietorakenteeseen.
databaseX = myresult['x'].to_numpy(dtype=int)
databaseY = myresult['y'].to_numpy(dtype=int)
databaseZ = myresult['z'].to_numpy(dtype=int)

#Emme voi tietää, ovatko kaikki akselit yhtä pitkiä. Siispä selvitetään suurin pituus np.max-funktiolla.
resultSize = np.max([databaseX.size, databaseY.size, databaseZ.size])

data2DArray = np.zeros(resultSize * 3).reshape(resultSize, 3)

#sijoita tietorakenteeseen
data2DArray[:, 0] = databaseX
data2DArray[:, 1] = databaseY
data2DArray[:, 2] = databaseZ
print(data2DArray)
pd.DataFrame.to_csv(myresult, 'data.csv')

#Varastoi maksimiarvot
maxVals = [databaseX.max(), databaseY.max(), databaseZ.max()]

#Tämän jälkeen luodaan (4x3) matriisi, jossa säilytetään 4 satunnaista pistettä.
keskipisteet = np.zeros(12, dtype=int).reshape((4, 3))
#sijoita satunnaisarvot matriisiin
for i in keskipisteet:
    for j in range(0,3):
        i[j] = np.random.randint(0, maxVals[j])

#Luodaan distances-taulukko etäisyyksien säilyttämistä varten.
Distances = np.zeros(4, dtype=float)

dataFromLoop = np.reshape(np.zeros(1200), [100, 4, 3])

for iterations in range(100):

    #print("Uudet keskipisteet: {}".format(keskipisteet))
    centerPointCumulativeSum = np.zeros(12, dtype=int).reshape((4, 3))
    Counts = np.zeros(4, dtype=int)
    smallestIndex = 0
    for piste in data2DArray:
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

pisteet =pd.DataFrame.from_dict(dataFromLoop[-1]) 

pd.DataFrame.to_csv(pisteet, 'finalpoints.csv')

plt.show()
