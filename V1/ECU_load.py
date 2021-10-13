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

    # function to change state of outputs
    def change_load(self, command_array):
        for x in range(len(command_array)):
            if command_array[x] == 1:
                self.l_array[x].on()
            else:
                self.l_array[x].off()


load_gpios = LoadRelaysGPIO()


# resistive load class -------------------------------------------------------------------------------------------------
class ResLoad:
    def __init__(self):
        self.level = 0
        self.kw_level = "0 KW"
        self.load_state = [0, 0, 0, 0, 0, 0, 0]
        self.amp_mat = [
            [0, 0, 0],
            [12, 0, 0],
            [12, 12, 0],
            [12, 12, 12],
            [24, 12, 12],
            [24, 24, 12],
            [24, 24, 24],
            [36, 24, 24],
            [36, 36, 24],
            [36, 36, 36],
            [48, 36, 36],
            [48, 48, 36],
            [48, 48, 48],
            [60, 48, 48],
            [60, 60, 48],
            [60, 60, 60],
            [72, 60, 60],
            [72, 72, 60],
            [72, 72, 72],
            [84, 72, 72],
            [84, 84, 72],
            [84, 84, 84],
            [96, 84, 84],
            [96, 96, 84],
            [96, 96, 96],
            [108, 96, 96],
            [108, 108, 96],
            [108, 108, 108],
            [120, 108, 108],
            [120, 120, 108],
            [120, 120, 120],
            [132, 120, 120],
            [132, 132, 120],
            [132, 132, 132],
            [144, 132, 132]

        ]

    def increment_load(self, inc=0):
        if 0 <= self.level+inc <= max_level:
            self.level = self.level+inc
            self.change_load()

    def reset_load(self):
        self.level = 0
        self.change_load()

    def set_load(self, ll):
        self.level = ll
        self.change_load()

    def change_load(self):
        self.kw_level = str(round(self.level*1.44, 2)) + " KW"
        self.load_state = load_array[self.level]

        # trigger the gpios to fire...
        load_gpios.change_load(self.load_state)


res_load = ResLoad()

# end
