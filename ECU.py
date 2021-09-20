import tkinter as tk
from tkinter import ttk
import time
from tkinter import *
from ECU_load import *
from ECU_gpios import *
from ECU_tkinter import *

update_time = 100


# State machine to handle everything...
class ECUState:
    def __init__(self):
        self.state = "OFF"
        self.igniter = "OFF"
        self.pumps = "OFF"
        self.state_time = 0

    def set_state(self, state):
        self.state_time = 0
        self.state = state
        if state == "OFF":
            self.igniter = "OFF"
            self.pumps = "OFF"

        elif state == "LIGHTOFF":
            self.igniter = "ON"
            self.pumps = "ON"

        elif state == "IDLE":
            self.igniter = "OFF"
            self.pumps = "ON"

        elif state == "RUNNING":
            self.igniter = "OFF"
            self.pumps = "ON"

        else:
            print("fault!")
        return


# function to handle presses of control button
def control_button():
    if ecu.state == "OFF":
        ecu.set_state("LIGHTOFF")

    elif ecu.state == "RUNNING":
        ecu.set_state("OFF")

    else:
        print("ignored")
    return


# ecu state controller
ecu = ECUState()


# testing window gui
class TestWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Test Window')
        self.resizable(0, 0)
        self.geometry('200x800')
        self['bg'] = 'black'

        # load bank
        self.load_up_button = standard_button(self, "Load Up", command=lambda: res_load.change_load(inc=1))
        self.load_down_button = standard_button(self, "Load Down", command=lambda: res_load.change_load(inc=-1))
        self.lll = standard_label(self, res_load.level)
        self.lls = standard_label(self, "Load States")
        self.load_labels = []
        for ll in range(5):
            label = standard_label(self, ll)
            self.load_labels.append(label)

        # control buttons
        self.control_button = standard_button(self, "Control Button", command=lambda: control_button())
        self.control_label = standard_label(self, ecu.state)
        self.control_time = standard_label(self, ecu.state_time)

        # system status's
        self.igniter_label = standard_label(self, "Igniter: " + ecu.igniter)
        self.pump_label = standard_label(self, "Fuel Pump: " + ecu.pumps)
        self.occ_status = standard_label(self, "OCC Status: " + ecu_gpios.occ_status)

        # screen refresh rate
        self.lls.after(1000, self.update_state())

    def update_state(self):
        if ecu.state == "LIGHTOFF" and ecu.state_time == 5:
            ecu.set_state("IDLE")

        elif ecu.state == "IDLE" and ecu.state_time == 5:
            ecu.set_state("RUNNING")

        self.lll.config(text=res_load.level)
        self.control_label.config(text=ecu.state)
        self.control_time.config(text=ecu.state_time)
        self.igniter_label.config(text="Igniter: " + ecu.igniter)
        self.pump_label.config(text="Fuel Pumps " + ecu.pumps)

        for ll in range(len(self.load_labels)):
            self.load_labels[ll].config(text=load_state[ll])

        ecu.state_time += 1
        self.lls.after(1000, self.update_state)


tw = TestWindow()


# pre-test window to test gpio stuff
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
            butt = standard_button(self, b, ssr_buttons[b])

        self.lls = standard_label(self, "Load States")

        self.l1 = standard_label(self, load_state[0])
        self.l2 = standard_label(self, load_state[1])

        self.lls.after(1000, self.update_load_state())

    def update_load_state(self):
        self.l1.config(text=load_state[0])
        self.l2.config(text=load_state[1])
        self.lls.after(1000, self.update_load_state)


# main menu
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

        self.pretest_button = standard_button(self, "Pre-Test", lambda: PreTestWindow())


if __name__ == "__main__":
    clock = LoadControl()
    clock.mainloop()


# end
