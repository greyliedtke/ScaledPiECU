"""
Main ECU program updated with control modes and n2 reading
"""

# import modules for tkinter gui
import tkinter as tk
import time

from ECU_gpios import *
from ECU_tkinter import *
from ECU_control import *

# refresh screen every 250 ms
refresh_ms = 250
refresh_s = refresh_ms/1000

# set control mode
ecu_control.set_control("PowerControl")
# ecu_control.set_control("SpeedControl")
# ecu_control.set_control("PassiveControl")


# State machine to operate system at each state... ---------------------------------------------------------------------
class ECUState:
    def __init__(self):
        # initialize system with everything off
        self.state = "OFF"
        self.control_mode = "Power Control"
        self.igniter = "OFF"
        self.pumps = "OFF"
        self.control_button_text = "Begin Test"
        # self.fuel_pwm = 37
        # self.n2_speed = 0
        self.state_time = 0
        self.pfc_state = "OFF"

    def set_state(self, state):
        # function to change the state of machine

        # set state as the state passed into function
        self.state = state

        # turn engine off
        if state == "OFF":
            self.igniter = "OFF"                            # turn igniter off
            ign.off()

            self.pumps = "OFF"                              # turn fuel pumps off and change their color
            fps.off()
            tw.pump_label.config(bg="grey")

            self.state_time = 0                             # reset time to zero
            ecu_control.encoder.value = 0                   # reset encoder steps to zero
            self.control_button_text = "Begin Test"         # reset control button text

        # countdown mode. Initialize state time and change labels
        elif state == "COUNTDOWN":
            self.state_time = 0
            self.igniter = "OFF"
            self.pumps = "OFF"
            self.control_button_text = "NA"

        # lightoff mode. Turn on igniter and pumps
        elif state == "LIGHTOFF":
            self.igniter = "ON"
            ign.on()
            tw.igniter_label.config(bg="green")

            self.pumps = "ON"
            fps.on()
            tw.pump_label.config(bg="green")

        # Idle mode. Turn off igniter. Ignore PFC fault if occurs...
        elif state == "IDLE":
            self.igniter = "OFF"
            ign.off()
            tw.igniter_label.config(bg="light grey")

        # Running state. No difference from idle except monitoring for fault
        elif state == "RUNNING":
            # make something green?
            self.pumps = "ON"

        # if PFC Fault occurs. Turn off system, make control button a reset button
        elif state == "FAULT":
            self.igniter = "OFF"
            ign.off()
            self.pumps = "OFF"
            fps.off()

            self.control_button_text = "RESET"
            ecu_control.encoder.value = 0  # reset encoder steps to zero

        # Tried to change state to an invalid state...
        else:
            print("fault! This is not a default state")

        return


# Initizialize state controller from above
ecu = ECUState()


