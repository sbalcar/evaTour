from typing import List

from pandas import DataFrame
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import _getItemIDDistance

import numpy as np

class FitnessKmTSPSolver:

    def __init__(self, itemsDF:DataFrame, distancesDF:DataFrame):
        self.itemsDF:float = itemsDF
        self.distancesDF:float = distancesDF

    def run(self, individual:List, debug=False):
        if not isinstance(individual, list):
            raise Exception("Individual is not list: " + str(individual))

        if debug:
            print("individual: " + str(individual))

        self.permutation = individual.exportUnraveledPermutation(self.distancesDF)

        permutationShifted = list(self.permutation[1::]) + list([self.permutation[0]])

        pairs:List = list(zip(self.permutation, permutationShifted))

        km = sum([self.distancesDF.iloc[pID1, pID2] for pID1, pID2 in pairs])
        return km
