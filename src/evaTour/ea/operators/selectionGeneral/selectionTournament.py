from numpy.random import randint
from typing import List
import numpy as np
import random,pdb
import operator

import math


class SelectionTournament:

    def __init__(self, k:int):
        self.k:int = k

    def run(self, pop, fitnessValues:List, countOfSelectedItem:int):
        selIndiv:List = []
        for _ in range(countOfSelectedItem):
            selIndivI = self.__tournamentSel(pop, fitnessValues)
            selIndiv.append(selIndivI)
        return selIndiv

    def __tournamentSel(self, pop:List, fitnessValues:List):
        bestIndex = -1
        for _ in range(self.k):
            rndIndex = random.randrange(0, len(pop)-1)
            if (bestIndex == -1) or fitnessValues[rndIndex] > fitnessValues[bestIndex]:
                bestIndex = rndIndex
        return pop[bestIndex]
