from typing import List

from pandas import DataFrame
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import _getItemIDDistance

import numpy as np

class FitnessKmTSP:

    def __init__(self, itemsDF:DataFrame):
        self.itemsDF:float = itemsDF

    def run(self, individual:List, debug=False):
        if not isinstance(individual, list):
            raise Exception("Individual is not list: " + str(individual))

        individualShifted = list(individual[1::]) + list([individual[0]])
        pairs:List = list(zip(individual, individualShifted))

        km = sum([_getItemIDDistance(self.itemsDF, pID1, pID2) for pID1, pID2 in pairs])
        return km