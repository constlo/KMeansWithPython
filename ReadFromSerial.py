import serial

ser = serial.Serial()
ser.baudrate = 9600
ser.port = 'COM5'

readData = []

ser.open()
num = input("What is the orientation of the sensor? (1 = up, 2 = down, 3=right, 4=left): ").encode('utf-8')
ser.write(num)
while ser.isOpen():
    text = ser.readline().decode('ASCII')
    readData.append(text)
    print(text)
    if(text == ''):
        break
ser.close()