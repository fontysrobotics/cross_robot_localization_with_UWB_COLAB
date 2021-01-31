import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import time

mqttBroker = "test.mosquitto.org"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
 
    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("CRL/location")
    client.subscribe("CRL/tasks")
    client.subscribe("CRL/messenger")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):

    # when a message is received in the location topic 
    if msg.topic == "CRL/location":
        #payload = json.loads(msg.payload)
        #print(payload)
        pass

    # when a message is received in the blackboard topic 
    if msg.topic == "CRL/tasks":
        payload = json.loads(msg.payload)
        #print(payload)
        if payload["msg_type"] == "accepted":
            print(payload["sender"], 'accepted task', payload["task_id"])

    # when a message is received in the messenger topic 
    if msg.topic == "CRL/messenger":
        payload = json.loads(msg.payload)

        # check if message is for this CoLAB
        if payload["receiver"] == ("admin"):
            print('Received: ', payload["message"], '    from', payload["sender"])

# Create an MQTT client, attach the custom routines to it and start it on a separete thread
def startMQTT():                
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    print("Connecting to MQTT Broker:", mqttBroker)

    client.connect(mqttBroker, 1883, 60)

    # start MQTT thread
    client.loop_start()
    time.sleep(1)

print("----------------------\n- ADMIN DEMO CONSOLE -\n----------------------")
startMQTT()

while True:
    inp = input("\nMessage (m) or Task (t)? ")
        
    if inp == "task" or inp == "Task" or inp == "t" or inp == "T":
        task_id = input("Task_id: ")
        action = input("send (s) or accept (a)? ")

        if action == "send" or action == "Send" or action == "s" or action == "S":
            data = {
              "msg_type": "task",
              "task_id": task_id,
              "details": {
                "pickLocation": [23.89, 12.69],
                "placeLocation": [4.23, 9.76],
                "payloadSize": [100, 200, 300],
                "payloadWeight": 43.8
                }
            }
            print('Published new task with Task_ID: ', data["task_id"])
            print('task detail: ', data["details"])

            data = json.dumps(data)
            publish.single("CRL/tasks", data, hostname=mqttBroker)

        elif action == "accept" or action == "Accept" or action == "a" or action == "A":
            data = {
              "msg_type": "accept",
              "task_id": task_id,
            }
            print('Task', data["task_id"], 'can be accepted by an AGV')

            data = json.dumps(data)
            publish.single("CRL/tasks", data, hostname=mqttBroker)
        
        else:
            print("error: invalid input")


    elif inp == "message" or inp == "Message" or inp == "m" or inp == "M":
        receiver = input("CoLAB ID of receiver (or all): ")
        message = input("Message: ")

        data = {
          "receiver": receiver,
          "message": message,
          "sender": "admin"
        }
        print('Send: ', data["message"], '    to', data["receiver"])

        data = json.dumps(data)
        publish.single("CRL/messenger", data, hostname=mqttBroker)
    
    else:
        print("error: invalid input")

    time.sleep(1)