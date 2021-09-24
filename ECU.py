import tkinter as tk
from tkinter import ttk
import time
from tkinter import *
from ECU_load import *
from ECU_tkinter import *
import gpiozero

update_time = 100


# State machine to handle commands at each state...
class ECUState:
    def __init__(self):
        self.state = "OFF"
        self.igniter = "OFF"
        self.pumps = "OFF"
        self.control_button_text = "Begin Test"
        self.pwm = 37
        self.n2_speed = 0
        self.state_time = 0

    def set_state(self, state):
        self.state_time = 0
        self.state = state
        if state == "OFF":
            self.igniter = "OFF"
            self.pumps = "OFF"
            res_load.reset_load()
            self.control_button_text = "Begin Test"

        elif state == "COUNTDOWN":
            self.igniter = "OFF"
            self.pumps = "OFF"
            self.control_button_text = "NA"

        elif state == "LIGHTOFF":
            self.igniter = "ON"
            self.pumps = "ON"
            self.control_button_text = "NA"

        elif state == "IDLE":
            self.igniter = "OFF"
            self.pumps = "ON"
            self.control_button_text = "NA"

        elif state == "RUNNING":
            self.igniter = "OFF"
            self.pumps = "ON"
            self.control_button_text = "OFF"

        else:
            print("fault!")
        return


# ecu state controller
ecu = ECUState()


# function to handle presses of control button
def control_button():
    if ecu.state == "OFF":
        ecu.set_state("COUNTDOWN")

    elif ecu.state == "RUNNING":
        ecu.set_state("OFF")

    else:
        print("ignored")
    return


# setting gpio buttons ---------------------------------------------
def mode_pressed():
    if ecu.state == "OFF":
        ecu.set_state("COUNTDOWN")

    elif ecu.state == "RUNNING":
        ecu.set_state("OFF")

    else:
        print("ignored")
    return


mode_button = gpiozero.Button(16, pull_up=True)
mode_button.when_pressed = mode_pressed

load_enc = gpiozero.RotaryEncoder(21, 20, max_steps=max_level)


# testing window gui -----------------------------------------------------------
class TestWindow(tk.Tk):
    def __init__(self):

        # initialize window
        super().__init__()
        self.title('Test Window')
        # self.resizable(0, 0)
        self.geometry('1000x500')
        self['bg'] = 'black'

        # control buttons
        control_column = 0
        self.control_button = button_grid(self, control_column, 0, ecu.control_button_text, command=lambda: control_button())
        self.control_label = label_grid(self, control_column, 1, ecu.state)
        self.control_time = label_grid(self, control_column, 2, ecu.state_time)

        # system status's
        status_column = 1
        self.pump_label = label_grid(self, status_column, 0, "Fuel Pump: " + ecu.pumps)
        self.igniter_label = label_grid(self, status_column, 1, "Igniter: " + ecu.igniter)
        # self.occ_status = label_grid(self, 1, 2, "PFC Status: " + ecu_gpios.occ_status)


        # load bank
        # add conditional statement for button presses only during test
        load_column = 2
        self.load_up_button = button_grid(self, load_column, 0, "Load Up", command=lambda: res_load.increment_load(inc=1))
        self.load_down_button = button_grid(self, load_column, 1, "Load Down", command=lambda: res_load.increment_load(inc=-1))
        self.lll = label_grid(self, load_column, 2, res_load.level)
        self.llkw = label_grid(self, load_column, 3, res_load.kw_level)
        self.llenc = label_grid(self, load_column, 4, load_enc.steps)

        # display all loads
        load_column_2 = 3
        self.lls = label_grid(self, load_column_2, 0, "Load States")
        self.load_labels = []
        for ll in range(7):
            label = label_grid(self, load_column_2, 1 + ll, ll)
            self.load_labels.append(label)

        # speed control
        # self.pwm_label = label_grid(self, 2, 0, "Speed %: " + str(ecu.pwm))
        # self.n2_speed = label_grid(self, 2, 1, "N2 krpm: " + str(ecu.n2_speed))

        # screen refresh rate
        self.lls.after(1000, self.update_state())

    def update_state(self):
        # function to run every xx seconds

        # check state and time to automatically trigger a state change
        if ecu.state == "COUNTDOWN" and ecu.state_time == 3:
            ecu.set_state("LIGHTOFF")

        elif ecu.state == "LIGHTOFF" and ecu.state_time == 5:
            ecu.set_state("IDLE")

        elif ecu.state == "IDLE" and ecu.state_time == 5:
            ecu.set_state("RUNNING")

        # update control state labels
        self.control_button.config(text=ecu.control_button_text)
        self.control_label.config(text=ecu.state)
        self.control_time.config(text=ecu.state_time)

        # update output commands
        self.igniter_label.config(text="Igniter: " + ecu.igniter)
        self.pump_label.config(text="Fuel Pumps " + ecu.pumps)

        # update text for resistive load stage, kw, and labels
        if load_enc.steps < 0:
            load_enc.steps = 0

        if res_load.level != load_enc.steps:
            res_load.set_load(load_enc.steps)

        self.lll.config(text=res_load.level)
        self.llkw.config(text=res_load.kw_level)
        self.llenc.config(text=load_enc.steps)
        for ll in range(len(self.load_labels)):
            self.load_labels[ll].config(text=res_load.load_state[ll])

        # increment state time call update
        ecu.state_time += 1
        self.lls.after(1000, self.update_state)


if __name__ == "__main__":
    # clock = LoadControl()
    tw = TestWindow()
    tw.mainloop()


# end
