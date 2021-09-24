# ecu gpios
from gpiozero import *


# Load Relays -----------------------------------------------
class LoadRelaysGPIO:
    def __init__(self):
        # initialize all relay outputs
        l1 = DigitalOutputDevice(9)
        l2 = DigitalOutputDevice(11)
        l3 = DigitalOutputDevice(5)
        l4 = DigitalOutputDevice(6)
        l5 = DigitalOutputDevice(13)
        l6 = DigitalOutputDevice(19)
        l7 = DigitalOutputDevice(26)
        self.l_array = [l1, l2, l3, l4, l5, l6, l7]

    # function to change state of outputs
    def change_load(self, command_array):
        for x in range(len(command_array)):
            if command_array[x] == 1:
                self.l_array[x].on()
            else:
                self.l_array[x].off()


load_gpios = LoadRelaysGPIO()

# end of script