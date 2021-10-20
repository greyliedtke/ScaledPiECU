

# I2c interface to 8 gpio output
# ac ssr require 7 ma, 5v input
# 80 ma Max... 10 ma per pin

# 7 ma to turn on...
relay_vals = [3, 3, 1, 1, 1, .5, 0, 0]
load_command = [0, 0, 0, 0, 0, 0, 0, 0]


def load_to_command(load):
    l_a = [3, 3, 1, 1, 1, .5, 1000, 1000]               # level correspoding to each gpio
    l_c = [0, 0, 0, 0, 0, 0, 0, 0]                      # initialize command
    l_c_oo = [0, 0, 0, 0, 0, 0, 0, 0]                   # command out

    ten_o = load/10                                     # divide to get in terms of .5 increments
    for r in range(0, 8):
        if sum(l_c) + l_a[r] <= ten_o:                  # if less or equal to, set as is
            l_c[r] = l_a[r]
            l_c_oo[r] = 1
            # print("match")
        else:                                           # else set 0
            l_c[r] = 0

    print(l_c_oo)


for ll in range(0, 100, 5):
    load_to_command(ll)

magic_array = [
    "00000000",
    "00000100",
    "00100000",
    "00100100",
    "00110000",
    "00110100",
    "10000000",
    "10000100",
    "10100000",
    "10100100",
    "10110000",
    "10110100",
    "11000000",
    "11000100",
    "11100000",
    "11100100",
    "11110000",
    "11110100",
    "11111000",
    "11111100",
]

magic_hex = [0x0, 0x4, 0x20, 0x24, 0x30, 0x34, 0x80, 0x84, 0xa0, 0xa4, 0xb0, 0xb4, 0xc0, 0xc4, 0xe0, 0xe4, 0xf0, 0xf4, 0xf8, 0xfc]

# end
