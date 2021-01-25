
import numpy as np
InRangeCount = 0
InRangeLocation = np.empty((0,2),int)
AGVLoc = np.empty((0,2), int); #data recieved x,y,angle?
XBound = (MidX + 2500, MidX - 2500) #in mm
YBound = (MidY + 2500, MidY - 2500)
DataWrite = False

DistancetoAGV = 0
AngletoAGV = 0

AGVMap = np.empty((0,3),int) 
length = np.empty((0,1),int)

AGVID = Integer.parseInt(payload("CoLAB_ID")) ##(String) jsonCRL.get("AGVID")
X = Integer.parseInt(payload["location"][0])
Y = Integer.parseInt(payload["location"][1])
Orientation = Integer.parseInt(payload("Orientation"))
AGVLoc = (X,Y,Orientation)
#is this how location can be filtered or is it named something else
if AGVLoc[0] < XBound[0] and AGVLoc[0] > XBound[1] and AGVLoc[1] < YBound[0] and AGVLoc[1] > YBound[1]: #shoudl the agv id be added to final array so each agv will only be plotted once
    InRangeLocation = np.append(InRangeLocation, AGVLoc, axis = 0) 
    InRangeCount = InRangeCount + 1

DistancetoAGV = int( np.sqrt(np.power(InRangeLocation[InRangeCount, 0]- MidX,2) + np.power(InRangeLocation[InRangeCount, 1]- MidY,2)))
AngletoAGV = np.arctan2((InRangeLocation[InRangeCount, 1]- MidY)/(InRangeLocation[InRangeCount, 0]- MidX)) * 180/np.pi

info = (DistancetoAGV, AngletoAGV, AGVID, Orientation)
length = AGVMap.shape
range = length[0]
for i in range (0, range):
    if AGVMap[i, 2] == AGVID:
        AGVMap[i, 0] = info[0]
        AGVMap[i, 1] = info[1]
        AGVMap[i, 3] = info[3]
        DataWrite = True
if DataWrite == False:
    AGVMap = np.append(AGVMap, info, axis = 0)