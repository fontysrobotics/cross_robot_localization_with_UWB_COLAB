"""This module is used to communicate with the AGV using RestAPI over ethernet"""

import requests
import json

import CoLAB_config as config

# Fromat Headers
headers = {}
headers['Content-Type'] = 'application/json'
headers['Authorization'] = config.restAuthorization  #This authorization key can be found at mir.com/help/api-documentation


def getBatteryPercentage():
    """Request the status of the AGV and return the current battery percentage of the AGV"""
    # get battery percentage
    #get_status = requests.get(config.restHost + 'status', headers = headers)

    # to simulate the response from the AGV a text file with a recorded response is used ---Only for testing---
    with open('getStatus_Simulation.txt') as json_file:
        get_status = json.load(json_file)

    return round(get_status["battery_percentage"], 2)

def demoMisson():
    """Just a simple demo mission"""
    print("Doing a demo mission")
    
