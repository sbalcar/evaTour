import random

from numpy.random import randint
from typing import List
import os

class GeneratorRtPerm:

    def __init__(self, indivPerm:List):
        self.indivPerm = indivPerm

    def run(self, popSize, debug=False):
        pop = [random.sample(self.indivPerm, k=len(self.indivPerm)) for _ in range(popSize)]
        return pop