from typing import List

from pandas import DataFrame
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import _getItemIDDistance

import numpy as np

from evaTour.ea.individuals.individualClusters import IndividualClusters


class FitnessCluKmPrecalculatedTSP:

    def __init__(self, itemsDF:DataFrame, distancesDF:DataFrame):
        self.itemsDF = itemsDF
        self.distancesDF = distancesDF

    def run(self, individual:IndividualClusters, debug=False):
        if not isinstance(individual, IndividualClusters):
            raise Exception("Individual is not " + str(IndividualClusters.__class__) + ": " + str(individual))
        if not individual.isValid():
            raise Exception("Individual is not valid")

        distances:List = []
        for clusterIdI, clusterI in individual.items():
            kmI = fitnessKmPrecalculatedTSPFnc(clusterI, self.itemsDF, self.distancesDF, debug)
            distances.append(kmI)

        return distances
