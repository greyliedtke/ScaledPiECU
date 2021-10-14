"""
File to read in analog voltage for N2 in krpm...
"""

# import modules
import smbus
import Adafruit_ADS1x15

# create ads conversion object
# https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/ads1015-slash-ads1115
adc = Adafruit_ADS1x15.ADS1115()

# filter factor. 1 = no filter, 0 = no reading
ff = 0.2
prev_v = 0


# scaling factor
scale_factor = 5197  # determined experimentally for u16 reading? to voltage (not actually u16...)

# into conversion module speed
max_freq = 1                            # khz max frequency
max_volt = 5                            # max voltage corresponding to frequency
khz_krpm = 60                           # krpm/khz factor
freq_volt = max_freq / max_volt         # khz/v


# class to organize N2
class N2:
    def __init__(self):
        self.adc = Adafruit_ADS1x15.ADS1115()
        self.ff = 0.2               # 1 = rely on previous reading entirely, 0 = rely on current reading
        self.v = 0                  # filtered 16 bit voltage reading
        self.volts = 0              # filtered voltage reading
        self.prev_v = 0             # previous voltage
        self.krpm = 0               # speed reading

    def read_voltage(self):
        # read analog channel differential (0 minus 1, at a gain of 1 (+- 4.096 V)
        # gain for 6.114 volts.
        adc_diff = self.adc.read_adc_difference(0, gain=2 / 3)

        # scaling factor determined experimentally...
        # c_bit_16 = 66535
        # c_gain = 6.114
        # v_theo = c_gain * adc_diff/c_bit_16
        # scale_factor = c_bit_16/c_gain = 10882

        self.prev_v = self.v
        self.v = adc_diff*(1-self.ff) + (self.prev_v * self.ff)
        self.volts = self.v / scale_factor

    def read_speed(self):
        # read n2 speed... from a 5 volt signal
        self.read_voltage()

        krpm_volt = khz_krpm * freq_volt  # krpm/volt

        self.krpm = round(krpm_volt * self.volts, 1)  # krpm/volt * volts to get krpm of n2
        self.volts = round(self.volts, 1)


# n2 object
n2 = N2()

# END OF SCRIPT
