import gpiozero

min_encoder = 0
max_encoder = 100
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


# rotary encoder for load bank
load_enc = gpiozero.RotaryEncoder(17, 27, max_steps=max_encoder)

# pwm pin
pwm_pin = gpiozero.PWMOutputDevice(10, frequency=5000)


# resistive load class
class ResLoad:
    def __init__(self):
        self.level = 0
        self.pwm_level = 0
        self.kw_level = "0 KW"
        self.load_state = [0, 0, 0, 0, 0, 0, 0]

    def refresh_load(self):
        # reset encoder if negative
        if load_enc.value < 0:
            load_enc.value = 0

        if load_enc.value != self.level:
            self.level = load_enc.value
            self.pwm_level = load_enc.value
            pwm_pin.value = self.pwm_level/max_encoder

    def reset_load(self):
        self.level = 0
        self.change_load()

    # function to update load on gpio level
    def change_load(self):
        self.kw_level = str(round(self.level*1.44, 2)) + " KW"
        self.load_state = load_array[self.level]

        # trigger the gpios to fire...
        # load_gpios.change_load(self.load_state)


res_load = ResLoad()

# end
