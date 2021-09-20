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




# ecu_gpios = GPIOState()
ecu_gpios = GPIOStateFake()
# end of script
