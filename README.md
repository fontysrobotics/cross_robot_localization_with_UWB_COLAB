# cross_robot_localization_with_UWB_COLAB

The new way to design large scale automation project is through the use of Autonomously Guided Vehicles (AGVs). They allow the connection of different workcells to have more flexibility and all this autonomously. This new technology brings a brandd new market with different companies competing to manufacture the best robot for a said application. This brings the costumers to a place where they have to go to different suppliers for the best AGVs based on their application. Incorporating AGVSs of different brands in the same automation process is a difficult task. While AGVs are good at navigating around a building and completing repetitive tasks, when faced with an unknown moving object such as another AGV they get into trouble. As the different brands cannot communicate this creates a serious issue.

## Project

The goal of the project is to make collaboration between AGVs of different brands possible using a relatively cheap solution. The main issue with collaboration is the lack of communication of crucial data. As the issue arises for navigation, the most important data to be shared between the AGVs is location. Localizing multi-vendor AGVs and sharing their location on the same delocalised system. This will allow the recognition of AGVs as obstacles and will leave room for future implementation of a task division control system. This delocalised communication system will achieve collaboration between the AGVs of various brands.

## Problem

The problem of the assignment is to create a delocalised communication system between the AGVs that can determine the position of each AGV. The localization system is built on the decawave UWB device. The principle of this device is to use the delay in Ultra Wide Band signals to measure distance between the devices on the same network. This localization system must be integrated with the AGVs. Each AGV must have a UWB device for localization which in some way has to be connected to a network of all other AGVs. The creation of this system is the problem of the assignment.

## Solution

In order to incorporate the UWB localization system with the AGV, a device titled Communication and Localization Add on Board or CoLAB was created as a solution. The CoLAB device handles the creation and connection of an AGV to the localization network as well as to the UWB network and the AGV. A CoLAB device is attached to each AGV along with two UWB devices that serve as a front and back tag for the positioning. Inside the CoLAb is a Raspberry pi that reads the positioning information from the two tags via UART. This information is processed to return location and orientation. The CoLAB publishes location, orientation and other useful information from the AGV config file as a message to a network which all AGVs are connected to. From this network AGVs scan and read messages of other AGVs and determine their location orientation and most important properties. This information is sent to the AGV and can be implemented for the software to recognize other AGVs as obstacles. Thus, solving the Communication and Localization issue between AGVs of different vendors. This system also opens the possibility to many more future solutions.

## Navigation of gitHub Page

Within the following the contents of the CoLAB gitHub page will be explained. The three main components the read me, repository and wiki will be highlighted.

* ### Read Me 
Within the read me the basic introduction to the project and problem happens. The products of the project thus to content of the gitHub page is also explained. Alongside this information the main credits to the page as well as a quick how to use guide can be found.

* ### Repository
The repository is where the final products of the project thus the content can be found. This is where the final designs and software can be downloaded from. All the research material used is also provided alongside the datasheets and explaining flow charts and diagrams. Some files to aid with system set up can also be found in the repository.

* ### Wiki
The wiki is where the design is given a further explanation. Each components of the system is given a page along with explanations to its design. Some pages elaborate on the system, validation or final conclusions. For navigation use the table of contents side bar on the right side of the page.

## How to use

Within the following a quick start guide will be given on how to set up the CoLAB system on your own AGV. It is Important to note that this guide will give a global layout and reference set up files, however some extra more in depth set up information might be found in the referenced files.

* ### How to initiate (loading code + connect)
In order to set up a system like the CoLAB first order all the components, print the parts and PCB. After this is completed there is a guide titled (start guide) in the depositor that is an assembly guide to the CoLAB. In this guide further information details how to set up a raspberry pi for the CoLAB as well.
Once the CoLAB is set up it is time to set up the UWB devices with the correct image. Only the tags on the AGV have to be set up

* ### How to set up (config)
It is very easy to use a CoLAB device. It is almost plug and play. There are a couple of things that need to be commpleted before use. A list of these can be found below. It is important to note that these steps must be repeated for each CoLAB device on each AGV.

