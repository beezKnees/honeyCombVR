import cv2
from cv2 import threshold
import numpy as np
import threading
import time
from tkinter import *
import os
valueR = 28
valueL = 18
multiplier = 4
left_slider = 0
right_slider = 0
two_cams = True
debug = False

cam = cv2.VideoCapture(0)
#cam2 = cv2.VideoCapture(2)


def slider():
    #from PIL import ImageTk,Image

    root = Tk()
    root.title('Slider Box')

    def update(number):
        global left_slider
        global right_slider

        left_slider = vertical.get()
        right_slider = vertical2.get()
        #os.system('CLS')
        #print("left: ", left_slider)
        #print("right: ", right_slider)


    def leave():
        exit()



    vertical = Scale(root, from_=0, to=100, command=update)
    vertical.pack()

    vertical2 = Scale(root, from_=0, to=100, command=update)
    vertical2.pack()


    update = Button(root, text="Click me to exit", command=leave).pack()



    root.mainloop()






def eye(eye, value):
    y = 0
    x = 0
    roi = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
    rows, cols = roi.shape
    roi = cv2.GaussianBlur(roi, (5, 5), 0)



    _, threshold = cv2.threshold(roi, value, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = lambda x: cv2.contourArea(x), reverse=True)

    for cnt in contours:
        #cv2.drawContours(eye, [cnt], -1, (0, 0, 255), 1)
        x, y, w, h = cv2.boundingRect(contours[0])
        cv2.rectangle(eye, (x, y), (x + w, y + h), (51, 87, 255), 1)
        cv2.line(eye, (x + int(w/2), 0), (x + int(w/2),rows), (255, 0, 0), 1)
        cv2.line(eye, (0, y + int(h/2)), (cols, y + int(h/2)), (255, 0, 0), 1)

        break

    return eye, (x,y)

def eye_main():
    global left_slider
    global right_slider
    valueR = 0
    valueL = 0
    multiplier = 4
    left_old = 0
    right_old = 0
    et = 0
    st = 0
    timeOld = 0

    while True:

        if (debug):
            os.system('CLS')
            print("left: ", left_slider)
            print("right: ", right_slider)
            timeTaken = et - st
            if (timeTaken != 0.0):
                print("Runtime: ", timeTaken)
                timeOld = timeTaken
            else:
                print("Runtime: ", timeOld)
            
        left_old = left_slider
        right_old = right_slider

        valueR = right_slider
        valueL = left_slider


        check, frame = cam.read()
        st = time.time()
        #check2, frame2 = cam2.read()
        roi1 = frame[270:300, 323:380]#[200:300, 180:480]

        roi2 = frame[270:300, 265:322]#[200:300, 180:480]

        eye1, coords_r = eye(roi2, valueR)

        eye2, coords_l = eye(roi1, valueL)

        hori = np.concatenate((eye1, eye2), axis = 1)
        verti = np.concatenate((eye1, eye2), axis = 0)

        height = (hori.shape[0] * multiplier)
        width = (hori.shape[1] * multiplier)

        hori = cv2.resize(hori, (width, height))

        cv2.imshow("hori", hori)
        et = time.time()

        #cv2.imshow("test", frame2)


        key = cv2.waitKey(1)
        if key == 27:
            break


t1 = threading.Thread(target=eye_main)
t1.start()

t2 = threading.Thread(target=slider)
t2.start()

#cam.release()
#cv2.destroyAllWindows()
