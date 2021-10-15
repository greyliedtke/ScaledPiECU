"""
Manage load control of ecu
"""
from gpiozero import *
import smbus

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

# ----------------------------------------------------------------------------------------------------------------------
# class PWMLoad:
#     def __init__(self):
#         # intialize pwm load control
#         self.pwm_pin = PWMOutputDevice(10, frequency=200)

load_pwm = PWMOutputDevice(12, frequency=200)


# Small passive load on i2c bus ----------------------------------------------------------------------------------------
class SmallLoad:
    def __init__(self):
        self.rm1 = 0x20
        self.rm2 = 0x21
        self.bus = smbus.SMBus(1)

        # hex bank for controlling relays of 0 up to 8... We should only use max 5!!!
        self.hex_bank = [0x0, 0x1, 0x3, 0x7, 0xf, 0x1f, 0x3f, 0x7f, 0xff]

        # initialize load at 0
        self.set_load(0)

    def set_load(self, pwm_load):
        # convert pwm signal to integer
        small_load_int = int(pwm_load*10)

        # if load is in between here. It is valid to turn on relays
        if 0 < small_load_int < 10:
            rm1l = small_load_int

            # deciding which relay modules have how many on
            if small_load_int > 5:
                rm1l = 5
                rm2l = small_load_int - 5
            else:
                rm2l = 0
        else:
            rm1l = 0
            rm2l = 0

        # convert it to hex
        rm1b = self.hex_bank[rm1l]
        rm2b = self.hex_bank[rm2l]

        # send on the bus
        self.bus.write_byte(self.rm1, rm1b)
        self.bus.write_byte(self.rm2, rm2b)


# initialzie small load object
small_load = SmallLoad()


# end
