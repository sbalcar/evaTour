import sys
from typing import List

from pandas import DataFrame
from pandas import Series

import random

from numpy.random import randint
from typing import List
import os

from evaTour.ea.individuals.individualCluster import IndividualCluster
from evaTour.ea.individuals.individualClusters import IndividualClusters
from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP


class MutationCluImproveCluster:

    def __init__(self, itemsDF:DataFrame, distancesDF:DataFrame, nearestNeighborsOfItemIdsDict:dict,
                 idealRoundtripLength:int, idealLandmarksCountInRoundtrip:int, debug:bool=False):
        if not isinstance(itemsDF, DataFrame):
            raise Exception("Argument itemsDF is not " + str(DataFrame) + ": " + str(itemsDF))
        if not isinstance(distancesDF, DataFrame):
            raise Exception("Argument distancesDF is not " + str(DataFrame) + ": " + str(distancesDF))
        if not isinstance(nearestNeighborsOfItemIdsDict, dict):
            raise Exception("Argument nearestNeighborsOfItemIdsDict is not " + str(dict) + ": " + str(nearestNeighborsOfItemIdsDict))
        if not isinstance(idealRoundtripLength, int):
            raise Exception("Argument idealRoundtripLength is not " + str(int) + ": " + str(idealRoundtripLength))
        if not isinstance(idealLandmarksCountInRoundtrip, int):
            raise Exception("Argument idealLandmarksCountInRoundtrip is not " + str(int) + ": " + str(idealLandmarksCountInRoundtrip))

        self.itemsDF:DataFrame = itemsDF
        self.distancesDF:DataFrame = distancesDF
        self.nearestNeighborsOfItemIdsDict:dict[int,Series] = nearestNeighborsOfItemIdsDict
        self.idealRoundtripLength:int = idealRoundtripLength
        self.idealLandmarksCountInRoundtrip:int = idealLandmarksCountInRoundtrip


    def run(self, individual:IndividualClusters, mutationRate:float, debug=False):
        if not isinstance(individual, IndividualClusters):
            raise Exception("Argument individual is not " + str(IndividualClusters) + ": " + str(individual))

        individualUnraveled:IndividualClusters = individual.exportUnraveledPermutation(self.distancesDF)

        newIndividual:IndividualClusters = individualUnraveled.clone()
        for clusterIdI, clusterI in individualUnraveled.individualsDict.items():
            ncItemIdsI:List = self._improveCluster(clusterI, debug)
            newIndividual.setIndivClusterByClusterId(clusterIdI, ncItemIdsI)

        return newIndividual

    def _improveCluster(self, clusterI:IndividualCluster, debug=False):
        #cItemIdsI = clusterI.getUnraveledItemIds(self.distancesDF)

        oprtI = FitnessKmPrecalculatedTSP(self.itemsDF, self.distancesDF)
        fitnessKmI:float = oprtI.run(clusterI, debug)

        #print("fitnessKmI: " + str(fitnessKmI))
        #print("idealRoundtripLength: " + str(self.idealRoundtripLength))

        if fitnessKmI > self.idealRoundtripLength:
            #print("DEL")
            #print("cItemIdsI: " + str(cItemIdsI))
            newClusterOfItemIds = oprtI.removeTheMostHarmfulItem(clusterI, self.idealRoundtripLength)
            return self._improveCluster(newClusterOfItemIds, debug)

        return clusterI