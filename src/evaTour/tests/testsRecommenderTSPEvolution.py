from pandas import DataFrame
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import readDatasetNYC

import os
import numpy as np

from evaTour.maps.openStreetMaps import showRouteMap
from evaTour.recommenders.recommenderSVDS import RecommenderSVDS
from evaTour.recommenders.recommenderTSPEvolution import getRecTSPEvolution
from evaTour.recommenders.recommenderTSPEvolution import getRecTSPEvolution2

def test01():
    print("test01")

    ratingsDF:DataFrame
    itemsDF:DataFrame
    distancesDF:DataFrame
    ratingsDF, itemsDF, distancesDF = readDatasetNYC()

    userID = 1
    k = 20

    recom = getRecTSPEvolution(ratingsDF, itemsDF, distancesDF)
    recom.train(ratingsDF, itemsDF, distancesDF)
    recomendation = recom.recommend(userID, k)

    print("recomendation: " + str(recomendation))


def test02():
    print("test02")

    ratingsDF:DataFrame
    itemsDF:DataFrame
    distancesDF:DataFrame
    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()

    userID = 1
    k = 15
    DEBUG = True

    r = RecommenderSVDS({RecommenderSVDS.ARG_K:8})
    r.train(ratingsNYcDF, itemsNYcDF, distancesNYcDF)
    recommendation = r.recommend(userID, k)
    rItemIDs, rScores = list(recommendation.keys()), list(recommendation.values)
    print("rItemIDs: " + str(rItemIDs))
    print("rScores: " + str(rScores))

    recom = getRecTSPEvolution2(ratingsNYcDF, itemsNYcDF, distancesNYcDF, rItemIDs, rScores)
    recom.train(ratingsNYcDF, itemsNYcDF, distancesNYcDF)
    recomendation = recom.recommend(userID, k, DEBUG)

    print("recomendation: " + str(recomendation))
    rItemIDs, rScores = list(recommendation.keys()), list(recommendation.values)
    print("rItemIDs: " + str(rItemIDs))
    print("rScores: " + str(rScores))

    # select rows and columns with index positions
    distancesSelDF = distancesNYcDF.iloc[rItemIDs, rItemIDs]
    distance_matrix = distancesSelDF.to_numpy()

    permutationOfIndexes, distance = solve_tsp_local_search(distance_matrix)

    # use numpy.take() to retrieve elements
    # from input list at given indices
    permutation = np.take(rItemIDs, permutationOfIndexes)

    showRouteMap(permutation, itemsNYcDF)


if __name__ == "__main__":
    os.chdir('../../../')
    #test01()
    test02()
    #test03()