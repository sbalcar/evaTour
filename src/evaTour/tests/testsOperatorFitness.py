from typing import List
from pandas import DataFrame

import os

from evaTour.datasets.datasetFoursquare import readDatasetNYC
from evaTour.ea.individuals.individualClusters import IndividualClusters
from evaTour.ea.operators.clusters.fitness.fitnessCluComplexTSP import FitnessCluComplexTSP
from evaTour.ea.operators.roundtrip.fitness.fitnessScore import FitnessScore


def test01():
    print("test01")

    individual:List = [100,200,300]
    recomItemIDs:List = [100,101,200,2021,300]
    recomScores:List = [1,30,1,30,1]

    value = FitnessScore(recomItemIDs, recomScores).run(individual)
    print(value)

def test02():
    print("test02")

    idealRoundtripLength:int = 20
    idealLandmarksCountInRoundtrip:int = 5
    ratingsNYcDF:DataFrame
    itemsNYcDF:DataFrame
    distancesNYcDF:DataFrame
    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()

    individualDict = {0: [220, 173, 59, 1600, 2607], 1: [232, 3880, 21, 4541, 2834], 2: [2479, 31, 298, 4010, 3341]}

    fOpr = FitnessCluComplexTSP(idealRoundtripLength, idealLandmarksCountInRoundtrip, itemsNYcDF, distancesNYcDF)
    fitValue:float = fOpr.run(individualDict)
    print("fitValue: " + str(fitValue))

def test03():
    print("test03")

    idealRoundtripLength: int = 20
    idealLandmarksCountInRoundtrip: int = 5
    ratingsDF:DataFrame
    itemsDF:DataFrame
    distancesDF: DataFrame
    ratingsDF, itemsDF, distancesDF = readDatasetNYC()

    debug = False
    idealRoundtripLength:int = 20
    idealLandmarksCountInRoundtrip:int = 5

    individual:IndividualClusters = IndividualClusters({0:[3617, 894, 1044, 900, 4541,1652, 3115, 2573, 3664, 2563, 718, 3214, 4669]})
    #individual:IndividualClusters = IndividualClusters({0:[3617, 894, 1044, 900, 4541,1652, 3115, 2573, 3664, 2563]})

    oprFit = FitnessCluComplexTSP(idealRoundtripLength, idealLandmarksCountInRoundtrip, itemsDF, distancesDF)
    fitVal:float = oprFit.run(individual, debug)

    print("fitVal: " + str(fitVal))


if __name__ == "__main__":
    os.chdir('../../../')
    #test01()
    #test02()
    test03()