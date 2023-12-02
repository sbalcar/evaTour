from numpy.random import randint
from typing import List
import numpy as np
import random, pdb

class SelectionRandom:

    def run(self, pop:List, fitnessValues:List, countOfSelectedItem:int):
        if not isinstance(pop, list):
            raise Exception("Argument pop is not " + str(list) + ": " + str(pop))
        if not isinstance(fitnessValues, list):
            raise Exception("Argument fitnessValues is not " + str(list) + ": " + str(fitnessValues))
        if len(pop) == 0:
            raise Exception("Arg pop is empty list")
        if len(pop) != len(fitnessValues):
            raise Exception("Not the same length")

        if len(pop) <= countOfSelectedItem:
            return pop

        return random.sample(pop, countOfSelectedItem)
