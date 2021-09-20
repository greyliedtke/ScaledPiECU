"""
Manage load control of ecu
"""
load_state = [0, 0, 0, 0, 0]
load_level = 0


# pre test window to toggle load pins
def load_press(load_pin):
    print("triggered load:", load_pin)
    load_state[load_pin] = 1 - load_state[load_pin]


# resistive load class
class ResLoad:
    def __init__(self):
        self.level = 0

    def change_load(self, inc=0):
        self.level = self.level+inc


res_load = ResLoad()


# end
