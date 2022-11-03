
from tkinter import *
import os

#from PIL import ImageTk,Image

root = Tk()
root.title('Slider Box')




def update(number):

    left_slider = vertical.get()
    right_slider = vertical2.get()
    os.system('CLS')
    print("left: ", left_slider)
    print("right: ", right_slider)


vertical = Scale(root, from_=0, to=255, command=update)
vertical.pack()

vertical2 = Scale(root, from_=0, to=255, command=update)
vertical2.pack()


#update = Button(root, text="Click me to update", command=update).pack()



root.mainloop()
