"""This module is used to receive the location data from the UWB tags, process the data and publish the processed data on the MQTT network on a separate thread"""

import paho.mqtt.publish as publish
from statistics import mean
import threading
import serial
import math
import time
import json

import CoLAB_config as config

running = False

preProcessedLocation = [0,0]
preProcessedOrientation = 0

# receive the location data from the UWB tags, process the data and publish the processed data on the MQTT network
def sendLocation():
    """Receive the location data from the UWB tags, process the data and publish the processed data on the MQTT network"""

    global running
    global preProcessedLocation
    global preProcessedOrientation
    running = True
    readingCount = 0
    lastReading = 0

    #Rear tag serial config
    serRear = serial.Serial()
    serRear.port = config.rearTag #red tag
    serRear.baudrate = 115200
    serRear.bytesize = serial.EIGHTBITS 
    serRear.parity =serial.PARITY_NONE 
    serRear.stopbits = serial.STOPBITS_ONE 
    serRear.timeout = 1
    serRear.open()
    serRear.write(b'\r\r')
    
    #Front tag serial config
    serFront = serial.Serial()
    serFront.port = config.frontTag #blue tag
    serFront.baudrate = 115200
    serFront.bytesize = serial.EIGHTBITS 
    serFront.parity =serial.PARITY_NONE 
    serFront.stopbits = serial.STOPBITS_ONE 
    serFront.timeout = 1
    serFront.open()
    serFront.write(b'\r\r')

    time.sleep(1)

    serFront.close()
    serRear.close()

    time.sleep(0.5)

    serFront.open()
    serRear.open()

    # loop until running is no longer true
    while running == True:
        # read the location data from the UWB tags 5 times per second
        if (time.perf_counter()-lastReading) > 1/5:

            # save the time of this reading
            lastReading = time.perf_counter()

            #Start with empty lists if the reading count is 0
            if readingCount == 0:
                FTagX = []
                FTagY = []
                RTagX = []
                RTagY = []

            # read location data from rear UWB tag
            serRear.write(b'apg\n')
            serRear.readline()
            dataRear= str(serRear.readline())

            # read location data from front UWB tag
            serFront.write(b'apg\n')
            serFront.readline()
            dataFront = str(serFront.readline())

            # extract x, y, z and qf values from the raw received data of the rear tag
            dataRear = dataRear.split(' ')
            dataRear[1] = float(dataRear[1].replace("x:","")) 
            dataRear[2] = float(dataRear[2].replace("y:","")) 
            dataRear[3] = float(dataRear[3].replace("z:","")) 
            dataRear[4] = dataRear[4].replace("qf:","")
            dataRear[4] = float(dataRear[4].replace("\\r\\n'",""))
            dataRear.pop(0)

            # extract x, y, z and qf values from the raw received data of the front tag
            dataFront = dataFront.split(' ')
            dataFront[1] = float(dataFront[1].replace("x:","")) 
            dataFront[2] = float(dataFront[2].replace("y:","")) 
            dataFront[3] = float(dataFront[3].replace("z:","")) 
            dataFront[4] = dataFront[4].replace("qf:","")
            dataFront[4] = float(dataFront[4].replace("\\r\\n'",""))
            dataFront.pop(0)

            # add the received x and y data to the lists
            FTagX.append(dataFront[0])
            FTagY.append(dataFront[1])
            RTagX.append(dataRear[0])
            RTagY.append(dataRear[1])

            # update readingCount
            readingCount += 1

        # preprocess the readings from the UWB tag if 10 readings are done
        if readingCount == 10:
            # preprocess the last 10 readings
            frontTagX = mean(FTagX) # FrontTag and RearTag are arrays 1x2 
            frontTagY = mean(FTagY)
            rearTagX = mean(RTagX)
            rearTagY = mean(RTagY)

            # find midpoint location
            midpointX = ((frontTagX-rearTagX)/2 + rearTagX)/1000
            midpointY = ((frontTagY-rearTagY)/2 + rearTagY)/1000
            preProcessedLocation = [round(midpointX, 2) , round(midpointY, 2)]

            # find orientation
            preProcessedOrientation = math.atan2((frontTagY-rearTagY), (frontTagX-rearTagX)) * 180/math.pi

            # find accuracy
            calculatedDistanceBetweenTags = math.sqrt(math.pow((frontTagX-rearTagX),2) + math.pow((frontTagY-rearTagY),2))/10
            errorDistanceBetweenTags = round(abs(calculatedDistanceBetweenTags-config.distanceBetweenTags),2)

            # build the dictionary with the data to send
            messageToSend = {
              "colab_id": config.colab_id,
              "location": preProcessedLocation,
              "orientation": int(preProcessedOrientation),
              "errorDistance": errorDistanceBetweenTags
            }

            # create a string with the data in JSON format
            payloadToSend = json.dumps(messageToSend)

            # publish the data on the MQTT topic
            publish.single("CRL/location", payloadToSend, hostname=config.mqttBroker)

            # reset the reading count to 0
            readingCount = 0

# create a thread to send location data
def startSending():
    """Start a thread for receiving UWB data from the tags and sending the processed data over the MQTT network"""
    
    t = threading.Thread(target=sendLocation)
    t.daemon = True
    t.start()

# stop the thread for sending location data
def stopSending():
    """Stop the thread for receiving UWB data from the tags and sending the processed data over the MQTT network"""

    global running
    running = False