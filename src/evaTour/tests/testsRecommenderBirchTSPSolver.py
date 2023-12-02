from pandas import DataFrame
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import _getDistance, _getVenueCategoryName, getVisitedPlacesOfUser, divideTrainTest
from evaTour.datasets.datasetFoursquare import _getGPS
from evaTour.datasets.datasetFoursquare import readDatasetNYC, readDatasetTKY
from evaTour.datasets.datasetFoursquare import transformDataset

import pandas as pd
import os

from evaTour.ea.individuals.individualClusters import IndividualClusters
from evaTour.maps.openStreetMaps import showRouteMaps
from evaTour.recommenders.recommenderSVDS import RecommenderSVDS
from evaTour.recommenders.recommenderBirchTSPSolver import RecommenderBirchTSPSolver


def test01():
    print("")

    userID = 1001
    DEBUG = False

    ratingsDF:DataFrame
    itemsDF:DataFrame
    distancesDF:DataFrame
    ratingsDF, itemsDF, distancesDF = readDatasetNYC()
    #ratingsDF, itemsDF, distancesDF = readDatasetTKY()

    argsDict = {RecommenderBirchTSPSolver.ARG_RECOMMENDER_CLASS:RecommenderSVDS,
                RecommenderBirchTSPSolver.ARG_RECOMMENDER_ARGS:{RecommenderSVDS.ARG_K:8},
                RecommenderBirchTSPSolver.ARG_RECOMMENDATION_POOL_SIZE:100,
                RecommenderBirchTSPSolver.ARG_CLUSTER_THRESHOLD:0.001,
                RecommenderBirchTSPSolver.ARG_CLUSTER_COUNT:10,
                RecommenderBirchTSPSolver.ARG_PYTHON_TSP_HEURISTIC_FNC:solve_tsp_local_search}

    r = RecommenderBirchTSPSolver(argsDict, DEBUG)
    r.train(ratingsDF, itemsDF, distancesDF)
    recomendationDict:dict = r.recommendClusters(userID)

    rClusterItemsDict:dict = {clusterIdI:itemIdsSerI.keys() for clusterIdI, itemIdsSerI in recomendationDict.items()}
    showRouteMaps(rClusterItemsDict.values(), itemsDF)



if __name__ == "__main__":
    os.chdir('../../../')
    print("")
    test01()