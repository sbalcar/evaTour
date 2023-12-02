from evaTour.ea.operators.selectionGeneral.selectionRoulette import SelectionRoulette

import random

from numpy.random import randint
from typing import List
import os

class GeneratorRtRoulette:

    def __init__(self, indivSize:int, itemIDs:List, scores:List):
        if len(itemIDs) != len(set(itemIDs)):
            raise Exception("Arg itemIDs has wrong length!")

        self.indivSize = indivSize
        self.itemIDs = itemIDs
        self.scores = scores

    def run(self, popSize, debug=False):

        #    normScoresValues = [(vI - min(scores)) / (max(scores) - min(scores)) for vI in scores]
        #    invNormScoresValues = [1.000001 - vI for vI in normScoresValues]
        invNormScoresValues = self.scores

        pop = []
        for _ in range(popSize):
            itemIDsI = list(self.itemIDs)
            invNormScoresValuesI = list(invNormScoresValues)
            indivI = []
            for _ in range(self.indivSize):
                indexJ = SelectionRoulette()._rouletteSel(invNormScoresValuesI)

                itemIDI = itemIDsI.pop(indexJ)
                invNormScoresValuesI.pop(indexJ)

                indivI.append(itemIDI)

            if len(set(indivI)) != self.indivSize:
                print("len(set(indivI)): " + str(len(set(indivI))))
                print("indivSize: " + str(self.indivSize))
                indivI.sort()
                print("indivI: " + str(indivI))
                raise Exception("Individual has wrong length!")
            pop.append(indivI)

        return pop