from tkinter import *

st_format = {'height': '1', 'width': '15', 'font': 'Courier, 15', 'wraplength': '200'}


def standard_button(frame, text, command):
    st_butt = Button(frame, text=text, command=command)
    st_butt.config(st_format)
    st_butt.pack()
    return st_butt


def standard_label(frame, text):
    st_label = Label(frame, text=text)
    st_label.config(st_format)
    st_label.pack()
    return st_label

# end
