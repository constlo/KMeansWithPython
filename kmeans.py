import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from itertools import chain


#lue putty.log tiedosto ja muokkaa se numpy arrayksi
mydf = pd.read_csv('putty.log').to_numpy()
#saatiin 2d array, joka pitää saada 1d arrayksi. Käytetään siihen itertoolsin chain-funktiota.
cleaned = np.array(list(chain(*mydf)))
NearestSizeOfthree = int(np.round(cleaned.size / 3) * 3)
cleaned.resize(NearestSizeOfthree)
#clean the array from incomplete rows
for i in cleaned:
    for j in range(0, 3):
        if i[j] == 0:
            break

print(cleaned)

new = cleaned.reshape(40, 3)
x_ax = new[0:40, 0]
y_ax = new[0:40, 1]
z_ax = new[0:40, 2]

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

ax.scatter(x_ax, y_ax, z_ax)
plt.show()

#new = np.reshape(new, [3, 40])