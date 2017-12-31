from threading import Event, Thread
import sys
import cv2
from subprocess import *
import numpy as np
import time
import matplotlib.pyplot as plt

WIDTH = 720
HEIGHT = 576

def feedPipe():
    #time.sleep(5)
    while (1):
        while (process == -1):
            time.sleep(0.5)
            continue

        bytes = f.read(1000)
        #print('read {} from file'.format(bytes))
        #continue

        if(len(bytes) == 0):
            break

        print('write {} bytes to stdin'.format(len(bytes)))
        process.stdin.write(bytes)
        #process.stdin.flush()



if __name__ == '__main__':
    f = open('./video.avi', 'rb')
    process = -1
    #cv2.namedWindow('image')

    # cmd = ['ffmpeg',
    #        '-i', '-',
    #        '-f', 'image2pipe',
    #        '-pix_fmt', 'rgb24',
    #        '-vcodec', 'rawvideo', '-']

    cmd = ['ffmpeg',
           '-i', '-',
           'out.mp4'
           ]

    thread = Thread(target=feedPipe).start()
    #process = Popen(cmd, stdout=PIPE, stdin=PIPE)
    process = Popen(cmd, stdin=PIPE)

    while(1):
        time.sleep(1)
        continue

        #print('--------------before read bytes from stdin')
        bytes = process.stdout.read(WIDTH*HEIGHT*3)
        print('---------read {} bytes from stdin'.format(len(bytes)))
        if (len(bytes) == 0):
            break

        #process.stdout.flush()
        img = np.fromstring(bytes, dtype='uint8')
        img = img.reshape((HEIGHT, WIDTH, 3))
        plt.imshow(img)
        plt.xticks([]), plt.yticks([])

        plt.pause(0.0001)

