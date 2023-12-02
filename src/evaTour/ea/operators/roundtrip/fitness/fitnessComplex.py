from typing import List

from pandas import DataFrame
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import _getItemIDDistance

import numpy as np

from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP
from evaTour.ea.operators.roundtrip.fitness.fitnessScore import FitnessScore


class FitnessComplex:

    def __init__(self, idealNumbeOfStopsInRoundtrip:int, idealLengthOfRoundtrip:int, recomItemIDs:List, recomScores:List, itemsDF:DataFrame, distancesDF:DataFrame):
        if not isinstance(itemsDF, DataFrame):
            raise Exception("Argument itemsDF is not DataFrame: " + str(itemsDF))

        self.idealNumbeOfStopsInRoundtrip:int = idealNumbeOfStopsInRoundtrip
        self.idealLengthOfRoundtrip:int = idealLengthOfRoundtrip
        self.recomItemIDs:List = recomItemIDs
        self.recomScores:List = recomScores
        self.itemsDF:DataFrame = itemsDF
        self.distancesDF:DataFrame = distancesDF

    def run(self, individual:List, debug=False):
        if not isinstance(individual, list):
            raise Exception("Individual is not list: " + str(individual))

        distanceInKkm:float = FitnessKmPrecalculatedTSP(self.itemsDF, self.distancesDF).run(individual)
        numberOfPlaces:int = len(individual)
        scoreSum = FitnessScore(self.recomItemIDs, self.recomScores).run(individual)

        if debug:
            print("distanceInKkm: " + str(distanceInKkm))
            print("numberOfPlaces: " + str(numberOfPlaces))
            print("scoreSum: " + str(scoreSum))

    #    return distanceInKkm / (1+scoreSum)  +  distanceInKkm * abs(idealNumbeOfStopsInRoundtrip - len(individual))/(1+scoreSum)
        return abs(distanceInKkm -self.idealNumbeOfStopsInRoundtrip) / (1+scoreSum)  +  0.5*abs(self.idealNumbeOfStopsInRoundtrip - len(individual))/(1+scoreSum)
    #    return abs(distanceInKkm - idealLengthOfRoundtrip +7) / (1+scoreSum)  +  abs(distanceInKkm - idealLengthOfRoundtrip -7) / (1+scoreSum)  +  10* abs(idealNumbeOfStopsInRoundtrip - len(individual))/(1+scoreSum)