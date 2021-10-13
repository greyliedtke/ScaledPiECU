"""
File to read in analog voltage for N2 in krpm...
"""

# import modules
import smbus
import Adafruit_ADS1x15

# create ads conversion object
# https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/ads1015-slash-ads1115
adc = Adafruit_ADS1x15.ADS1115()


# THIS WILL NEED TO CHANGE FOR 6 VOLT SIGNAL RANGE...
# function to read analog voltage on channel 0 minus channel 1
def read_ai01_v():
    # read analog channel differential (0 minus 1, at a gain of 1 (+- 4.096 V)
    # gain for 6.114 volts.
    adc_diff = adc.read_adc_difference(0, gain=2/3)

    # scaling factor determined experimentally...
    # c_bit_16 = 66535
    # c_gain = 6.114
    # v_theo = c_gain * adc_diff/c_bit_16
    # scale_factor = c_bit_16/c_gain = 10882

    scale_factor = 10882             # determined experimentally
    adc_v = adc_diff/scale_factor
    return adc_v


def read_n2_speed():
    # read n2 speed... from a 5 volt signal
    n2_volt = read_ai01_v()

    # into conversion module speed
    max_freq = 10                       # khz max frequency
    max_volt = 10                       # max voltage corresponding to frequency
    khz_krpm = 60                       # krpm/khz factor
    freq_volt = max_freq/max_volt       # khz/v
    krpm_volt = khz_krpm*freq_volt      # krpm/volt

    n2_krpm = round(krpm_volt*n2_volt, 1)         # krpm/volt * volts to get krpm of n2
    n2_volt = round(n2_volt, 1)

    # print(n2_a_in, n2_krpm)             # print voltage and supposed n2 speed
    return n2_krpm, n2_volt

# END OF SCRIPT