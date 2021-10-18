"""
Script to determine control method for ECU
"""

# import
import gpiozero
from ECU_load_command import *
from ECU_N2 import *
from ECU_load_calcs import *


# Control Loop used to control the engine ------------------------------------------------------------------------------
class ControlLoop:
    def __init__(self):
        self.control_mode = "None"              # control mode for engine
        self.control_state = "OFF"              # state of controlling
        self.control_units = "None"             # units encoder will control to
        self.n2 = 0                             # krpm
        self.n2_v = 0                           # voltage
        self.target_n2 = 0                      # target n2 speed
        self.kw = 0                             # kw reading
        self.r_level = 0                        # resistive level
        self.ssr_level = 0                      # level on ssr resistive load
        self.pwm_level = 0
        self.currents = [0, 0, 0]
        self.encoder = None
        self.ev = 0                             # encoder value (steps)

    def set_control(self, mode):
        if mode == "PowerControl":
            self.control_mode = mode
            self.control_state = ""
            self.control_units = "Power Level"  # units encoder will control to
            self.encoder = gpiozero.RotaryEncoder(17, 27, max_steps=180)

        elif mode == "SpeedControl":
            self.control_mode = mode
            self.control_state = ""
            self.control_units = "KRPM"  # units encoder will control to
            self.encoder = gpiozero.RotaryEncoder(17, 27, max_steps=40)

        elif mode == "PassiveControl":
            self.control_mode = mode
            self.control_state = ""
            self.control_units = "# PR "  # units encoder will control to
            self.encoder = gpiozero.RotaryEncoder(17, 27, max_steps=12)

        else:
            print("Invalid control state selected")

    def control_loop(self):
        # read n2 speed
        n2.read_speed()
        self.n2 = round(n2.krpm, 2)
        self.n2_v = round(n2.volts, 2)

        # reset steps if less than 0
        if self.encoder.steps < 0:
            self.encoder.steps = 0

        # read in encoder steps value
        self.ev = self.encoder.steps

        # ------------------------------------------- Control Modes ----------------------------------------------------
        # power control mode. Rotary encoder directly controls the load bank
        if self.control_mode == "PowerControl":
            self.r_level = self.ev

        # speed control mode. Load bank will modulate to this speed
        elif self.control_mode == "SpeedControl":

            # also set target speed here
            self.target_n2 = self.ev

            # set minimum speed for active control. Figure out delay or active safeties here...
            if self.n2 > 15:
                self.control_state = "ON"

                # control speed by changing resistive level
                # tap on the brakes if too fast by adding an r level
                if self.n2 > self.target_n2:
                    self.r_level += 1

                elif self.n2 < (self.target_n2-2):
                    self.r_level -= 1

            else:
                self.control_state = "OFF"

        # control mode to follow dynamics of passive power control
        elif self.control_mode == "PassiveControl":
            power_calc = 0.00215 * self.ev * self.n2**2                         # theoretical power at given speed
            self.r_level = (power_calc/1.44) * 10                               # power level in steps

        # ------------------------------------------- Setting Values ---------------------------------------------------
        # values for desired resistive level
        self.ssr_level, self.pwm_level, self.kw, self.currents = load_interp(self.r_level)
        load_gpios.set_load(self.ssr_level)

        small_load.set_load(self.pwm_level)
        # load_pwm.value = self.pwm_level


# control loop object
ecu_control = ControlLoop()


# end of script
