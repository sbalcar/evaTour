import sys
from typing import List

from pandas import DataFrame
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import _getItemIDDistance

import numpy as np

from evaTour.ea.individuals.individualCluster import IndividualCluster


class FitnessKmPrecalculatedTSP:

    def __init__(self, itemsDF:DataFrame, distancesDF:DataFrame):
        self.itemsDF: float = itemsDF
        self.distancesDF: float = distancesDF

    def run(self, individual:IndividualCluster, debug=False):
        if not isinstance(individual, IndividualCluster):
            raise Exception("Individual is not IndividualCluster: " + str(individual))
        individualList:List = individual.getUnraveledItemIds(self.distancesDF)
        return self.runList(individualList, debug)

    def runList(self, individual:List, debug=False):
        if not isinstance(individual, list):
            raise Exception("Individual is not list: " + str(individual))

        individualShifted = list(individual[1::]) + list([individual[0]])
        pairs:List = list(zip(individual, individualShifted))

        km = sum([self.distancesDF.iloc[pID1, pID2] for pID1, pID2 in pairs])
        return km

    def removeTheMostHarmfulItem(self, individualClu:IndividualCluster, idealRoundtripLength:int, debug=False):
        individual = individualClu.getUnraveledItemIds(self.distancesDF)
        kmCurrent = self.run(individualClu, debug)
        if kmCurrent < idealRoundtripLength:
            return individual

        theBestAbsValue = sys.maxsize
        theBestIndividual = list(individual)
        for indexI in range(len(individual)-1):
            individualNewI:List = individual[0:indexI] + individual[indexI+1:len(individual)]
            individualClusterNewI = IndividualCluster(individualNewI)
            kmI = self.run(individualClusterNewI, debug)
            absValueI = abs(kmI - idealRoundtripLength)
            if absValueI < theBestAbsValue:
                theBestAbsValue = absValueI
                theBestIndividual = individualNewI

        return IndividualCluster(theBestIndividual)