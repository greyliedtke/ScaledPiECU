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

bb = [
    "00000000",             # all off
    "10000000",             # 1 r
    "11000000",             # 2 r
    "11100000",             # 3 r
    "11110000",             # 4 r
    "11111000",             # 5 r
    "11111100",             # 6 r
    "11111110",             # 7 r
    "11111111"              # 8 r
               ]

bank_half_count = [
    "00000000",             # all off
    "00000001",             # .5
    "10000000",             # 1
    "10000001",             # 1.5
    "11000000",             # 2
    "11000001",             # 2.5
    "11100000",             # 3
    "11100001",             # 3.5
    "11110000",             # 4
    "11110001",             # 4.5
                    ]

# hex representation of turning on relays up too all 8 on at once backwards...
hex_bank = [0x0, 0x1, 0x3, 0x7, 0xf, 0x1f, 0x3f, 0x7f, 0xff]


# hex single steps
hex_bb = [0x0, 0x80, 0xc0, 0xe0, 0xf0, 0xf8]


# hex half bank of 0 to 4.5 in .5 increments
half_hex_bank = [0x0, 0x1, 0x80, 0x81, 0xc0, 0xc1, 0xe0, 0xe1, 0xf0, 0xf1]

bank_020 = [
    [0x0, 0x0],         # 0
    [0x0, 0x1],         # 0.5
    [0x0, 0x80],        # 1
    [0x0, 0x81],        # 1.5
    [0x0, 0xc0],        # 2
    [0x0, 0xc1],        # 2.5
    [0x0, 0xe0],        # 3
    [0x0, 0xe1],        # 3.5
    [0x0, 0xf0],        # 4
    [0x0, 0xf1],        # 4.5
    [0x80, 0xf0],        # 5
    [0x80, 0xf1],        # 5.5
    [0xc0, 0xf0],        # 6
    [0xc0, 0xf1],        # 6.5
    [0xe0, 0xf0],        # 7
    [0xe0, 0xf1],        # 7.5
    [0xf0, 0xf0],        # 8
    [0xf0, 0xf1],        # 8.5
    [0xf1, 0xf0],        # 9
    [0xf1, 0xf1],        # 9.5
]


# function to write array
def load_array(level):
    # send commands to gpio 0-7 from given level... number of relays on
    bin_rep = bb[level]            # binary representation
    dec_rep = int(bin_rep, 2)               # decimal representation
    hex_rep = hex(dec_rep)                  # hex representation
    # print(bin_rep, dec_rep, hex_rep)
    print(hex_rep)


# loop through testing values
for load in range(6):
    load_array(load)


# end

