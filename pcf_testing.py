"""
controlling pcf gpio expander...
"""

# define IO's. Hex representation of individual commands
io_0 = 0x01     # 1
io_1 = 0x02     # 2
io_2 = 0x04     # 4
io_3 = 0x08     # 8
io_4 = 0x10     # 16
io_5 = 0x20     # 32
io_6 = 0x40     # 64
io_7 = 0x80     # 128


# bank of array commands that will be converted to decimal and hex...
binary_bank = [
    "00000000",             # all off
    "00000001",             # 1 r
    "00000011",             # 2 r
    "00000111",             # 3 r
    "00001111",             # 4 r
    "00011111",             # 5 r
    "00111111",             # 6 r
    "01111111",             # 7 r
    "11111111"              # 8 r
               ]

# hex representation of turning on relays up too all 8 on at once
hex_bank = [0x0, 0x1, 0x3, 0x7, 0xf, 0x1f, 0x3f, 0x7f, 0xff]


# function to write array
def load_array(level):
    # send commands to gpio 0-7 from given level... number of relays on
    bin_rep = binary_bank[level]            # binary representation
    dec_rep = int(bin_rep, 2)               # decimal representation
    hex_rep = hex(dec_rep)                  # hex representation
    # print(bin_rep, dec_rep, hex_rep)
    print(hex_rep)


# loop through testing values
for load in range(9):
    load_array(load)


# end

