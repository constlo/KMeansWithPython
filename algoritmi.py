import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import mysql.connector
import pandas as pd
from sklearn.cluster import KMeans


#Haetaan ensin data tietokannasta
mydb = mysql.connector.connect(
  host="172.20.241.9",
  user="dbaccess_ro",
  password="vsdjkvwselkvwe234wv234vsdfas",
  database="measurements"
)