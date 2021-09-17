"""
Manage load control of ecu
"""
load_state = [0, 0, 0, 0, 0]


# pre test window to toggle load pins
def load_press(load_pin):
    print("triggered load:", load_pin)
    load_state[load_pin] = 1 - load_state[load_pin]

# end
