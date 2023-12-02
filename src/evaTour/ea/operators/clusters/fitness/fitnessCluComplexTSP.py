from typing import List

from pandas import DataFrame
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import _getItemIDDistance

import numpy as np

from evaTour.ea.individuals.individualClusters import IndividualClusters
from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP
from evaTour.ea.operators.roundtrip.fitness.fitnessKmTSPSolver import FitnessKmTSPSolver


class FitnessCluComplexTSP:

    def __init__(self, idealRoundtripLength:int, idealLandmarksCountInRoundtrip:int,
                 rScorePoolDict:dict, itemsDF:DataFrame, distancesDF:DataFrame):
        if idealRoundtripLength <= 0:
            raise Exception("Argument idealRoundtripLength doesn't contain correct value: " + str(idealRoundtripLength))
        if idealLandmarksCountInRoundtrip <= 0:
            raise Exception("Argument idealLandmarksCountInRoundtrip doesn't contain correct value: " + str(idealLandmarksCountInRoundtrip))
        if not isinstance(rScorePoolDict, dict):
            raise Exception("Argument rScorePoolDict is not dict: " + str(rScorePoolDict))
        if not isinstance(itemsDF, DataFrame):
            raise Exception("Argument itemsDF is not DataFrame: " + str(itemsDF))
        if not isinstance(distancesDF, DataFrame):
            raise Exception("Argument distancesDF is not DataFrame: " + str(distancesDF))

        self.rItemIdsPoolScoreDict:dict = rScorePoolDict

        self.itemsDF:DataFrame = itemsDF
        self.distancesDF:DataFrame = distancesDF
        self.idealRoundtripLength:int = idealRoundtripLength
        self.idealLandmarksCountInRoundtrip:int = idealLandmarksCountInRoundtrip

    def run(self, individual:IndividualClusters, debug=False):
        if not isinstance(individual, IndividualClusters):
            raise Exception("Individual is not " + str(IndividualClusters.__class__) + ": " + str(individual))
        if not individual.isValid():
            raise Exception("Individual is not valid")

        individualUnraveled:IndividualClusters = individual.exportUnraveledPermutation(self.distancesDF)
        individualDict:dict = individualUnraveled.individualsDict

        fitnessKm:List = []
        for clusterIdI, clusterI in individualDict.items():
            oprtI = FitnessKmPrecalculatedTSP(self.itemsDF, self.distancesDF)
            fitnessKmI:float = oprtI.run(clusterI, debug)
            fitnessKm.append(fitnessKmI)

        #print("fitnessKm: " + str(fitnessKm))
        #print("individualDict: " + str(individualDict))

        fitDistanceKmRate:List = [1 - (abs(fitValI - self.idealRoundtripLength) / (10 * self.idealRoundtripLength))
                           for fitValI in fitnessKm]
        fitLandmarkRate:List = [1 - (1 / (abs(self.idealLandmarksCountInRoundtrip - len(clusterI.getUnraveledItemIds(self.distancesDF))) + 1))
                            for _, clusterI in individualDict.items()]
        fitScoreRate:List = []
        for clusterIdI, clusterI in individualDict.items():
            clusterScoresI = [self.rItemIdsPoolScoreDict.get(itemIdJ,0) for itemIdJ in clusterI.getUnraveledItemIds(self.distancesDF)]
            clusterScoreRateI = sum(clusterScoresI) / len(clusterScoresI)
            fitScoreRate.append(clusterScoreRateI)

        if debug:
            print("fitRateKm: " + str(fitDistanceKmRate))
            print("fitRatteOfLm: " + str(fitLandmarkRate))
            print("fitScoreRate: " + str(fitScoreRate))
            print("fitRateKmSum: " + str(sum(fitDistanceKmRate)))
            print("fitRatteOfLmSum: " + str(sum(fitLandmarkRate)))
            print("fitScoreRateSum: " + str(sum(fitScoreRate)))

        return 3*sum(fitDistanceKmRate) + sum(fitLandmarkRate) + sum(fitScoreRate)
        #return sum(fitDistanceKmRate)
        #return -sum(fitnessKm)
