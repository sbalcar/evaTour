import sys
from typing import List

from pandas import DataFrame
from pandas import Series

from evaTour.datasets.datasetFoursquare import getNearestNeighbors, readDatasetNYC
from evaTour.ea.individuals.individualClusters import IndividualClusters
from evaTour.ea.operators.clusters.mutation.mutationCluImproveCluster import MutationCluImproveCluster
from evaTour.ea.operators.oneHot.mutation.mutationFlipOneBit import MutationFlipOneBit
from evaTour.ea.operators.roundtrip.mutation.mutationRtSwap import MutationRtSwap
from evaTour.ea.operators.roundtrip.mutation.mutationRt2Opt import MutationRt2Opt
import os

from evaTour.maps.openStreetMaps import showRouteMaps


def test01():
    individual = [1,0,0,0]
    individual2 = MutationFlipOneBit().run(individual, 0.5)
    print(individual2)

def test02():
    print("test04")

    a = MutationRtSwap().run([1, 2, 3, 4, 5], 0.2)
    print(a)

def test03():
    print("test03")

    a = MutationRt2Opt().run([1, 2, 3, 4, 5], 1.0)
    print(a)

def test04():
    print("test04")

    ratingsNYcDF:DataFrame
    itemsNYcDF:DataFrame
    distancesNYcDF:DataFrame
    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()

    userID:int = 1001
    DEBUG:bool = False

    IDEAL_ROUNDTRIP_LENGTH:int = 25
    IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP:int = 20

    nearestNeighborsOfItemIdsDict:dict = getNearestNeighbors(distancesNYcDF, 5)

    iterCount:int = 5
    popSize:int = 10
    crossRate:float = 0.1
    mutRate:float = 0.5

    itemIds:List = [2717, 1989, 1246, 2475, 3592, 1295, 1652, 3880, 1044, 3214, 718, 3664]
    itemIds:List = [2717, 3664, 718, 2530, 3214, 1044, 3880, 4548, 2545, 1652, 3380, 1295, 2567, 3592, 2475, 1246, 1703, 1989, 3123, 3414]
    individual = IndividualClusters({0:itemIds}, True)
    opr = MutationCluImproveCluster(itemsNYcDF, distancesNYcDF, nearestNeighborsOfItemIdsDict,
                            IDEAL_ROUNDTRIP_LENGTH, IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP)

    individualResult = opr.run(individual, 0.5)
    print(individualResult)
    showRouteMaps(individualResult.clustersOfItemIdsDict.values(), itemsNYcDF)


if __name__ == "__main__":
    os.chdir('../../../')
    print("")
    #test01()
    #test02()
    #test03()
    test04()