"""File that has all the usefull gui creation tools"""

from tkinter import *


# ------------------------------------------ Create Widgets ------------------------------------------------------------
class CreateWidget:
    def __init__(self, **kargs):
        self.w_type = kargs.get("w_type")
        w_frame = kargs.get("w_frame")
        w_cont = kargs.get("w_cont")
        self.widget = Label(w_frame, text=w_cont)
        if self.w_type == 'Label':
            label = Label(w_frame, text=w_cont)
            self.widget = label
        if self.w_type == 'Button':
            button = Button(w_frame, text=w_cont[0], command=w_cont[1])
            self.widget = button

        if self.w_type == 'Entry':
            entry = Entry(w_frame, text=w_cont)
            entry.delete(0, END)
            entry.insert(END, w_cont)
            self.widget = entry
        if self.w_type == 'Drop Down':
            options = w_cont[1]
            self.d_options = options
            self.widget = StringVar(w_frame)
            self.widget.set(w_cont[0])
            self.dropdown = OptionMenu(w_frame, self.widget, *options)
            self.config = self.dropdown.config
            return
        self.config = self.widget.config
        self.pack = self.widget.pack
        self.grid = self.widget.grid


class CreatePackWidget(CreateWidget):
    def __init__(self, **kargs):
        super().__init__(**kargs)
        if self.w_type == 'Label':
            label_format = {'height': '1', 'width': '15', 'font': 'Courier, 15'}
            self.config(**label_format)
        if self.w_type == 'Button':
            more_config = kargs.get("more_config")
            button_format = {'height': '4', 'width': '15', 'font': 'Courier, 15', 'wraplength': '200'}
                             #'color': 'light sky blue'},
                             # 'background': 'light sky blue', 'foreground': 'white'
            # if more_config is not None:
            #     button_format = {more_config}
            #     print(button_format)
            self.config(**button_format)
            #self.config(background='light sky blue')
            self.pack(fill=X, padx=10, pady=5, side=TOP)
            return

        if self.w_type == 'Entry':
            entry_format = {'width': '30', 'font': '10'}
            self.config(**entry_format)
        if self.w_type == 'Drop Down':
            self.dropdown.pack(fill=BOTH)
            return
        self.pack()


class CreateGridWidget(CreateWidget):
    def __init__(self, **kargs):
        super().__init__(**kargs)
        coordinates = kargs.get("coordinates")
        if self.w_type == 'Label':
            label_format = {'height': '1', 'width': '15', 'font': 'Courier, 10'}
            self.config(**label_format)
        if self.w_type == 'Button':
            button_format = {'height': '1', 'width': '15', 'font': 'Courier, 10'}
            self.config(**button_format)
        if self.w_type == 'Entry':
            entry_format = {'width': '15', 'font': 'Courier, 10'}
            self.config(**entry_format)
        if self.w_type == 'Drop Down':
            self.dropdown.grid(row=coordinates[0], column=coordinates[1], sticky=W+E)
            return
        self.grid(row=coordinates[0], column=coordinates[1])


# ------------------------------------------ Create Window/Frame -------------------------------------------------------
def create_window(window_name):
    window_gui = Tk(className=window_name)
    window_gui.geometry("1000x800")
    return window_gui


def create_frame(gui, frame_type='Normal', pack='Yes'):
    # Function to clear contents of gui and return frame
    if pack == 'Yes':
        widgets = gui.pack_slaves()
        for widget in widgets:
            widget.destroy()
    if frame_type == 'Scroll':
        frame = ScrollWindow(gui)
    else:
        frame = Frame(gui)
        frame.pack(expand=True, fill=BOTH)
    return frame


class ScrollWindow:
    # Class to create Scrolling Window Frame. (including back button)
    def __init__(self, window_gui):
        self.outer_frame = Frame(window_gui, width=100)
        self.outer_frame.pack(fill=BOTH, expand=1)                   # Create a main frame
        sub_canvas = Canvas(self.outer_frame)
        sub_canvas.pack(side=LEFT, fill=BOTH, expand=1)       # Create a canvas
        y_scrollbar = Scrollbar(self.outer_frame, orient=VERTICAL, command=sub_canvas.yview)
        y_scrollbar.pack(side=RIGHT, fill=Y)  # Add scroll bar
        x_scrollbar = Scrollbar(self.outer_frame, orient=HORIZONTAL, command=sub_canvas.xview)
        x_scrollbar.pack(side=BOTTOM, fill=X)
        sub_canvas.configure(yscrollcommand=y_scrollbar.set, xscrollcommand=x_scrollbar.set)
        sub_canvas.bind('<Configure>', lambda e: sub_canvas.configure(scrollregion=sub_canvas.bbox("all")))
        self.scroll_frame = Frame(sub_canvas)  # Create inner frame
        sub_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")


# ------------------------------------------ Common functions ----------------------------------------------------------
# used for creating commands and buttons in a loop. first input is command, then array of command inputs... confusing
def button_in_loop(command, option_list):
    # function that can generate button commands in a loop... work more on this
    loop_funcs = []
    if len(option_list) == 3:
        loop_funcs = [lambda i=i: command(option_list[0][i], option_list[1], option_list[2])
                      for i in range(len(option_list[0]))]
    if len(option_list) == 2:
        loop_funcs = [lambda i=i: command(option_list[0][i], option_list[1:]) for i in range(len(option_list[0]))]
    if len(option_list) == 1:
        loop_funcs = [lambda i=i: command(option_list[i]) for i in range(len(option_list))]
    return loop_funcs


# Generate labels for a grid interface interface
def table_labels(row, frame, labels):
    for p in range(len(labels)):
        CreateGridWidget(w_type='Label', w_frame=frame, w_cont=labels[p], coordinates=[row, p])


# Wipes row to allow for other population
def ds_wipe_row(row, frame):
    # Function to wipe out row of contents
    try:
        widgets = frame.grid_slaves(row=row)
        for delete_widget in range(len(widgets)):
            widgets[delete_widget].destroy()
    except IndexError:
        return