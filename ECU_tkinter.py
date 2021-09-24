from tkinter import *

st_format = {'height': '1', 'width': '15', 'font': 'Courier, 15', 'wraplength': '200'}


# create buttons -------------------------------------------------------------------------------------------------------
def standard_button(frame, text, command):
    st_butt = Button(frame, text=text, command=command)
    st_butt.config(st_format)
    st_butt.pack()
    return st_butt


def button_grid(frame, col, row, text, command):
    st_butt = Button(frame, text=text, command=command)
    st_butt.config(st_format)
    st_butt.config(background='yellow')
    st_butt.grid(column=col, row=row)
    return st_butt


# create labels --------------------------------------------------------------------------------------------------------
def standard_label(frame, text):
    st_label = Label(frame, text=text)
    st_label.config(st_format)
    st_label.pack()
    return st_label


def label_grid(frame, col, row, text):
    st_label = Label(frame, text=text)
    st_label.config(st_format)
    # st_label.config(sticky='ns')
    st_label.grid(column=col, row=row, sticky='ns')
    return st_label

# end
