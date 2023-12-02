from typing import List

from pandas import DataFrame
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import _getItemIDDistance

import numpy as np

from evaTour.ea.individuals.individualClusters import IndividualClusters
from evaTour.ea.operators.roundtrip.fitness.fitnessKmTSP import FitnessKmTSP
from evaTour.ea.operators.roundtrip.fitness.fitnessKmTSPSolver import FitnessKmTSPSolver


class FitnessCluKmTSPSolver:

    def __init__(self, itemsDF:DataFrame, distancesDF:DataFrame):
        self.itemsDF:float = itemsDF
        self.distancesDF:float = distancesDF

    def run(self, individual:IndividualClusters, debug=False):
        if not isinstance(individual, IndividualClusters):
            raise Exception("Individual is not IndividualClusters: " + str(individual))

        unraveleIndividual:IndividualClusters = individual.exportUnraveledPermutation(self.distancesDF)

        clustersOfItemIdsDict:dict = unraveleIndividual.clustersOfItemIdsDict

        self.fitnessValues:List[float] = []
        for clusterIdI, clusterI in clustersOfItemIdsDict.items():
            oprtI = FitnessKmTSP(self.itemsDF, self.distancesDF)
            fitnessI:float = oprtI.run(clusterI, debug)
            self.fitnessValues.append(fitnessI)

        return sum(self.fitnessValues)