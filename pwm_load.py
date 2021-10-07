# script to convert load for a finely controlled step size

min_step = 0
max_step = 180


def load_interp(load):

    res_lvl = load/10                       # divide the level by 10 for resolution
    res_stage = int(res_lvl)                # round the number down to nearest integer

    pwm_level = res_lvl - res_stage         # set pwm signal as value in between stages
    kw_level = res_lvl*1.44                 # kw level rounded to nearest number
    kw_display = round(kw_level, 1)
    currents = current_multiple(res_stage, pwm_level)

    print(kw_display, currents)


def current_multiple(stage, pwm_sig):
    cf = 12                     # current factor of 12 amps
    phase3 = stage // 3                         # see how many times multiples of 3 can fit in
    rem = stage - phase3*3                      # remaining resistors after 3 multiple
    if rem == 1:                                # if 1 remaining, add to first phase
        cs = [phase3+1, phase3, phase3]
    elif rem == 2:                              # if 2 remaining, add to second phase
        cs = [phase3+1, phase3+1, phase3]
    else:
        cs = [phase3, phase3, phase3]           # otherwise, have all phases equal

    # current calculation
    currents = [cs[0]*cf, cs[1]*cf, (cs[2] + pwm_sig)*cf]
    return currents


load_interp(25)

# end
