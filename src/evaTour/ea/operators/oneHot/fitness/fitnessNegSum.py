from typing import List

from pandas import DataFrame
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import _getItemIDDistance

import numpy as np


class FitnessNegSum:

    def run(self, individual:List, debug=False):
        if not isinstance(individual, list):
            raise Exception("Individual is not list: " + str(individual))

        return -sum(individual)
