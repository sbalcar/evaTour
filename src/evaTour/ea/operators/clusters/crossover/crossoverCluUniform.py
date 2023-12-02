from random import random
from typing import List

from pandas import DataFrame
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import _getItemIDDistance

import numpy as np

from evaTour.ea.individuals.individualClusters import IndividualClusters
from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP


class CrossoverCluUniform:

    def __init__(self, itemsDF:DataFrame, distancesDF:DataFrame):
        if not isinstance(itemsDF, DataFrame):
            raise Exception("Param itemsDF is not DataFrame: " + str(itemsDF))
        if not isinstance(distancesDF, DataFrame):
            raise Exception("Param distancesDF is not DataFrame: " + str(distancesDF))

        self.itemsDF:DataFrame = itemsDF
        self.distancesDF:DataFrame = distancesDF

    def run(self, indivParent1:IndividualClusters, indivParent2:IndividualClusters, debug=False):
        if not isinstance(indivParent1, IndividualClusters):
            raise Exception("Argument parent1 is not " + str(IndividualClusters) + ": " + str(indivParent1))
        if not isinstance(indivParent2, IndividualClusters):
            raise Exception("Argument parent2 is not " + str(IndividualClusters) + ": " + str(indivParent2))
        if not indivParent1.isValid():
            raise Exception("Argument parent1 is not valid")
        if not indivParent2.isValid():
            raise Exception("Argument parent2 is not valid")
        parent1:IndividualClusters = indivParent1.clone()
        parent2:IndividualClusters = indivParent2.clone()
        #if len(parent1.getUnraveledItemIds(self.distancesDF)) != len(parent2.getUnraveledItemIds(self.distancesDF)):
        #    raise Exception("Parents have not the same length!")

        #TODO
        return [parent1, parent2]

        # children are copies of parents by default
        ch1, ch2 = parent1.copy(), parent2.copy()

        for clusterIdI in ch1.keys():
            if random() > 0.5:
                ch1Val = ch1[clusterIdI]
                ch2Val = ch2[clusterIdI]
                ch1[clusterIdI] = ch2Val
                ch2[clusterIdI] = ch1Val

        return [IndividualClusters(ch1, False), IndividualClusters(ch2, False)]

