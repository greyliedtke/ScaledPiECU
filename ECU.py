import tkinter as tk
from tkinter import ttk
import time
from tkinter import *
from ECU_load import *
from ECU_tkinter import *
import gpiozero

refresh = 250   # refresh screen every 250 ms


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
        self.pfc_state = "OFF"

    def set_state(self, state):
        self.state = state
        if state == "OFF":
            self.state_time = 0
            self.igniter = "OFF"
            self.pumps = "OFF"
            tw.pump_label.config(bg="grey")
            load_enc.steps = 0
            self.control_button_text = "Begin Test"

        elif state == "COUNTDOWN":
            self.state_time = 0
            self.igniter = "OFF"
            self.pumps = "OFF"
            self.control_button_text = "NA"

        elif state == "LIGHTOFF":
            self.igniter = "ON"
            tw.igniter_label.config(bg="green")
            tw.pump_label.config(bg="green")
            self.pumps = "ON"
            self.control_button_text = "NA"

        elif state == "IDLE":
            self.igniter = "OFF"
            tw.igniter_label.config(bg="light grey")
            self.pumps = "ON"
            self.control_button_text = "NA"

        elif state == "RUNNING":
            self.igniter = "OFF"
            self.pumps = "ON"
            self.control_button_text = "OFF"

        elif state == "FAULT":
            self.igniter = "OFF"
            self.pumps = "OFF"
            self.control_button_text = "RESET"
            load_enc.steps = 0

        else:
            print("fault!")
        return

    def pfc_state_change(self, pfc_switch):
        if pfc_switch == 0 and self.state == "RUNNING":
            self.set_state("OFF")
            self.pfc_state = "FAULT"
        elif pfc_switch == 0:
            self.pfc_state = "OFF"
        elif pfc_switch == 1:
            self.pfc_state = "ON"


# ecu state controller
ecu = ECUState()


#


# setting gpio buttons ---------------------------------------------
def mode_pressed():
    if ecu.state == "OFF":
        ecu.set_state("COUNTDOWN")

    elif ecu.state == "RUNNING":
        ecu.set_state("OFF")

    elif ecu.state == "FAULT":
        ecu.set_state("OFF")

    else:
        print("ignored")
    return


mode_button = gpiozero.Button(16, pull_up=True)
mode_button.when_pressed = mode_pressed


# pfc status
class PFCStatus:
    def __init__(self):
        self.pfc_button = gpiozero.Button(7, pull_up=True, hold_time=1)
        self.text = "OFF"

    def state_text(self):
        if self.pfc_button.value == 0:
            text = "OFF"
        else:
            text = "ON"
        return text


pfc = PFCStatus()


# rotary encoder for load bank
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
        # self.control_button = button_grid(self, control_column, 0, ecu.control_button_text, command=lambda: control_button())
        control_column = 0
        self.system_label = label_grid(self, control_column, 0, "System Status")
        self.control_label = label_grid(self, control_column, 1, ecu.state)
        self.control_time = label_grid(self, control_column, 2, ecu.state_time)

        # system status's
        status_column = 1
        self.eq_label = label_grid(self, status_column, 0, "Device Status")
        self.pump_label = label_grid(self, status_column, 1, "Fuel Pumps: " + ecu.pumps)
        self.igniter_label = label_grid(self, status_column, 2, "Igniter: " + ecu.igniter)
        self.pfc_status = label_grid(self, status_column, 3, "PFC Status: " + ecu.pfc_state)

        # load bank
        load_column = 2
        # self.load_up_button = button_grid(self, load_column, 0, "Load Up",
        #                                   command=lambda: res_load.increment_load(inc=1))
        # self.load_down_button = button_grid(self, load_column, 1, "Load Down",
        #                                     command=lambda: res_load.increment_load(inc=-1))
        # self.lll = label_grid(self, load_column, 1, res_load.level)
        self.ll = label_grid(self, load_column, 0, "Load Bank")
        self.llenc = label_grid(self, load_column, 1, load_enc.steps)
        self.llkw = label_grid(self, load_column, 2, res_load.kw_level)

        amp_column = 2
        self.amp_label = label_grid(self, amp_column, 0, "Expected Currents")
        self.a1 = label_grid(self, load_column, 1, str(res_load.amp_mat[res_load.level][0]))
        self.a2 = label_grid(self, load_column, 2, str(res_load.amp_mat[res_load.level][1]))
        self.a3 = label_grid(self, load_column, 3, str(res_load.amp_mat[res_load.level][2]))

        # display all loads
        # load_column_2 = 3
        # self.lls = label_grid(self, load_column_2, 0, "Load States")
        # self.load_labels = []
        # for ll in range(7):
        #     label = label_grid(self, load_column_2, 1 + ll, ll)
        #     self.load_labels.append(label)

        # speed control
        # self.pwm_label = label_grid(self, 2, 0, "Speed %: " + str(ecu.pwm))
        # self.n2_speed = label_grid(self, 2, 1, "N2 krpm: " + str(ecu.n2_speed))

        # screen refresh rate
        self.control_label.after(refresh, self.update_state())

    def update_state(self):
        # function to run every xx seconds

        # check state and time to automatically trigger a state change
        if ecu.state == "COUNTDOWN" and ecu.state_time == 3:
            ecu.set_state("LIGHTOFF")

        elif ecu.state == "LIGHTOFF" and ecu.state_time == 6:
            ecu.set_state("IDLE")

        elif ecu.state == "IDLE" and ecu.state_time == 10:
            ecu.set_state("RUNNING")

        elif ecu.state == "RUNNING" and pfc.pfc_button.value == 0:
            ecu.set_state("FAULT")

        # update control state labels
        # self.control_button.config(text=ecu.control_button_text)
        self.control_label.config(text=ecu.state)
        self.control_time.config(text=round(ecu.state_time, 0))

        # update output commands
        self.igniter_label.config(text="Igniter: " + ecu.igniter)
        self.pump_label.config(text="Fuel Pumps " + ecu.pumps)
        self.pfc_status.config(text="PFC " + pfc.state_text())

        # update text for resistive load stage, kw, and labels
        if load_enc.steps < 0:
            load_enc.steps = 0

        if res_load.level != load_enc.steps:
            res_load.set_load(load_enc.steps)

        # self.lll.config(text=res_load.level)
        self.llkw.config(text=res_load.kw_level)
        self.llenc.config(text=load_enc.steps)
        self.a1.config(text=str(res_load.amp_mat[res_load.level][0]))
        self.a2.config(text=str(res_load.amp_mat[res_load.level][1]))
        self.a3.config(text=str(res_load.amp_mat[res_load.level][2]))
        # for ll in range(len(self.load_labels)):
        #     self.load_labels[ll].config(text=res_load.load_state[ll])

        # increment state time call update
        ecu.state_time += .25
        self.control_label.after(refresh, self.update_state)


if __name__ == "__main__":
    # clock = LoadControl()
    tw = TestWindow()
    tw.mainloop()


# end
