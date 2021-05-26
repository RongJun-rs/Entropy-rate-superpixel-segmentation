import numpy as np
from utils.utils import *
from utils.utils import lut

@timeit(20)
def repeatonarray(func,inpt):
    for el in inpt:
        func(el)
    return

if __name__ == '__main__':
    z = list(lut.keys())

    repeatonarray(partial_entropy_single,z)
    repeatonarray(partial_entropy_single_lut_mode,z)
    repeatonarray(partial_entropy_single_lut_mode_with_rounded_input,z)

