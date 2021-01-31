import paho.mqtt.client as mqtt
import json
import datetime

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
    payload = json.loads(msg.payload)
    print(datetime.datetime.now().strftime("%H:%M:%S.%f"), end=' ')
    print(msg.topic, end=':\t')
    print(payload)

# Create an MQTT client, attach our routines to it and loop forever.
def startMQTT():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("test.mosquitto.org", 1883, 60)

    client.loop_forever()

startMQTT()