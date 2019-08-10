#!/usr/bin/env python
# coding: utf-8

from tkinter import *
from tkinter import ttk
import PIL
from PIL import Image, ImageTk
import cv2
import datetime
import os, sys
import numpy as np

# ############################################################################
# Filter Imports and List
# ############################################################################
import moustache as ms
import beard as bd
import gaussian as gf


FILTERS = [ ('MOUSTACHE', ms.moustache), \
            ('BEARD', bd.beard), \
            ('FFT', None), \
            ('DFT', None), \
            ('GAUSSIAN NOISE', gf.gaussian), \
            ('RANDOM', None), \
            ]

# ############################################################################
# GUI Class
# ############################################################################
class GUI():
    def __init__(self, master):
        self.running = False
        self.width, self.height = 1000, 1000
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.cap = None
        self.frame = None
        self.img_cap = None
        self.capture = False

        ############################################################################
        # Root Window
        ############################################################################
        mainframe = ttk.Frame(master, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, S, E, W))

        ############################################################################
        # Buttons:
        ############################################################################
        self.run_b = ttk.Button(mainframe, text="Run", command=self.run_cam)
        self.run_b.grid(column=0, row=1, sticky=(N, W))
        self.cap_b = ttk.Button(mainframe, text="Capture", command=self.cap_image)
        self.cap_b.grid(column=0, row=2, sticky=W)
        self.mod_b = ttk.Button(mainframe, text="Modify", command=self.mod_image)
        self.mod_b.grid(column=0, row=5, sticky=W)
        self.sav_b = ttk.Button(mainframe, text="Save Image", command=self.save_image)
        self.sav_b.grid(column=5, row=10, sticky=E)

        ############################################################################
        # Listbox:
        ############################################################################
        self.lb = Listbox(mainframe, height=5)
        self.lb.grid(column=0, row=4, sticky=W)
        sb = ttk.Scrollbar(mainframe, orient=VERTICAL, command=self.lb.yview)
        sb.grid(column=1, row=4, sticky=W)
        self.lb['yscrollcommand'] = sb.set

        for i in FILTERS:
            self.lb.insert('end', i[0])

        ############################################################################
        # Image Panel:
        ############################################################################
        self.img_panel = Label(mainframe, text="test image please ignore")
        self.img_panel.grid(column=2, row=1, columnspan=4, rowspan=4, sticky=W+E+N+S, padx=5, pady=5)

        ############################################################################
        # Grid Setup
        ############################################################################
        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)
        
        ############################################################################
        # Keybinds:
        ############################################################################
        master.bind('r', self.run_cam)
        master.bind('c', self.cap_image)
        master.bind('m', self.mod_image)
        master.bind('s', self.save_image)
        master.bind('<Escape>', lambda e: master.quit())

    ############################################################################
    # Callback Functions
    ############################################################################
    def run_cam(self, event=None):
        try:
            #print("open and run web cam here")
            if not self.running:
                print("[INFO]: Starting Video Stream")
                self.cap = cv2.VideoCapture(0)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                self.running = True
                self.capture = False

            if self.running:
                if self.capture:
                    print("[INFO]: Displaying Captured Image")
                    self.running = False
                    imgtk = ImageTk.PhotoImage(image=self.img_cap)
                    self.img_panel.configure(image=imgtk)
                    self.img_panel.image = imgtk
                    self.cap.release()
                    cv2.destroyAllWindows()

                elif not self.capture:
                    #print("[INFO]: VS Running")
                    _, self.frame = self.cap.read()
                    self.frame = cv2.flip(self.frame, 1)
                    cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
                    img = PIL.Image.fromarray(cv2image)
                    imgtk = ImageTk.PhotoImage(image=img)
                    self.img_panel.imgtk = imgtk
                    self.img_panel.configure(image=imgtk)
                    self.img_panel.after(10, self.run_cam)

        except ValueError:
            pass

    def cap_image(self, event=None):
        try:
            #print("capture image from web cam here")
            if self.running:
                print("[INFO]: Image Capture Requested")
                self.capture = True

                # grab the current timestamp and use it to construct the output path
                ts = datetime.datetime.now()
                filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
                img_pth = os.path.sep.join((self.dir_path, filename))
        
                # save the file
                img = self.frame
                cv2.imwrite(img_pth, img)
                self.img_cap = Image.open(img_pth)
                print("[INFO]: Saved capture as: {}".format(filename))

        except ValueError:
            pass

    def mod_image(self, event=None):
        try:
            #print("modify image here")
            
            # get the current selection in the list box
            idx = self.lb.curselection()

            # the expectation here is that only the displayed image is supplied to 
            # the function, and that image is then overwritten by the return image
            if idx:
                self.img_cap = FILTERS[idx[0]][1](self.img_cap)

            # display the updated image
            imgtk = ImageTk.PhotoImage(image=self.img_cap)
            self.img_panel.configure(image=imgtk)
            self.img_panel.image = imgtk

        except ValueError:
            pass

    def save_image(self, event=None):
        try:
            #print("save current image here")

            # grab the current timestamp and use it to construct the output path
            ts = datetime.datetime.now()
            filename = "{}_USER_SAVE.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
            img_pth = os.path.sep.join((self.dir_path, filename))
    
            # save the file
            img = cv2.cvtColor(np.asarray(self.img_cap), cv2.COLOR_RGBA2BGRA)
            cv2.imwrite(img_pth, img)
            print("[INFO]: Saved image as: {}".format(filename))

        except ValueError:
            pass

############################################################################
if __name__ == "__main__":
    root = Tk()
    root.title("EECE5626 Image Processing & Pattern Recognition")
    app = GUI(root)
    root.mainloop()