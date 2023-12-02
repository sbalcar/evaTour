import random

from numpy.random import randint
from typing import List
import os

class MutationRt2Opt:

    def run(self, individual:List, mutationRate:float, debug=False):
    #    if len(set(individual)) != 20:
    #        raise Exception("Not the right length of individual")

        if random.random() > mutationRate:
            return individual

        index1:int = int(random.random() * len(individual))
        index2:int = int(random.random() * len(individual))

        if index1 > index2:
            index1, index2 = index2, index1

        partStart:List = individual[:index1]
        partMiddle:List = individual[index1:index2]
        partMiddle.reverse()
        partEnd:List = individual[index2:]

        #print("index1: " + str(index1))
        #print("index2: " + str(index2))
        #print()

        #print("partStart: " + str(partStart))
        #print("partMiddle: " + str(partMiddle))
        #print("partEnd: " + str(partEnd))

        newIndiv = partStart + partMiddle + partEnd

        if len(set(newIndiv)) != len(newIndiv):
            raise Exception("Not the right length of individual")

        return newIndiv
