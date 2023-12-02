import sys
from typing import List

from pandas import DataFrame
from pandas import Series

import os

from evaTour.datasets.datasetFoursquare import readDatasetNYC
from evaTour.ea.individuals.individualClusters import IndividualClusters
from evaTour.ea.operators.clusters.fitness.fitnessCluComplexTSP import FitnessCluComplexTSP
from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP


def test01():
    print("test01")

    ratingsNYcDF:DataFrame
    itemsNYcDF:DataFrame
    distancesNYcDF:DataFrame
    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()

    idealRoundtripLength:int = 11
    idealLandmarksCountInRoundtrip:int = 15

    # item 1434 je nejvzdalenejsi a mel by byt vymazan
    individual:List = [1434,2242,4268,1764,3174,3314,3246,1745,3424,4389,5022,3457]
    rScorePoolDict:dict = {1434:0.1,2242:0.1,4268:0.1,1764:0.1,3174:0.1,3314:0.1,3246:0.1,1745:0.1,3424:0.1,4389:0.1,5022:0.1,3457:0.1}

    oprPrecalculated = FitnessKmPrecalculatedTSP(itemsNYcDF, distancesNYcDF)
    newIndividual:List = oprPrecalculated.removeTheMostHarmfulItem(individual, idealRoundtripLength)
    newRScorePoolDict:dict = {2242:0.1,4268:0.1,1764:0.1,3174:0.1,3314:0.1,3246:0.1,1745:0.1,3424:0.1,4389:0.1,5022:0.1,3457:0.1}

    print(newIndividual)

    print()
    opr = FitnessCluComplexTSP(idealRoundtripLength,idealLandmarksCountInRoundtrip,rScorePoolDict, itemsNYcDF,distancesNYcDF)
    fitnessValue = opr.run(IndividualClusters({0:individual}), True)
    print(fitnessValue)

    print()
    oprNew = FitnessCluComplexTSP(idealRoundtripLength,idealLandmarksCountInRoundtrip,newRScorePoolDict, itemsNYcDF,distancesNYcDF)
    fitnessValueNew = oprNew.run(IndividualClusters({0:newIndividual}), True)
    print(fitnessValueNew)


if __name__ == "__main__":
    os.chdir('../../../')
    test01()
    #test02()
    #test03()