1. Order all parts and assemble the device compoennets using the [guides](https://github.com/fontysrobotics/cross_robot_localization_with_UWB_COLAB/tree/main/PhysicalSystem/Assembly_documents)
1. Fill out [Configuration File](https://github.com/fontysrobotics/cross_robot_localization_with_UWB_COLAB/blob/main/Software/CoLAB_config.py) of AGV
1. Plug tags to CoLAB and Attach to AGV
1. Note down distance between tags in config file
1. Set up ports of tags using [set up guide](https://github.com/fontysrobotics/cross_robot_localization_with_UWB_COLAB/blob/main/UWB_Documentation/UWB_Setup_Guides/Use%20RaspberryPi%20terminal%20(1).docx)
1. The device must be connected to the network and it is ready to use

* ### End results
As an end reslut of running the code correctly, there are two important aspects taht happen. The communication code between all the connected AGVs is running and they are communicating their information to each other. The second thing is a visualziation software that is built into every AGV. This shows the AGVs around. This is the end result of code in a nutshell, the wiki explains further information of the exact communication and information passing through.


## Bibliography & Credits

This project was created as part of a Mechatronics university course for Fontys University of Applied Sciences with the involvement of the following parties:

### Created by
* Nicole Celine
* Arjan van der Heijden
* Mike Luiken
* Simeon Stoyanov
* Pascal Dinjens
* Long Nguyen
* Ryan Muhammad
* Benedek Papp

### Mentorship and Project Ownership
* Pablo Negrete Rubio
* Sjriek Alers


Throughout the project the following sources were used as guidence, inspiration and technical details:

### Sources

* EEAdi, et al. “Using DWM1001 API on Raspberry Pi and PySerial.” Decawave Tech Forum, 8 Dec. 2019, [decaforum.decawave.com/t/using-dwm1001-api-on-raspberry-pi-and-pyserial/6567]( decaforum.decawave.com/t/using-dwm1001-api-on-raspberry-pi-and-pyserial/6567). 

* Robots, Mobile Industrial. “Please Select Language.” MiR100™ | Mobile Industrial Robots, [www.mobile-industrial-robots.com/en/solutions/robots/mir100/]( www.mobile-industrial-robots.com/en/solutions/robots/mir100/). 

* “The Standard for IoT Messaging.” MQTT, [mqtt.org/]( mqtt.org/).

* Eclipse Mosquitto, 8 Jan. 2018, [mosquitto.org/]( mosquitto.org/.). 

* Craggs, Ian. “Eclipse Paho: The Eclipse Foundation.” Enabling Open Innovation & Collaboration, [www.eclipse.org/paho/]( www.eclipse.org/paho/). 

* “Visualization with Python¶.” Matplotlib, [matplotlib.org/]( matplotlib.org/). 

* “Home.” Decawave, 29 May 2019, [decawave.com/](decawave.com/). 

* Apichet Garaipoom I love the electronic circuits. I will collect a lot of circuit electronics to teach my son and are useful for everyone., et al. “LM2596 Circuit Voltage Regulator and LM2673 Datasheet.” ElecCircuit.com, 19 July 2020, [www.eleccircuit.com/regulator-switching-dc-to-dc-step-down-voltage-with-lm2596/]( www.eleccircuit.com/regulator-switching-dc-to-dc-step-down-voltage-with-lm2596/.). 

* “LTC Debuts LTC4060 NiMH/NiCd Battery Charger - New Industry Products.” EEPower, [eepower.com/new-industry-products/ltc-debuts-ltc4060-nimhnicd-battery-charger/#]( eepower.com/new-industry-products/ltc-debuts-ltc4060-nimhnicd-battery-charger/#). 

* “Dual 4A Ideal Diodes with Adjustable Current Limit.” Datasheet, Linear Technology Co., [datasheet.datasheetarchive.com/originals/distributors/Datasheets-SFU1/DSASFU10008413.pdf]( datasheet.datasheetarchive.com/originals/distributors/Datasheets-SFU1/DSASFU10008413.pdf). 

* Zach-Goh. “Zach-Goh/Omron_LD_ROS_Package.” GitHub, [github.com/zach-goh/Omron_LD_ROS_Package](github.com/zach-goh/Omron_LD_ROS_Package). 

* “OMRON Industrial Automation.” OMRON, [www.ia.omron.com/]( www.ia.omron.com/). 
