
import socket
import time
import timerThread
import channels
from threading import Event, Thread
import sys, select
import cv2
from subprocess import *
import numpy as np


DRONE_IP = '172.16.10.1'
TCP_PORT = 8888
UDP_PORT = 8895
BUFFER_SIZE = 8192
WIDTH = 720
HEIGHT = 576

magicBytesCtrl = bytes([
		0x49, 0x54, 0x64, 0x00, 0x00, 0x00, 0x5D, 0x00, 0x00, 0x00, 0x81, 0x85, 0xFF, 0xBD, 0x2A, 0x29, 0x5C, 0xAD, 0x67, 0x82, 0x5C, 0x57, 0xBE, 0x41, 0x03, 0xF8, 0xCA, 0xE2, 0x64, 0x30, 0xA3, 0xC1,
		0x5E, 0x40, 0xDE, 0x30, 0xF6, 0xD6, 0x95, 0xE0, 0x30, 0xB7, 0xC2, 0xE5, 0xB7, 0xD6, 0x5D, 0xA8, 0x65, 0x9E, 0xB2, 0xE2, 0xD5, 0xE0, 0xC2, 0xCB, 0x6C, 0x59, 0xCD, 0xCB, 0x66, 0x1E, 0x7E, 0x1E,
		0xB0, 0xCE, 0x8E, 0xE8, 0xDF, 0x32, 0x45, 0x6F, 0xA8, 0x42, 0xEE, 0x2E, 0x09, 0xA3, 0x9B, 0xDD, 0x05, 0xC8, 0x30, 0xA2, 0x81, 0xC8, 0x2A, 0x9E, 0xDA, 0x7F, 0xD5, 0x86, 0x0E, 0xAF, 0xAB, 0xFE,
		0xFA, 0x3C, 0x7E, 0x54, 0x4F, 0xF2, 0x8A, 0xD2, 0x93, 0xCD
	])

magicBytesVideo1 = [bytes(
		[0x49, 0x54, 0x64, 0x00, 0x00, 0x00, 0x52, 0x00, 0x00, 0x00, 0x0F, 0x32, 0x81, 0x95, 0x45, 0x2E, 0xF5, 0xE1, 0xA9, 0x28, 0x10, 0x86, 0x63, 0x17, 0x36, 0xC3, 0xCA, 0xE2, 0x64, 0x30, 0xA3, 0xC1,
        0x5E, 0x40, 0xDE, 0x30, 0xF6, 0xD6, 0x95, 0xE0, 0x30, 0xB7, 0xC2, 0xE5, 0xB7, 0xD6, 0x5D, 0xA8, 0x65, 0x9E, 0xB2, 0xE2, 0xD5, 0xE0, 0xC2, 0xCB, 0x6C, 0x59, 0xCD, 0xCB, 0x66, 0x1E, 0x7E, 0x1E,
        0xB0, 0xCE, 0x8E, 0xE8, 0xDF, 0x32, 0x45, 0x6F, 0xA8, 0x42, 0xB7, 0x33, 0x0F, 0xB7, 0xC9, 0x57, 0x82, 0xFC, 0x3D, 0x67, 0xE7, 0xC3, 0xA6, 0x67, 0x28, 0xDA, 0xD8, 0xB5, 0x98, 0x48, 0xC7, 0x67,
        0x0C, 0x94, 0xB2, 0x9B, 0x54, 0xD2, 0x37, 0x9E, 0x2E, 0x7A]), bytes(
		[0x49, 0x54, 0x64, 0x00, 0x00, 0x00, 0x52, 0x00, 0x00, 0x00, 0x54, 0xB2, 0xD1, 0xF6, 0x63, 0x48, 0xC7, 0xCD, 0xB6, 0xE0, 0x5B, 0x0D, 0x1D, 0xBC, 0xA8, 0x1B, 0xCA, 0xE2, 0x64, 0x30, 0xA3, 0xC1,
        0x5E, 0x40, 0xDE, 0x30, 0xF6, 0xD6, 0x95, 0xE0, 0x30, 0xB7, 0xC2, 0xE5, 0xB7, 0xD6, 0x5D, 0xA8, 0x65, 0x9E, 0xB2, 0xE2, 0xD5, 0xE0, 0xC2, 0xCB, 0x6C, 0x59, 0xCD, 0xCB, 0x66, 0x1E, 0x7E, 0x1E,
        0xB0, 0xCE, 0x8E, 0xE8, 0xDF, 0x32, 0x45, 0x6F, 0xA8, 0x42, 0xB7, 0x33, 0x0F, 0xB7, 0xC9, 0x57, 0x82, 0xFC, 0x3D, 0x67, 0xE7, 0xC3, 0xA6, 0x67, 0x28, 0xDA, 0xD8, 0xB5, 0x98, 0x48, 0xC7, 0x67,
        0x0C, 0x94, 0xB2, 0x9B, 0x54, 0xD2, 0x37, 0x9E, 0x2E, 0x7A])
	]
