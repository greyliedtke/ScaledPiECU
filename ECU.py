import tkinter as tk
from tkinter import ttk
import time
from tkinter import *

loads = [0, 0, 0, 0, 0]
update_time = 100


def load_inc():
    loads[1] = loads[1] + 1
    return loads


# pre test window to trigger gpio stuff
def load_press(load_pin):
    print("triggered load:", load_pin)
    loads[load_pin] = 1 - loads[load_pin]


class PreTestWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('PreTest Window')
        self.resizable(0, 0)
        self.geometry('400x200')
        self['bg'] = 'black'

        option_list = range(5)
        ssr_buttons = [lambda i=i: load_press(option_list[i]) for i in range(len(option_list))]
        for b in range(5):
            butt = Button(self, text=b, command=ssr_buttons[b])
            butt.pack()

        self.lls = Label(self, text="Load States")
        self.lls.pack()
        self.l1 = Label(self, text=loads[0])
        self.l2 = Label(self, text=loads[1])
        l3 = Label(self, text=loads[2])
        l4 = Label(self, text=loads[3])
        self.l1.pack()
        self.l2.pack()
        self.lls.after(1000, self.update_load_state())

    def update_load_state(self):
        self.l1.config(text=loads[0])
        self.l2.config(text=loads[1])
        self.lls.after(1000, self.update_load_state)








class LoadControl(tk.Tk):
    def __init__(self):
        super().__init__()

        # configure the root window
        self.title('ECU Control')
        self.resizable(0, 0)
        self.geometry('400x200')
        self['bg'] = 'black'

        # change the background color to black
        self.style = ttk.Style(self)
        self.style.configure(
            'TLabel',
            background='black',
            foreground='red')

        # Buttons
        self.pretest_button = ttk.Button(self, text="Pre-Test", command=lambda: PreTestWindow())
        self.pretest_button.pack()

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



if __name__ == "__main__":
    clock = LoadControl()
    clock.mainloop()


# end
