import random

from numpy.random import randint
from typing import List
import os

class MutationRtSwap:

    def run(self, individual:List, mutationRate:float, debug=False):
        for swapped in range(len(individual)):
            import random
            if (random.random() < mutationRate):
                swapWith = int(random.random() * len(individual))

                city1 = individual[swapped]
                city2 = individual[swapWith]

                individual[swapped] = city2
                individual[swapWith] = city1
        return individual

