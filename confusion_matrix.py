import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import serial

"""
This python file reads data sent to serial, and plots a confusion matrix based on the received data.
"""


directions = {1 : "up", 2 : "down", 3 : "right", 4 : "left"}

#log the directions to measure
loggedDirections = []

#Here we get the numbers from arduino
gotPredictions = []

ser = serial.Serial('COM13', 9600)
if not ser.is_open:
        ser.open()

for i in range(4):
        dirToSend = int(input("Give the direction you want to measure (up, down, right, left) in numbers(1-4):"))

        if ser.is_open:
                ser.write(dirToSend)
                gotDir = int(ser.read(1).decode('ASCII'))
                print(f"sent {directions[dirToSend]}, got {directions[gotDir]}")
                loggedDirections.append(dirToSend)
                gotPredictions.append(gotDir)

confMat = confusion_matrix(loggedDirections, gotPredictions)

confMatDisplay = ConfusionMatrixDisplay(confMat, display_labels=['Up', 'Down', 'Right', 'Left'])


confMatDisplay.plot(cmap=plt.cm.Blues)

confMatDisplay.ax_.set(
                #title='Sklearn Confusion Matrix with labels!!', 
                xlabel='Predicted', 
                ylabel='Actual')


plt.show()