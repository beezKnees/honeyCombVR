import cv2
from cv2 import threshold
import numpy as np
import threading
import time
from tkinter import *
import os
is_on = True
valueR = 28
valueL = 18
multiplier = 4
left_slider = 0
right_slider = 0
two_cams = True
debug = True


cam = cv2.VideoCapture(2, cv2.CAP_DSHOW)
#cam2 = cv2.VideoCapture(2)
check, frame = cam.read()


def calibrate():
    if __name__ == '__main__' :
        
        # Read image
        check, im = cam.read()
        
    
        # Select ROI
        r = cv2.selectROI(im)
    
        cv2.waitKey(0)
        #cv2.destroyWindow("Image")
        cv2.destroyWindow("ROI selector")

        return r
def slider():
    root = Tk()
    root.title('Slider Box')

    def update(number):
        global left_slider
        global right_slider

        left_slider = vertical.get()
        right_slider = vertical2.get()


    def leave():
        os._exit(1)

    def norm():
        global is_on

        # Determine if button is on or off
        if is_on:
            is_on = False
        else:
            is_on = True




    vertical = Scale(root, from_=0, to=150, command=update)
    vertical.pack()

    vertical2 = Scale(root, from_=0, to=150, command=update)
    vertical2.pack()


    update = Button(root, text="Click me to exit", command=leave).pack()
    on_button = Button(root, text="Normalize", command = norm).pack()




    root.mainloop()






def eye(eye, value):
    global is_on
    y = 0
    x = 0
    roi = cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY)
    rows, cols = roi.shape
    roi = cv2.bilateralFilter(roi, 9, 20, 20)

    if is_on:
        #helps normalize the image in different lighting
        norm_img = np.zeros((800,800))
        roi = cv2.normalize(roi,  norm_img, 75, 255, cv2.NORM_MINMAX)



    _, threshold = cv2.threshold(roi, value, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = lambda x: cv2.contourArea(x), reverse=True)

    for cnt in contours:
        x, y, w, h = cv2.boundingRect(contours[0])
        cv2.rectangle(eye, (x, y), (x + w, y + h), (51, 87, 255), 1)
        cv2.line(eye, (x + int(w/2), 0), (x + int(w/2),rows), (255, 0, 0), 1)
        cv2.line(eye, (0, y + int(h/2)), (cols, y + int(h/2)), (255, 0, 0), 1)

        break

    return eye, (x,y)

def eye_main():
    global left_slider
    global right_slider
    global is_on
    valueR = 0
    valueL = 0
    multiplier = 1
    left_old = 0
    right_old = 0
    et = 0
    st = 0
    timeOld = 0
    r = calibrate()

    while True:


        if (debug):
            os.system('CLS')
            print("Having debug set to True does slow down the program")
            print("Left: ", left_slider)
            print("Right: ", right_slider)
            print("Normalizing: ", is_on)
            
            timeTaken = et - st
            if (timeTaken != 0.0):
                print("Runtime: ", timeTaken)
                timeOld = timeTaken
            else:
                print("Runtime: ", timeOld)

        valueR = right_slider
        valueL = left_slider


        check, frame = cam.read()
        st = time.time()
        #check2, frame2 = cam2.read()

        imCrop = frame[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]

        h, w, channels = imCrop.shape
        half = w//2

        roi1 = imCrop[:, :half]

        roi2 = imCrop[:, half:]

        eye1, coords_r = eye(roi2, valueR)

        eye2, coords_l = eye(roi1, valueL)

        hori = np.concatenate((eye2, eye1), axis = 1)

        height = (hori.shape[0] * multiplier)
        width = (hori.shape[1] * multiplier)

        hori = cv2.resize(hori, (width, height))

        hori = cv2.flip(hori, 1)
        cv2.imshow("hori", hori)
        et = time.time()


        key = cv2.waitKey(1)
        if key == 27:
            break
        if key == 114:
            r =calibrate()


t1 = threading.Thread(target=eye_main)
t1.start()

t2 = threading.Thread(target=slider)
t2.start()

#cam.release()
#cv2.destroyAllWindows()
