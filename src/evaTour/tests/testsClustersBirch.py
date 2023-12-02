from pandas import DataFrame
from pandas import Series
from python_tsp.heuristics import solve_tsp_local_search
from sympy.physics.quantum.circuitplot import matplotlib

from evaTour.datasets.datasetFoursquare import _getDistance, _getVenueCategoryName, getVisitedPlacesOfUser, \
    divideTrainTest, readDatasetTKY
from evaTour.datasets.datasetFoursquare import _getGPS
from evaTour.datasets.datasetFoursquare import readDatasetNYC
from evaTour.datasets.datasetFoursquare import transformDataset

import pandas as pd
import os
import numpy as np

# birch clustering
from numpy import unique
from numpy import where
from sklearn.datasets import make_classification
from sklearn.cluster import Birch
from matplotlib import pyplot
import tkinter

from evaTour.maps.openStreetMaps import convertIndividualToGPS, showRouteMap, showRouteMaps
from evaTour.recommenders.recommenderSVDS import RecommenderSVDS

matplotlib.use('TkAgg')

def test01():
    print("test01")

    # define dataset
    X, _ = make_classification(n_samples=1000, n_features=2, n_informative=2, n_redundant=0, n_clusters_per_class=1, random_state=4)
    print(type(X))
    print(X)
    # define the model
    model = Birch(threshold=0.01, n_clusters=6)
    # fit the model
    model.fit(X)
    # assign a cluster to each example
    yhat = model.predict(X)
    # retrieve unique clusters
    clusters = unique(yhat)
    # create scatter plot for samples from each cluster
    for cluster in clusters:
     # get row indexes for samples with this cluster
     row_ix = where(yhat == cluster)
     # create scatter of these samples
     pyplot.scatter(X[row_ix, 0], X[row_ix, 1])
    # show the plot
    pyplot.show()


def test02():
    print("test02")

    ratingsDF:DataFrame
    itemsDF:DataFrame
    distancesDF:DataFrame
    ratingsDF, itemsDF, distancesDF = readDatasetNYC()
    #ratingsDF, itemsDF, distancesDF = readDatasetTKY()

    userID = 1
    k = 100
    DEBUG = True

    r = RecommenderSVDS({RecommenderSVDS.ARG_K:8})
    r.train(ratingsDF, itemsDF, distancesDF)
    recommendationSer:Series = r.recommend(userID, k)
    rItemIDs, rScores = list(recommendationSer.keys()), list(recommendationSer.values)
    print("rItemIDs: " + str(rItemIDs))
    print("rScores: " + str(rScores))

    gpsCoordsListOfTuple = convertIndividualToGPS(rItemIDs, itemsDF)
    gpsCoords = np.array(gpsCoordsListOfTuple)
    #print("gpsCoords: " + str(gpsCoords))

    # define the model
    model = Birch(threshold=0.01, n_clusters=10)
    # fit the model
    model.fit(gpsCoords)
    # assign a cluster to each example
    yhat = model.predict(gpsCoords)
    # retrieve unique clusters
    clusters = unique(yhat)
    clustersOfItemIdsDict = {}
    # create scatter plot for samples from each cluster
    for clusterIdI in clusters:
        # get row indexes for samples with this cluster
        itemIdsIndexesI = where(yhat == clusterIdI)[0]
        itemIdsI = [rItemIDs[itemIdsIndexI] for itemIdsIndexI in itemIdsIndexesI]
        #print("itemIdsI: " + str(itemIdsI))
        clustersOfItemIdsDict[clusterIdI] = list(itemIdsI)

    clustersOfScoreDict = {}
    for clusterIdI in clustersOfItemIdsDict.keys():
        itemIdsI = clustersOfItemIdsDict[clusterIdI]
        # select rows and columns with index positions
        distancesSelDF = distancesDF.iloc[itemIdsI, itemIdsI]
        distance_matrix = distancesSelDF.to_numpy()

        permutationOfIndexes, distance = solve_tsp_local_search(distance_matrix)

        # use numpy.take() to retrieve elements
        # from input list at given indices
        permutation = np.take(itemIdsI, permutationOfIndexes)
        clustersOfItemIdsDict[clusterIdI] = permutation

        scoresI = [recommendationSer[itemIdI] for itemIdI in permutation]
        clustersOfScoreDict[clusterIdI] = scoresI

    # printing points by pyplot
    for clusterIdI in clustersOfItemIdsDict.keys():
        itemIdsI = clustersOfItemIdsDict[clusterIdI]
        gpsCoordsI = convertIndividualToGPS(itemIdsI, itemsDF)

        itemIds0I = [gpsCoordsIndexI[0] for gpsCoordsIndexI in gpsCoordsI]
        itemIds1I = [gpsCoordsIndexI[1] for gpsCoordsIndexI in gpsCoordsI]

        # create scatter of these samples
        pyplot.scatter(itemIds0I, itemIds1I)
    # show the plot
    #pyplot.show()

    print("clustersOfItemIdsDict: " + str(clustersOfItemIdsDict))
    print("clustersOfScoreDict: " + str(clustersOfScoreDict))
    showRouteMaps(clustersOfItemIdsDict.values(), itemsDF)


if __name__ == "__main__":
    os.chdir('../../../')
    print("")
    #test01()
    test02()
