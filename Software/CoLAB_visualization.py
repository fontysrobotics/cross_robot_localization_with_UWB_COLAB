import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

from CoLAB_main import AGVMap
import CoLAB_sendLocation as sendLocation

fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    xar = []
    yar = []

    for j in range(0, len(AGVMap)):
        xar.append(AGVMap[j][2][0] - sendLocation.preProcessedLocation[0])
        yar.append(AGVMap[j][2][1] - sendLocation.preProcessedLocation[1])

    ax1.clear()
    ax1.plot(xar,yar,"o")

    # Move left y-axis and bottom x-axis to centre, passing through (0,0)
    ax1.spines['left'].set_position('zero')
    ax1.spines['bottom'].set_position('zero')
    # Eliminate upper and right axes
    ax1.spines['right'].set_color('none')
    ax1.spines['top'].set_color('none')

    # Show ticks in the left and lower axes only
    ax1.xaxis.set_ticks_position('bottom')
    ax1.yaxis.set_ticks_position('left')
 
    ax1.set_xlim([-10, 10])
    ax1.set_ylim([-10, 10])


ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()