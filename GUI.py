#!/usr/bin/env python
# coding: utf-8

# In[1]:

from tkinter import *
from tkinter import ttk


# In[2]:
# Callback Functions

def calculate(*args):
    try:
        value = float(feet.get())
        meters.set((0.3048 * value * 10000.0 + 0.5)/10000.0)
    except ValueError:
        pass

def run_cam(*args):
    try:
        print("open web cam here")
    except ValueError:
        pass

def cap_image(*args):
    try:
        print("capture image from web cam here")
    except ValueError:
        pass

def mod_image(*args):
    try:
        print("modify image here")
    except ValueError:
        pass

def save_image(*args):
    try:
        print("save current image here")
    except ValueError:
        pass

# In[3]:


root = Tk()
root.title("EECE5626 Image Processing & Pattern Recognition")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, S, E, W))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)


# In[4]:


feet = StringVar()
meters = StringVar()

gui = ttk.Entry(mainframe, width=50, textvariable=feet)
gui.grid(column=2, row=1, sticky=(W, E))


# In[5]:

ttk.Button(mainframe, text="Run", command=run_cam).grid(column=1, row=1, sticky=(N, W))
ttk.Button(mainframe, text="Capture", command=cap_image).grid(column=1, row=2, sticky=W)
ttk.Button(mainframe, text="Modify", command=mod_image).grid(column=1, row=5, sticky=W)
ttk.Button(mainframe, text="Save Image", command=save_image).grid(column=5, row=10, sticky=E)

ttk.Label(mainframe, textvariable=meters).grid(column=3, row=2, sticky=(W, E))
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)
ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=2, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=4, row=2, sticky=W)


# In[6]:

for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

# In[7]:
# Keybinds:
gui.focus()
root.bind('<Return>', calculate)
root.bind('r', run_cam)
root.bind('c', cap_image)
root.bind('m', mod_image)
root.bind('s', save_image)
root.bind('<Escape>', lambda e: root.quit())

# In[8]:

root.mainloop()

