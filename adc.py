# reading in the analog speed signal
import smbus
import Adafruit_ADS1x15

# create ads conversion object
adc = Adafruit_ADS1x15.ADS1115()


def read_ai01_v():
    # read analog channel differential (0 minus 1, at a gain of 1 (+- 4.096 V)
    adc_diff = adc.read_adc_difference(0, gain=1)

    # scaling factor determined experimentally...
    # c_bit_16 = 66535
    # c_gain = 4.096
    # v_theo = c_gain * adc_diff/c_bit_16
    # scale_factor = c_bit_16/c_gain = 16244

    scale_factor = 7779             # determined experimentally
    adc_v = adc_diff/scale_factor
    return adc_v


def read_n2_speed():
    # read n2 speed... from a 3.3 volt signal
    n2_a_in = read_ai01_v()     # max 3.3 volts
    # Banner outputs a frequency

    # into conversion module speed
    max_freq = 10           # khz max frequency
    max_volt = 10           # max voltage corresponding to frequency
    khz_krpm = 60
    freq_volt = max_freq/max_volt   # khz/v
    krpm_volt = khz_krpm*freq_volt  # krpm/volt

    # into level shifter
    f3 = 5/3.3
    n2_krpm = krpm_volt*n2_a_in*f3   # scale for
    return n2_krpm



# end of script
