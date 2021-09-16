import tkinter as tk
from tkinter import ttk
import time
from tkinter import *

loads = [0, 0, 0, 0, 0]
update_time = 100


def load_inc():
    loads[1] = loads[1] + 1
    return loads


def but_press():
    loads[2] += 1



class LoadControl(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Digital Clock')
        self.resizable(0, 0)
        self.geometry('400x200')
        self['bg'] = 'black'

        # change the background color to black
        self.style = ttk.Style(self)
        self.style.configure(
            'TLabel',
            background='black',
            foreground='red')

        # labels
        self.lab1 = ttk.Label(
            self,
            text=loads[0],
            font=('Digital-7', 40))
        self.lab1.pack(expand=True)
        self.lab2 = ttk.Label(
            self,
            text=loads[2],
            font=('Digital-7', 40))
        self.lab2.pack(expand=True)
        self.lab3 = ttk.Label(
            self,
            text=loads[2],
            font=('Digital-7', 40))
        self.lab3.pack(expand=True)

        # schedule an update every 1 second
        self.lab1.after(update_time, self.update)

    fuel_window = Tk(className="Fuel")
    fuel_window.geometry("1000x800")
    fuel_frame = Frame(fuel_window)
    fuel_frame.pack()
    button = Button(fuel_frame, text="Press me!", command=lambda: but_press())
    button.pack()


    def time_string(self):
        return time.strftime('%H:%M:%S')

    def update(self):
        """ update the label every 1 second """

        loads_update = load_inc()
        self.lab1.configure(text=self.time_string())
        self.lab2.configure(text=loads_update[1])
        self.lab3.configure(text=loads_update[2])

        # schedule another timer
        self.lab1.after(update_time, self.update)


class FuelControl(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('Fuel Control')
        self.resizable(0, 0)
        self.geometry('400x200')
        self['bg'] = 'black'

        # change the background color to black
        self.style = ttk.Style(self)
        self.style.configure(
            'TLabel',
            background='black',
            foreground='red')

        # labels
        self.lab1 = ttk.Label(
            self,
            text=loads[0],
            font=('Digital-7', 40))
        self.lab1.pack(expand=True)
        self.lab2 = ttk.Label(
            self,
            text=loads[2],
            font=('Digital-7', 40))
        self.lab2.pack(expand=True)

        # schedule an update every 1 second
        self.lab1.after(update_time, self.update)

    def time_string(self):
        return time.strftime('%H:%M:%S')

    def update(self):
        """ update the label every 1 second """

        loads_update = load_inc()
        self.lab1.configure(text=self.time_string())
        self.lab2.configure(text=loads_update[1])

        # schedule another timer
        self.lab1.after(1000, self.update)


if __name__ == "__main__":
    clock = LoadControl()
    clock.mainloop()


# end
