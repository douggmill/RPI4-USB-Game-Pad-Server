#### RPI4 USB Controller Server ****

import time # python standard module
from evdev import list_devices, InputDevice, categorize, ecodes # pip install evdev
import evdev # pip install evdev
from select import select # python standard module
import socket # pip install socket
import configparser #pip install configparser
connected = False
P1connected = False
P2connected = False
P3connected = False
P4connected = False

config = configparser.ConfigParser()
config.read('config.txt')
P1name = config['Player1']['name']
P2name = config['Player2']['name']
P3name = config['Player3']['name']
P4name = config['Player4']['name']
    

def connectSocket():
    global connect, connected, sendSocket, sock, P1connected, P2connected, P3connected, P4connected
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('192.168.8.105', 8888))
    sock.listen()
    connect, addr = sock.accept()
    sendSocket=""
    connected = True
    P1connected = False
    P2connected = False
    P3connected = False
    P4connected = False
connectSocket()

def evdevPaths():
    global devices, paths, P1name, P2name, P3name, P4name, P1connected, P2connected, P3connected, P4connected
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    paths=[]
    for device in devices:
        print(device.path, device.name, device.phys)
        #print(P1connected)
        #print(devices)
        if P1name == device.name and P1connected==False:
            paths.append(device.path)
            print('found P1')
            P1connected=True
            #print(device.capabilities())
        elif P2name == device.name and P2connected==False:
            paths.append(device.path)
            print('found P2')
            P2connected=True
            #print(device.capabilities())
        elif P3name == device.name and P3connected==False:
            paths.append(device.path)
            print('found P3')
            P3connected=True
            #print(device.capabilities())
        elif P4name == device.name and P4connected==False:
            paths.append(device.path)
            print('found P4')
            P4connected=True
            #print(device.capabilities()

    devices = map(InputDevice, (paths))
    devices = {dev.fd: dev for dev in devices}
    i=1
    for key in devices:
        playerKey=str(key)+',P'+str(i)+',Connected:'
        #print(playerKey)
        connect.send(playerKey.encode())
        i+=1
evdevPaths()

def sendMsg():
    global sendSocket, connect
    r, w, x = select(devices, [], [])
    for fd in r:
        for event in devices[fd].read():
            if event.type == ecodes.EV_KEY:
                sendSocket=str(fd)+','+str(event.code)+','+str(event.value)+':'
                connect.send(sendSocket.encode())
            if event.type == ecodes.EV_ABS:
                if event.code == 0 or event.code == 1:
                    ts = time.time() * 10000
                    sendSocketTs=event.timestamp() * 10000
                    mSec = ts - sendSocketTs
                    if mSec < 3: # and event.value % 2 == 0: # timestamp < .2s and value == even
                        sendSocket=str(fd)+','+str(event.code)+','+str(event.value)+':'
                        connect.send(sendSocket.encode())
                    elif mSec >= 3 and event.value == 128: # recover zero value
                        sendSocket=str(fd)+','+str(event.code)+','+str(event.value)+':'
                        connect.send(sendSocket.encode())
                else:
                    sendSocket=str(fd)+','+str(event.code)+','+str(event.value)+':'
                    connect.send(sendSocket.encode())

while True:
    if(not connected):
        try:
            connectSocket()
            evdevPaths()
            print("Server connected")
            connected = True
        except:
            pass
    else:
        try:
            sendMsg()
        except:
            print("Server not connected")
            connected = False
            pass
s.close

