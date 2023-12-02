import random
from typing import List

from numpy.random import rand, randint

from evaTour.ea.individuals.individualClusters import IndividualClusters


class CrossoverRtPMX:

    #def __init__(self):

    def run(self, parent1:dict, parent2:dict, debug=False):
        if len(parent1) != len(parent2):
            raise Exception("Parents have not the same length!")

        #sliceIndex1 = 3
        #sliceIndex2 = 7
        sliceIndex1:int = int(random.random() * len(parent1))
        sliceIndex2:int = int(random.random() * len(parent1))

        if sliceIndex1 > sliceIndex2:
            sliceIndex1, sliceIndex2 = sliceIndex2, sliceIndex1

        child1:List = parent1.copy()
        child2:List = parent2.copy()

        mapping1:dict = {}
        mapping2:dict = {}

        # Map slice
        for i in range(sliceIndex1, sliceIndex2):
            mapping1[parent2[i]] = parent1[i]
            child1[i] = parent2[i]

            mapping2[parent1[i]] = parent2[i]
            child2[i] = parent1[i]

        # repair lower slice
        for i in range(sliceIndex1):
            while child1[i] in mapping1:
                #print("parent1: " + str(parent1))
                #print("parent2: " + str(parent2))
                child1[i] = mapping1[child1[i]]
            while child2[i] in mapping2:
                child2[i] = mapping2[child2[i]]

        # repair upper slice
        for i in range(sliceIndex2, len(child1)):
            while child1[i] in mapping1:
                child1[i] = mapping1[child1[i]]
            while child2[i] in mapping2:
                child2[i] = mapping2[child2[i]]

        return [child1, child2]
