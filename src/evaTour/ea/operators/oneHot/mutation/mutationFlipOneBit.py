import random
from numpy.random import rand

from numpy.random import randint
from typing import List
import os

class MutationFlipOneBit:

    def __init__(self, mutationRate:float):
        self.mutationRate:float = mutationRate

    def run(self, individual:List, debug=False):
        individualCopy = individual.copy()
        for i in range(len(individualCopy)):
            # check for a mutation
            if rand() < self.mutationRate:
                # flip the bit
                individualCopy[i] = 1 - individualCopy[i]
        return individualCopy