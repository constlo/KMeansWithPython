# Tietoliikenteen sovellusprojekti
## Konsta Lohilahti
TVT21SPL, Oulun Ammattikorkeakoulu


This is a school project made at Oulu University of Applied Sciences.
In this project, we developed our own k-means algorithm using sensor data from an embedded device.

Here is the architecture diagram of our project.

<a href="https://github.com/constlo/TL_SvProjekti2022_loko/blob/main/systemflowchart.drawio.png?raw=true"> <img alt="system flowchart" src="https://github.com/constlo/TL_SvProjekti2022_loko/blob/main/systemflowchart.drawio.png?raw=true" >  </a>

This first image displays the algorithm with arbitary data.

<a href="https://github.com/constlo/TL_SvProjekti2022_loko/blob/main/preprocessedData.png"><img alt="Implementation using provided data" src="https://github.com/constlo/TL_SvProjekti2022_loko/blob/main/preprocessedData.png"> </a>

The second image displays the algorithm working with our own data.

<a href="https://github.com/constlo/TL_SvProjekti2022_loko/blob/main/sensorData.png"><img alt="Implementation using own data" src="https://github.com/constlo/TL_SvProjekti2022_loko/blob/main/sensorData.png"> </a>

The k-means algorithm we implemented works in the following way:

1. We assume k amount of centroids. Their coordinates are randomized relative to the data's maximum and minimum values. (Here, we know the amount of k is 4, so no need to figure out the optimum k first)
2. Assume the data points to the centroids, and start to iterate the centroid's position relative to the data points. The iteration stops when the centroid position has not changed.
3. The trained centroids are stored for later use.

Our algorith was then ported to arduino for prediction purposes. Measurements for the arduino yielded the following confusion matrix:

<a href="https://github.com/constlo/TL_SvProjekti2022_loko/blob/main/Confusion_matrix.png"><img alt="confusion matrix" src="https://github.com/constlo/TL_SvProjekti2022_loko/blob/main/Confusion_matrix.png"> </a>

<a title="alaa kaddour, CC BY-SA 4.0 &lt;https://creativecommons.org/licenses/by-sa/4.0&gt;, via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File:Sql_data_base_with_logo.png"><img width="512" alt="Sql data base with logo" src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Sql_data_base_with_logo.png/512px-Sql_data_base_with_logo.png">
</a><sub> (1)</sub>

<a title="JrawX, CC0, via Wikimedia Commons" href="https://commons.wikimedia.org/wiki/File:Arduino_Uno_board.jpg"><img width="512" alt="Arduino Uno board" src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Arduino_Uno_board.jpg/512px-Arduino_Uno_board.jpg"></a><sub> (2)</sub>

<a title="putty.log-tiedosto" href="">


Sources:

(1)<sub>https://commons.wikimedia.org/wiki/File:Sql_data_base_with_logo.png</sub> alaa kaddour, CC BY-SA 4.0

(2)<sub>https://commons.wikimedia.org/wiki/File:Arduino_Uno_board.jpg</sub> JrawX, CC0, via Wikimedia Commons
