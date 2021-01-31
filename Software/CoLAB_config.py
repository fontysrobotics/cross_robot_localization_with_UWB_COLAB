"""This module is used to configure the main settings of the CoLAB software"""

# General
colab_id = "mir_03"
mqttBroker = "test.mosquitto.org"

# UWB tags
frontTag = '/dev/UWBfront'
rearTag = '/dev/UWBrear'
distanceBetweenTags = 65 #cm

# Rest API
restAvailable = True
restHost = 'http://mir.com/api/v2.0.0/'
restAuthorization = 'Basic YWRtaW46OGM2OTc2ZTViNTQxMDQxNWJkZTkwOGJkNGRlZTE1ZGZiMTY3YTljODczZmM0YmI4YTgxZjZmMmFiNDQ4YTkxOA=='

# Test/simulation
cost = 15