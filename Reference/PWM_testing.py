import tkinter as tk
from ECU_tkinter import *
from Reference.pwm_dimmer import *


# system variables
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
        if pfc_switch == 1 and self.state == "RUNNING":
            self.set_state("OFF")
            self.pfc_state = "FAULT"
        elif pfc_switch == 1:
            self.pfc_state = "OFF"
        elif pfc_switch == 0:
            self.pfc_state = "ON"


# ecu state controller
ecu = ECUState()


# testing window gui -----------------------------------------------------------
class TestWindow(tk.Tk):
    def __init__(self):

        # initialize window
        super().__init__()
        self.title('Test Window')
        # self.resizable(0, 0)
        self.geometry('1000x500')
        self['bg'] = 'black'

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
        self.ll = label_grid(self, load_column, 0, "Load Bank")
        self.llenc = label_grid(self, load_column, 1, load_enc.steps)
        self.llkw = label_grid(self, load_column, 2, res_load.kw_level)
        self.ll_pwm = label_grid(self, load_column, 3, res_load.pwm_level)

        # amp column
        # amp_column = 3
        # self.amp_label = label_grid(self, amp_column, 0, "Expected Currents")
        # self.a1 = label_grid(self, amp_column, 1, str(res_load.amp_mat[res_load.level][0]))
        # self.a2 = label_grid(self, amp_column, 2, str(res_load.amp_mat[res_load.level][1]))
        # self.a3 = label_grid(self, amp_column, 3, str(res_load.amp_mat[res_load.level][2]))

        # screen refresh rate
        self.control_label.after(refresh, self.update_state())

    def update_state(self):

        # function to run every xx seconds
        res_load.refresh_load()

        # check state and time to automatically trigger a state change
        if ecu.state == "COUNTDOWN" and ecu.state_time == 3:
            ecu.set_state("LIGHTOFF")

        elif ecu.state == "LIGHTOFF" and ecu.state_time == 12:
            ecu.set_state("IDLE")

        elif ecu.state == "IDLE" and ecu.state_time == 15:
            ecu.set_state("RUNNING")

        # elif ecu.state == "RUNNING" and pfc.pfc_button.value == 1:
        #     time.sleep(1)
        #     if pfc.pfc_button.value == 1:
        #         ecu.set_state("FAULT")

        # update control state labels
        self.control_label.config(text=ecu.state)
        self.control_time.config(text=round(ecu.state_time, 0))

        # update output commands
        self.igniter_label.config(text="Igniter: " + ecu.igniter)
        self.pump_label.config(text="Fuel Pumps " + ecu.pumps)
        # self.pfc_status.config(text="PFC " + pfc.state_text())

        # update text for resistive load stage, kw, and labels
        if load_enc.steps < 0:
            load_enc.steps = 0

        # self.lll.config(text=res_load.level)
        self.llkw.config(text=res_load.kw_level)
        self.llenc.config(text=load_enc.steps)
        self.ll_pwm.config(text=res_load.pwm_level)
        # self.a1.config(text=str(res_load.amp_mat[res_load.level][0]))
        # self.a2.config(text=str(res_load.amp_mat[res_load.level][1]))
        # self.a3.config(text=str(res_load.amp_mat[res_load.level][2]))

        # increment state time call update
        ecu.state_time += .25
        self.control_label.after(refresh, self.update_state)


if __name__ == "__main__":
    # clock = LoadControl()
    tw = TestWindow()
    tw.mainloop()
