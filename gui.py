#!/usr/bin/python


import tkinter
import tkinter.messagebox
from tkinter import *
top = tkinter.Tk()

def helloCallBack():
   tkinter.messagebox.showinfo( "Hello Python", "Hello World")

B = tkinter.Button(top, text ="Hello", command = helloCallBack)

B.pack()

L1 = tkinter.Label(top, text="Vstart")
L1.pack( side = LEFT)
E1 = tkinter.Entry(top, bd =5)
E1.pack(side = RIGHT)

L2 = tkinter.Label(top, text="Vend")
L2.pack( side = LEFT)
E2 = tkinter.Entry(top, bd =5)
E2.pack(side = RIGHT)

L3 = tkinter.Label(top, text="Vstep")
L3.pack( side = LEFT)
E3 = tkinter.Entry(top, bd =5)
E3.pack(side = RIGHT)

top.mainloop()
