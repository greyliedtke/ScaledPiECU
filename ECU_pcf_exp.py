"""
File to utilize pcf expander to utilize 8 gpio pins per module
"""

# import necessary info
import smbus

pcf_bus = smbus.SMBus(1)

# addresses from setting the jumper
pcf_1 = 0x20
pcf_2 = 0x21

# hex representation of turning on relays up too all 8 on at once
hex_bank = [0x0, 0x1, 0x3, 0x7, 0xf, 0x1f, 0x3f, 0x7f, 0xff]


# function to turn x number of relays
def send_load(relays, pcf_module):
    pcf_bus.write_byte(pcf_module, hex_bank[relays])


# end
