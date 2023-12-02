import random

from numpy.random import randint
from typing import List
import os

class Generator01:

    def __init__(self, n_bits:int):
        self.n_bits = n_bits

    def run(self, popSize:int, debug=False):
        pop = [randint(0, 2, self.n_bits).tolist() for _ in range(popSize)]
        return pop

