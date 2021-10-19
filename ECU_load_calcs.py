# script to convert load for a finely controlled step size

min_step = 0
max_step = 360
i_s = 20


# calculate load setting for a given input. 10 represents a full resistor
def load_interp(r_level):

    # setting the range of r_level if out of scale
    if r_level < min_step:
        r_level = min_step
    elif r_level > max_step:
        r_level = max_step

    ssr_lvl = r_level/i_s                    # divide the level by 20 for big ssr command in range of 0-18
    res_stage = int(ssr_lvl)                # round the number down to nearest integer to set the ssr resistive level

    # calculate the remain percentage for sending level to small ssr bank
    small_res_stage = r_level - (res_stage * i_s)           # set partial signal as value in between stages.

    kw_level = ssr_lvl*1.44/i_s                             # kw level rounded to nearest number
    kw_display = round(kw_level, 1)

    # calculate current from resistive stage and pwm level
    currents = current_multiple(res_stage, small_res_stage)

    return res_stage, small_res_stage, kw_display, currents


def current_multiple(stage, small_res_stage):
    cf = 12                     # current factor of 12 amps
    phase3 = stage // 3                         # see how many times multiples of 3 can fit in
    rem = stage - phase3*3                      # remaining resistors after 3 multiple
    if rem == 1:                                # if 1 remaining, add to first phase
        cs = [phase3+1, phase3, phase3]
    elif rem == 2:                              # if 2 remaining, add to second phase
        cs = [phase3+1, phase3+1, phase3]
    else:
        cs = [phase3, phase3, phase3]           # otherwise, have all phases equal

    # current calculation for the pwm signal current
    partial_current = int(round((cs[2] + small_res_stage/i_s)*cf, 0))

    currents = [cs[0]*cf, cs[1]*cf, partial_current]
    return currents


# end
