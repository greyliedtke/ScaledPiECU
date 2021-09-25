import numpy

def load_to_amps(load):
    # check if divisible by 3
    if load % 3 == 0:
        div3 = load / 3
        m_array = [div3, div3, div3]

    # else check if 2 more is divisible by 3
    elif ((load+2) % 3) == 0:
        div1 = (load+2) / 3
        m_array = [div1, div1-1, div1-1]

    # else if 2 more is divisible by 3
    else:
        div2 = (load + 1) / 3
        m_array = [div2, div2, div2 - 1]

    m_array = numpy.array(m_array)
    amps = m_array * 12
    return amps

amp_loads = []
for x in range(35):
    amp_loads.append(load_to_amps(x))

print(amp_loads)
for a in amp_loads:
    print(a.tolist())

list_35 = [
    [0, 0, 0],
    [12, 0, 0],
    [12, 12, 0],
    [12, 12, 12],
    [24, 12, 12],
    [24, 24, 12],
    [24, 24, 24],
    [36, 24, 24],
    [36, 36, 24],
    [36, 36, 36],
    [48, 36, 36],
    [48, 48, 36],
    [48, 48, 48],
    [60, 48, 48],
    [60, 60, 48],
    [60, 60, 60],
    [72, 60, 60],
    [72, 72, 60],
    [72, 72, 72],
    [84, 72, 72],
    [84, 84, 72],
    [84, 84, 84],
    [96, 84, 84],
    [96, 96, 84],
    [96, 96, 96],
    [108, 96, 96],
    [108, 108, 96],
    [108, 108, 108],
    [120, 108, 108],
    [120, 120, 108],
    [120, 120, 120],
    [132, 120, 120],
    [132, 132, 120],
    [132, 132, 132],
    [144, 132, 132]
    ]

# end of script
