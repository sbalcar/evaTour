import random
from typing import List

from numpy.random import rand, randint


class CrossoverRtOnePoint:

    def __init__(self, crossRate:float):
        self.crossRate:float = crossRate

    def run(self, p1:List, p2:List, debug=False):
        if len(p1) != len(p2):
            raise Exception("Parents have not the same length!")

        # children are copies of parents by default
        ch1, ch2 = p1.copy(), p2.copy()
        # check for recombination
        if rand() < self.crossRate:
            # select crossover point that is not on the end of the string
            pt = randint(1, len(p1) - 2)
            # perform crossover
            ch1 = p1[:pt] + p2[pt:]
            ch2 = p2[:pt] + p1[pt:]
        return [ch1, ch2]