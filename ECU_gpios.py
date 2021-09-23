# ecu gpios
from gpiozero import *


class GPIOState:
    def __init__(self):
        self.occ_button = Button(3, pull_up=False)
        self.re = RotaryEncoder(1, 2)
        self.re.value = 0

    def poll_states(self, state):
        if state == "OFF":
            b = "start button"

        elif state == "LIGHTOFF":
            b = None

        elif state == "IDLE":
            b = None

        elif state == "RUNNING":
            b = "OCC Monitor"


class GPIOStateFake:
    def __init__(self):
        self.occ_status = "Fault"


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

# ecu_gpios = GPIOState()
ecu_gpios = GPIOStateFake()
# end of script
