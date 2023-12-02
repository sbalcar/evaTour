from numpy.random import randint
from typing import List
import numpy as np
import random, pdb
import operator

import math


class SelectionRoulette:

    def __init__(self, maximization:bool, debug:bool=False):
        if not isinstance(maximization, bool):
            raise Exception("Argument maximization is not " + str(bool) + ": " + str(maximization))
        self.maximization = maximization

    def isMaximization(self):
        return self.maximization

    def run(self, pop:List, fitnessValues:List, countOfSelectedItem:int):
        if not isinstance(pop, list):
            raise Exception("Argument pop is not " + str(list) + ": " + str(pop))
        if not isinstance(fitnessValues, list):
            raise Exception("Argument fitnessValues is not " + str(list) + ": " + str(fitnessValues))
        if len(pop) == 0:
            raise Exception("Arg pop is empty list")
        if len(pop) != len(fitnessValues):
            raise Exception("Not the same length")

        #print("len(pop): " + str(len(pop)))
        if len(pop) <= countOfSelectedItem:
            return pop

        #print("fitnessValues: " + str(fitnessValues))

        popI = list(pop)
        normFitnessValuesI = [(vI - min(fitnessValues)) / (max(fitnessValues) - min(fitnessValues)) for vI in
                              fitnessValues]

        if not self.maximization:
            normFitnessValuesI = [1.000001 - vI for vI in normFitnessValuesI]


        selItems = []
        for i in range(countOfSelectedItem):
            selectedIndexI = self._rouletteSel(list(normFitnessValuesI))
            # print("selectedIndexI: " + str(selectedIndexI))
            selectedItemI = popI[selectedIndexI]

            popI.pop(selectedIndexI)
            normFitnessValuesI.pop(selectedIndexI)

            selItems.append(selectedItemI)

        return selItems

    def _rouletteSel(self, weights:List):
        #print("weights: " + str(weights))
        if math.isnan(sum(weights)):
            raise Exception("Wrong weights")

        # sorting weights in ascending order
        indexedWeightsSorted = sorted(enumerate(weights), key=operator.itemgetter(1));
        indices, weightsSorted = zip(*indexedWeightsSorted);
        # calculate sum of probability
        sumOfAll = sum(weightsSorted)
        prob = [x / sumOfAll for x in weightsSorted]
        cumProb = np.cumsum(prob)
        # select a random a number in the range [0,1]
        randNum = random.random()

        for indexValueI, cumProbValueI in zip(indices, cumProb):
            if randNum < cumProbValueI:
                return indexValueI
