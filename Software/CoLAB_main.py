import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import requests
import json
import time
import math

import CoLAB_sendLocation as sendLocation
import CoLAB_config as config
import CoLAB_restAPI_MiR as restAPI

# Activate/deactivate prints for debugging
debugPrints = True

# Global list with all AGVs within a set range
AGVMap = []
# Global list with all the open tasks responded to
taskList = []


# Handler for messages in the LOCATION topic
def locationHandler(msg):
    """Handler for messages in the LOCATION topic"""

    payloadReceived = json.loads(msg.payload)

    # check if the received location is not the location of this AGV
    if payloadReceived["colab_id"] != config.colab_id:
        global AGVMap
        # calculating the boundaries locations based on the current location of the AGV and the boundarie range
        boundRange = 100
        XBound = [sendLocation.preProcessedLocation[0] - boundRange, sendLocation.preProcessedLocation[0] + boundRange] #in meters
        YBound = [sendLocation.preProcessedLocation[1] - boundRange, sendLocation.preProcessedLocation[1] + boundRange]

        # variable to indicate if the AGV is already in the AGVMap
        AGVInList = False

        # check if the received AGV location is within the set boundaries from the AGV
        if XBound[0] <= payloadReceived["location"][0] <= XBound[1] and YBound[0] <= payloadReceived["location"][1] <= YBound[1]:
            # calculate the distance from this AGV to the received AGV location
            DistancetoAGV = math.sqrt(math.pow(payloadReceived["location"][0]- sendLocation.preProcessedLocation[0],2) + math.pow(payloadReceived["location"][1]- sendLocation.preProcessedLocation[1],2))

            # calculate the angle from this AGV to the received AGV location
            #AngletoAGV = math.atan2((payloadReceived["location"][1]- sendLocation.preProcessedLocation[1]),(payloadReceived["location"][0]- sendLocation.preProcessedLocation[0])) * 180/math.pi

            # store the CoLAB_ID together with the distance and angle to the AGV
            infoList = [payloadReceived["colab_id"], round(DistancetoAGV, 2), payloadReceived["location"], payloadReceived["orientation"]]

            # check if the AGV is already in the AGVMap
            for i in range(0, len(AGVMap)):
                if AGVMap[i][0] == infoList[0]:
                    # update the AGV information to the new information
                    AGVMap[i][1] = infoList[1]
                    AGVMap[i][2] = infoList[2]
                    AGVMap[i][3] = infoList[3]

                    # set AGVInList true to indicate that this AGV is already in the AGVMap
                    AGVInList = True

                    # exit the for loop if a match is found
                    break

            # if the AGV was not found in AGVMap then add it
            if AGVInList == False:
                AGVMap.append(infoList)

            # display the current AGVMap list
            if debugPrints == True: print('AGVs within', boundRange, 'meters:', AGVMap)

# Handler for messages in the TASKS topic
def tasksHandler(msg):
    """Handler for messages in the TASKS topic"""

    payloadReceived = json.loads(msg.payload)

    # when a new task is received in the tasks topic
    if payloadReceived["msg_type"] == "task":
        global taskList
        # print the task that is received with the task details
        if debugPrints == True: print('Task', payloadReceived["task_id"], 'received with details:', payloadReceived["details"])

        # --- calculation of the cost based on the task details and AGV specification/status ---

        # build the dictionary with the data to send
        message = {
            "msg_type": "response",
            "task_id": payloadReceived["task_id"],
            "sender": config.colab_id,
            "cost": config.cost
        }

        # add the new task to the task list
        taskList.append([message["task_id"], message["cost"]])

        # print the message to send
        if debugPrints == True: print('Responded to task: ', message["task_id"], '  with cost:', message["cost"], '\n')

        # create a string with the data in JSON format
        message = json.dumps(message)

        # publish the message in the messenger topic
        publish.single("CRL/tasks", message, hostname=config.mqttBroker)

    # when a response from a different CoLAB is received in the tasks topic
    if (payloadReceived["msg_type"] == "response") and (payloadReceived["sender"] != config.colab_id):
        
        for i in range(0, len(taskList)):
            if payloadReceived["task_id"] in taskList[i]:
                # check if the cost of the received response is lower then the cost in the task list of the CoLAB
                if payloadReceived["cost"] < taskList[i][1]:
                    # remove the task from the task list
                    taskList.pop(i)
                else:
                    # don't look through the rest of the task list if the task is found with a lower cost
                    break
    
    # when a task is open for accepting
    if payloadReceived["msg_type"] == "accept":
        # check if the task that is open to accept is in the task list
        for i in range(0, len(taskList)):
            if payloadReceived["task_id"] in taskList[i]:
                # print that this CoLAB has accepted the task
                if debugPrints == True: print('Task', payloadReceived["task_id"], 'Accepted', '\n')

                # build the dictionary with the data to send
                message = {
                    "msg_type": "accepted",
                    "task_id": payloadReceived["task_id"],
                    "sender": config.colab_id
                }
                # create a string with the data in JSON format
                message = json.dumps(message)

                # publish the message in the messenger topic
                publish.single("CRL/tasks", message, hostname=config.mqttBroker)

                # execute the task (for now a demo mission)
                if config.restAvailable == True:
                    restAPI.demoMisson()

                # remove the task from the task list
                taskList.pop(i)

                # exit the loop to stop checking the rest of the task list
                break

