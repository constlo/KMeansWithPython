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

print(np.min(myresult['x'].to_numpy(dtype=int)))

#Otetaan talteen x-y-ja z-arvot. Nämä sijoitetaan data2DArray-tietorakenteeseen.
databaseX = myresult['x'].to_numpy(dtype=int)
databaseY = myresult['y'].to_numpy(dtype=int)
databaseZ = myresult['z'].to_numpy(dtype=int)

#Emme voi tietää, ovatko kaikki akselit yhtä pitkiä. Siispä selvitetään suurin pituus np.max-funktiolla.
resultSize = np.max([databaseX.size, databaseY.size, databaseZ.size])

data2DArray = np.zeros(resultSize * 3, dtype=int).reshape(resultSize, 3)

#sijoita tietorakenteeseen
data2DArray[:, 0] = databaseX
data2DArray[:, 1] = databaseY
data2DArray[:, 2] = databaseZ
print(data2DArray[:, 0])
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

iterAmount = 100

dataFromLoop = np.reshape(np.zeros(iterAmount * 12), [iterAmount, 4, 3])

#muuttuja johon tallennetaan viimeisin iteraatio, jossa oltiin:
lastIteration = 0

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

            
ax.scatter(databaseX, databaseY, databaseZ, alpha=0.05, color='green', marker='^')
ax.scatter(keskipisteet[0][0], keskipisteet[0][1], keskipisteet[0][2], marker='+', color='r')
ax.scatter(keskipisteet[1][0], keskipisteet[1][1], keskipisteet[1][2], marker='+', color='r')
ax.scatter(keskipisteet[2][0], keskipisteet[2][1], keskipisteet[2][2], marker='+', color='r')
ax.scatter(keskipisteet[3][0], keskipisteet[3][1], keskipisteet[3][2], marker='+', color='r')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()

for iterations in range(iterAmount):
    if iterations == 10:
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

                    
        ax.scatter(databaseX, databaseY, databaseZ, alpha=0.05, color='green', marker='^')
        ax.scatter(keskipisteet[0][0], keskipisteet[0][1], keskipisteet[0][2], marker='+', color='r')
        ax.scatter(keskipisteet[1][0], keskipisteet[1][1], keskipisteet[1][2], marker='+', color='r')
        ax.scatter(keskipisteet[2][0], keskipisteet[2][1], keskipisteet[2][2], marker='+', color='r')
        ax.scatter(keskipisteet[3][0], keskipisteet[3][1], keskipisteet[3][2], marker='+', color='r')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()
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
        centerPointCumulativeSum[smallestIndex] += piste
        Counts[smallestIndex] += 1
    #Valitaan uudelleen ne pisteet, joihin ei tullut voittoa, ja arvotaan niihin uudet arvot
    for i in range(4):
        if(Counts[i] == 0):
            
            for k in range(0, 3):
                keskipisteet[i][k] = np.random.randint(0, maxVals[j])
            #print("index {} has 0 counts. New point is {}".format(i, keskipisteet[i]))
        else:
            keskipisteet[i, :] = centerPointCumulativeSum[i][:] / Counts[i]
    dataFromLoop[iterations] = keskipisteet
    lastIteration = iterations
    if(iterations > 10):
        if np.array_equal(keskipisteet, dataFromLoop[iterations - 1]):
            print("No change from last iteration. Terminating loop at index {}".format(iterations))
            break
print(Counts)
    
    
            
fig = plt.figure()
ax = fig.add_subplot(projection='3d')

pisteet = pd.DataFrame.from_dict(dataFromLoop[lastIteration])


ax.scatter(databaseX, databaseY, databaseZ, alpha=0.05, color='green', marker='^')
ax.scatter(dataFromLoop[lastIteration][0][0], dataFromLoop[lastIteration][0][1], dataFromLoop[lastIteration][0][2], color='r', marker='+')
ax.scatter(dataFromLoop[lastIteration][1][0], dataFromLoop[lastIteration][1][1], dataFromLoop[lastIteration][1][2], color='r', marker='+')
ax.scatter(dataFromLoop[lastIteration][2][0], dataFromLoop[lastIteration][2][1], dataFromLoop[lastIteration][2][2], color='r', marker='+')
ax.scatter(dataFromLoop[lastIteration][3][0], dataFromLoop[lastIteration][3][1], dataFromLoop[lastIteration][3][2], color='r', marker='+')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

pd.DataFrame.to_csv(pisteet, 'finalpoints.csv')

plt.show()
