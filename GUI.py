#!/usr/bin/env python
# coding: utf-8

from tkinter import *
from tkinter import ttk
import PIL
from PIL import Image, ImageTk
import cv2
import datetime
import os, sys


class GUI():
    def __init__(self, running=False, width=800, height=600):
        self.running = running
        self.width, self.height = width, height
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.cap = None
        self.frame = None
        self.img_cap = None

        self.root = Tk()
        self.root.title("EECE5626 Image Processing & Pattern Recognition")

        self.mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        self.mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        ttk.Button(self.mainframe, text="Run", command=self.run_cam).grid(column=1, row=1, sticky=(N, W))
        ttk.Button(self.mainframe, text="Capture", command=self.cap_image).grid(column=1, row=2, sticky=W)
        ttk.Button(self.mainframe, text="Modify", command=self.mod_image).grid(column=1, row=5, sticky=W)
        ttk.Button(self.mainframe, text="Save Image", command=self.save_image).grid(column=5, row=10, sticky=E)

        self.img_panel = Label(self.mainframe, text="test image please ignore")
        self.img_panel.grid(column=2, row=1, columnspan=4, rowspan=4, sticky=W+E+N+S, padx=5, pady=5)

        for child in self.mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

        # Keybinds:
        #root.bind('<Return>', )
        self.root.bind('r', self.run_cam)
        self.root.bind('c', self.cap_image)
        self.root.bind('m', self.mod_image)
        self.root.bind('s', self.save_image)
        self.root.bind('<Escape>', lambda e: self.root.quit())


    # Callback Functions

    def run_cam(self):
        try:
            #print("open web cam here")
            if not self.running:
                self.cap = cv2.VideoCapture(0)
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
                self.running = True

            if self.running:
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

    def cap_image(self):
        try:
            print("capture image from web cam here")
            if self.running:
                # grab the current timestamp and use it to construct the
                # output path
                ts = datetime.datetime.now()
                filename = "{}.jpg".format(ts.strftime("%Y-%m-%d_%H-%M-%S"))
                p = os.path.sep.join((self.dir_path, filename))
        
                # save the file
                img = self.frame
                cv2.imwrite(p, img)
                self.img_cap = img
                print("[INFO] saved {}".format(filename))
                
                self.cap.release()
                cv2.destroyAllWindows()
                self.running = False
                imgtk = ImageTk.PhotoImage(image=img)
                self.img_panel.image = imgtk
                self.img_panel.configure(image=imgtk)

        except ValueError:
            pass

    def mod_image(self):
        try:
            print("modify image here")
        except ValueError:
            pass

    def save_image(self):
        try:
            print("save current image here")
        except ValueError:
            pass


if __name__ == "__main__":
    GUI().root.mainloop()