# Handler for messages in the MESSENGER topic
def messengerHandler(msg):
    """Handler for messages in the MESSENGER topic"""

    payloadReceived = json.loads(msg.payload)

    # check if message is for this CoLAB
    if (payloadReceived["receiver"] == config.colab_id) or (payloadReceived["receiver"] == "all"):
        # display the incoming message
        if debugPrints == True: print('Received: ', payloadReceived["message"], '  from', payloadReceived["sender"])

        # fixed test response if received message is "hello"
        if payloadReceived["message"] == "hello":

            # build the dictionary with the data to send
            message = {
              "receiver": payloadReceived["sender"],
              "message": "world",
              "sender": config.colab_id
            }

            # print the message to send
            if debugPrints == True: print('Send: ', message["message"], '  to', message["receiver"], '\n')

            # create a string with the data in JSON format
            message = json.dumps(message)

            # publish the message in the messenger topic
            publish.single("CRL/messenger", message, hostname=config.mqttBroker)
            

        # reply to getBattery with the battery percentage of the AGV
        if payloadReceived["message"] == "getBattery":
                
            # get the battery percentage of the AGV via RestAPI
            if config.restAvailable == True:
                batteryPercentage = restAPI.getBatteryPercentage()

                # build the dictionary with the data to send
                message = {
                  "receiver": payloadReceived["sender"],
                  "message": batteryPercentage,
                  "sender": config.colab_id
                }

                # print the message to send
                if debugPrints == True: print('Send: ', message["message"], '  to', message["receiver"], '\n')

                # create a string with the data in JSON format
                message = json.dumps(message)

                # publish the message in the messenger topic
                publish.single("CRL/messenger", message, hostname=config.mqttBroker)


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    """Callback for when the client receives a CONNACK response from the server"""

    if debugPrints == True: print("Connected with result code " + str(rc) + "\n")
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("CRL/location")
    client.subscribe("CRL/tasks")
    client.subscribe("CRL/messenger")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    """Callback for when a PUBLISH message is received from the server"""

    # when a message is received in the LOCATION topic 
    if msg.topic == "CRL/location":
        locationHandler(msg)

    # when a message is received in the BLACKBOARD topic 
    elif msg.topic == "CRL/tasks":
        tasksHandler(msg)

    # when a message is received in the MESSENGER topic 
    elif msg.topic == "CRL/messenger":
        messengerHandler(msg)

# Create an MQTT client, attach the custom routines to it and start it on a separete thread
def startMQTT():
    """Create a MQTT client, connect to the MQTT broker specified in CoLAB_config.py and start the client on a new thread"""

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    if debugPrints == True: print("Connecting to MQTT Broker:", config.mqttBroker)

    client.connect(config.mqttBroker, 1883, 60)

    # start MQTT thread
    client.loop_start()


if debugPrints == True: print('CoLAB main code running (CoLAB ID:', config.colab_id, ")")

startMQTT()
#sendLocation.startSending()

#while True:
#    pass