# testing window gui ---------------------------------------------------------------------------------------------------
class TestWindow(tk.Tk):
    def __init__(self):

        # initialize window
        super().__init__()
        self.title('Test Window')
        self.geometry('1000x500')
        self['bg'] = 'black'

        # system status's
        # add mode control button?
        system_column = 0
        self.system_label = label_grid(self, system_column, 0, "System Status")
        self.control_time = label_grid(self, system_column, 1, ecu.state_time)
        # self.control_label = label_grid(self, system_column, 1, ecu.state)

        # system status's
        status_column = 1
        self.eq_label = label_grid(self, status_column, 0, "Device Status")
        self.pump_label = label_grid(self, status_column, 1, "Fuel Pumps: " + ecu.pumps)
        self.igniter_label = label_grid(self, status_column, 2, "Igniter: " + ecu.igniter)
        self.pfc_status = label_grid(self, status_column, 3, "PFC Status: " + ecu.pfc_state)

        # speed reading
        n2_column = 2
        self.n2_label = label_grid(self, n2_column, 0, "N2 Speed (KRPM)")
        self.n2_speed = label_grid(self, n2_column, 1, str(ecu_control.n2))
        self.n2_volts = label_grid(self, n2_column, 2, str(ecu_control.n2_v))

        # control column
        control_column = 3
        self.control_mode = label_grid(self, control_column, 0, ecu_control.control_mode)
        self.control_status = label_grid(self, control_column, 1, ecu_control.control_state)
        self.control_units = label_grid(self, control_column, 2, ecu_control.control_units)
        self.control_target = label_grid(self, control_column, 3, ecu_control.encoder.steps)

        # load bank
        load_column = 4
        self.ll = label_grid(self, load_column, 0, "Load Bank")
        self.ssr_level = label_grid(self, load_column, 1, ecu_control.ssr_level)
        self.ll_pwm = label_grid(self, load_column, 2, ecu_control.pwm_level)
        self.llkw = label_grid(self, load_column, 3, ecu_control.kw)
        self.amp_label = label_grid(self, load_column, 4, "Expected Currents")
        self.a1 = label_grid(self, load_column, 5, str(ecu_control.currents[0]))
        self.a2 = label_grid(self, load_column, 6, str(ecu_control.currents[1]))
        self.a3 = label_grid(self, load_column, 7, str(ecu_control.currents[2]))

        # screen refresh rate
        self.system_label.after(refresh_ms, self.update_state())

    # function to run every xx seconds
    def update_state(self):

        # control loop
        ecu_control.control_loop()

        # check pfc status
        if pfc_button.value == 1:
            pfc_status = "OFF"
        else:
            pfc_status = "ON"

        # Begin lightoff if mode button is pressed and time is greater than 10 seconds
        if ecu.state == "OFF" and mode_button.value == 1 and ecu.state_time > 10:
            ecu.set_state("COUNTDOWN")

        # Reset fault if mode button is pressed and time is greater than 10 seconds
        if ecu.state == "FAULT" and mode_button.value == 1 and ecu.state_time > 10:
            ecu.set_state("OFF")

        # check state and time to automatically trigger a state change
        if ecu.state == "COUNTDOWN" and ecu.state_time == 3:
            ecu.set_state("LIGHTOFF")

        elif ecu.state == "LIGHTOFF" and ecu.state_time == 12:
            ecu.set_state("IDLE")

        elif ecu.state == "IDLE" and ecu.state_time == 15:
            ecu.set_state("RUNNING")

        # if engine is running and reads a pfc fault, ignore for 1 second
        elif ecu.state == "RUNNING" and pfc_status == "OFF":
            time.sleep(1)
            # if still there for 1 second... turn system off
            if pfc_button.value == 1:
                ecu.set_state("FAULT")

        # update control state labels
        self.system_label.config(text=ecu.state)
        self.control_time.config(text=round(ecu.state_time, 0))

        # update output labels
        self.igniter_label.config(text="Igniter: " + ecu.igniter)
        self.pump_label.config(text="Fuel Pumps " + ecu.pumps)
        self.pfc_status.config(text="PFC " + pfc_status)

        # update speed
        self.n2_speed.config(text=str(ecu_control.n2))
        self.n2_volts.config(text="V: " + str(ecu_control.n2_v))

        # update control status values
        self.control_status.config(text=ecu_control.control_state)
        self.control_target.config(text=ecu_control.ev)

        # update text for resistive load stage, kw, and current labels
        self.llkw.config(text="kw: " + str(ecu_control.kw))
        self.ssr_level.config(text="resitors" + str(ecu_control.r_level))
        self.ll_pwm.config(text="pwm: " + str(ecu_control.pwm_level))
        self.a1.config(text=str(ecu_control.currents[0]))
        self.a2.config(text=str(ecu_control.currents[1]))
        self.a3.config(text=str(ecu_control.currents[2]))

        # increment state time and rerun function
        ecu.state_time += refresh_s
        self.system_label.after(refresh_ms, self.update_state)


# Initialize test window -----------------------------------------------------------------------------------------------
if __name__ == "__main__":
    tw = TestWindow()
    tw.mainloop()


# end
