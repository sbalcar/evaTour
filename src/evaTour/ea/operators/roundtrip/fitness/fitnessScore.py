from typing import List

from pandas import DataFrame
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import _getItemIDDistance

import numpy as np


class FitnessScore:

    def __init__(self, recomItemIDs:List, recomScores:List):
        self.recomItemIDs:float = recomItemIDs
        self.recomScores:float = recomScores

    def run(self, individual:List, debug=False):
        if not isinstance(individual, list):
            raise Exception("Individual is not list: " + str(individual))

        scores:List = []
        for itemIdI in individual:
            indexI:int = self.recomItemIDs.index(itemIdI)
            scoreI:float = self.recomScores[indexI]
            scores.append(scoreI)
        return sum(scores)
