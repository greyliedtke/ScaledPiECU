"""
Manage load control of ecu
"""
from gpiozero import *

# Load bank GPIOS ------------------------------------------------------------------------------------------------------
load_array = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 1],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 0, 0, 1, 1],
    [1, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 1, 0],
    [1, 0, 0, 0, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 1, 0],
    [1, 0, 0, 1, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 1, 0],
    [1, 1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 1, 0, 0],
    [1, 1, 0, 0, 1, 1, 0],
    [1, 1, 0, 0, 1, 1, 1],
    [1, 1, 0, 1, 0, 0, 0],
    [1, 1, 0, 1, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 0],
    [1, 1, 1, 0, 0, 1, 1],
    [1, 1, 1, 0, 1, 0, 0],
    [1, 1, 1, 0, 1, 1, 0],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 0, 1, 1]
]
max_level = 18


# Class to cluster gpios
class LoadRelaysGPIO:
    def __init__(self):
        # initialize all relay outputs
        l1 = DigitalOutputDevice(26)
        l2 = DigitalOutputDevice(19)
        l3 = DigitalOutputDevice(13)
        l4 = DigitalOutputDevice(6)
        l5 = DigitalOutputDevice(5)
        l6 = DigitalOutputDevice(11)
        l7 = DigitalOutputDevice(9)
        self.l_array = [l1, l2, l3, l4, l5, l6, l7]

        self.level = 0
        self.load_state = [0, 0, 0, 0, 0, 0, 0]

    # function to change load outputs
    def set_load(self, load_level):
        self.load_state = load_array[load_level]
        for x in range(len(self.load_state)):
            if self.load_state[x] == 1:
                self.l_array[x].on()
            else:
                self.l_array[x].off()


load_gpios = LoadRelaysGPIO()


# class PWMLoad:
#     def __init__(self):
#         # intialize pwm load control
#         self.pwm_pin = PWMOutputDevice(10, frequency=200)

load_pwm = PWMOutputDevice(10, frequency=200)


# end