magicVideoIdx = 0

magicBytesVideo2 = bytes([
		0x49, 0x54, 0x64, 0x00, 0x00, 0x00, 0x58, 0x00, 0x00, 0x00, 0x80, 0x86, 0x38, 0xC3, 0x8D, 0x13, 0x50, 0xFD, 0x67, 0x41, 0xC2, 0xEE, 0x36, 0x89, 0xA0, 0x54, 0xCA, 0xE2, 0x64, 0x30, 0xA3, 0xC1,
        0x5E, 0x40, 0xDE, 0x30, 0xF6, 0xD6, 0x95, 0xE0, 0x30, 0xB7, 0xC2, 0xE5, 0xB7, 0xD6, 0x5D, 0xA8, 0x65, 0x9E, 0xB2, 0xE2, 0xD5, 0xE0, 0xC2, 0xCB, 0x6C, 0x59, 0xCD, 0xCB, 0x66, 0x1E, 0x7E, 0x1E,
        0xB0, 0xCE, 0x8E, 0xE8, 0xDF, 0x32, 0x45, 0x6F, 0xA8, 0x42, 0xEB, 0x20, 0xBE, 0x38, 0x3A, 0xAB, 0x05, 0xA8, 0xC2, 0xA7, 0x1F, 0x2C, 0x90, 0x6D, 0x93, 0xF7, 0x2A, 0x85, 0xE7, 0x35, 0x6E, 0xFF,
        0xE1, 0xB8, 0xF5, 0xAF, 0x09, 0x7F, 0x91, 0x47, 0xF8, 0x7E
	])

data = bytes([0xCC, 0x7F, 0x7F, 0x0, 0x7F, 0x0, 0x7F, 0x33])

def sendMagicPacket1():
    channels.tcpSocketVideo1.send(magicBytesVideo1[0])
    #time.sleep(1)
    channels.tcpSocketVideo1.send(magicBytesVideo1[1])
    #time.sleep(1)
    print('sendMagicPacket1')

def sendMagicPacket2():
    channels.tcpSocketVideo2.send(magicBytesVideo2)
    print('sendMagicPacket2')

def sendUdp():
    sent = channels.udpSocket.sendto(data, (DRONE_IP, UDP_PORT))
    print('sendUdp - {} bytes'.format(sent))

def sendAllPackets():
    sendUdp()
    sendMagicPacket1()
    sendMagicPacket2()

def initComm():
    channels.udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    channels.udpSocket.bind(('0.0.0.0', UDP_PORT))

    channels.tcpSocketControl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    channels.tcpSocketControl.connect((DRONE_IP, TCP_PORT))

    channels.tcpSocketVideo1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    channels.tcpSocketVideo1.connect((DRONE_IP, TCP_PORT))

    channels.tcpSocketVideo2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    channels.tcpSocketVideo2.connect((DRONE_IP, TCP_PORT))

def closeComm():
    channels.tcpSocketVideo1.close()
    channels.tcpSocketVideo2.close()
    channels.tcpSocketControl.close()
    channels.udpSocket.close()

def resetComm():

    print('enter resetCom')
    closeComm()
    time.sleep(0.05)
    initComm()
    sendAllPackets()
    channels.stopListen = False
    startListen(channels.tcpSocketVideo2)


def startListen(tcpSocket):
    try:

        count = 0
        print('enter startLisen\n')
        while (not channels.stopListen):
            count = count +1
            msg = tcpSocket.recv(65000)
            if(count >= 20):
                end = '\n'
                count = 0
            else:
                end = ', '

            print(len(msg), sep=', ', end=end, file=sys.stdout)

            if len(msg) == 40:
                #print(msg)
                continue

            process.stdin.write(msg)
            #f.write(msg)
    except Exception as e:
        print("startListen error", e)

    print('exiting startListen')
    f.close()

def userListener():
    input("Press Enter to exit...\n")
    print('Enter pressed ')
    channels.stopListen = True
    stopFlag.set()

if __name__ == '__main__':
    f = open('./video.avi', 'wb')
    channels = channels.Channels()
    initComm()
    sendAllPackets()
    stopFlag = Event()
    cmd = ['ffplay','-i', '-']
    process = Popen(cmd, stdin=PIPE)
    timer = timerThread.Timer(stopFlag,resetComm, channels, 10)
    timer.start()
    stopThread = Thread(target=userListener).start()
    startListen(channels.tcpSocketVideo2)

    timer.join()
    process.kill()
    f.close()
    closeComm()
    print('finished')




