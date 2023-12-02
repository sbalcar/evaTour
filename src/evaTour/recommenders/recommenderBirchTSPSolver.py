from numpy import sort
from typing import List

from pandas.core.frame import DataFrame  # class
from pandas.core.series import Series  # class
from python_tsp.heuristics import solve_tsp_local_search

from scipy.sparse.linalg import svds
import numpy as np

# birch clustering
from numpy import unique
from numpy import where
from sklearn.datasets import make_classification
from sklearn.cluster import Birch
from matplotlib import pyplot

from evaTour.ea.individuals.individualClusters import IndividualClusters
from evaTour.maps.openStreetMaps import convertIndividualToGPS


class RecommenderBirchTSPSolver:
    _ratingsDF:DataFrame = None
    _itemsDF:DataFrame = None
    _distancesDF:DataFrame = None

    ARG_RECOMMENDER_CLASS = "recommenderClass"
    ARG_RECOMMENDER_ARGS = "recommenderArgs"
    ARG_RECOMMENDATION_POOL_SIZE = "recommendatonPoolSize"
    ARG_CLUSTER_COUNT = "clusterCount"
    ARG_CLUSTER_THRESHOLD = "clusterThreshold"
    ARG_PYTHON_TSP_HEURISTIC_FNC =  "pythonTspHeuristicsFnc"
    DEBUG = None

    def __init__(self, args:dict, DEBUG=False):
        self._args = args
        self._DEBUG = DEBUG

        recommenderClass = args[self.ARG_RECOMMENDER_CLASS]
        recommenderArgs = args[self.ARG_RECOMMENDER_ARGS]
        self.recommender = recommenderClass(recommenderArgs, DEBUG)

        self.recommendatonPoolSize = self._args[self.ARG_RECOMMENDATION_POOL_SIZE]

        self.pythonTspHeuristicsFnc = self._args[self.ARG_PYTHON_TSP_HEURISTIC_FNC]
        self.clusterCount = self._args[self.ARG_CLUSTER_COUNT]
        self.clusterThreshold = self._args[self.ARG_CLUSTER_THRESHOLD]

    def train(self, ratingsDF, itemsDF, distancesDF):
        if not isinstance(ratingsDF, DataFrame):
            raise Exception("Argument ratingsDF is not DataFrame: " + str(ratingsDF))
        if not isinstance(itemsDF, DataFrame):
            raise Exception("Argument itemsDF is not DataFrame: " + str(itemsDF))
        if not isinstance(distancesDF, DataFrame):
            raise Exception("Argument distancesDF is not DataFrame: " + str(distancesDF))

        self._ratingsDF = ratingsDF
        self._itemsDF = itemsDF
        self._distancesDF = distancesDF

        if self._DEBUG:
            print(self._ratingsDF.head(10))

        if self._DEBUG:
            print("Training started")
        self.recommender.train(ratingsDF, itemsDF, distancesDF)
        if self._DEBUG:
            print("Training finished")

    def recommend(self, userID, k=20):
        recommendation:Series = self.recommender.recommend(userID, k)
        return recommendation

    def recommendClusters(self, userID:int):
        recommendationPool:Series = self.recommender.recommend(userID, self.recommendatonPoolSize)
        self.rItemIdsPool, self.rItemIdsPoolScore = list(recommendationPool.keys()), list(recommendationPool.values)

        if self._DEBUG:
            print("rItemIdsPool: " + str(self.rItemIdsPool))
            print("rItemIdsPoolScore: " + str(self.rItemIdsPoolScore))

        gpsCoordsListOfTuple = convertIndividualToGPS(self.rItemIdsPool, self._itemsDF)
        gpsCoords = np.array(gpsCoordsListOfTuple)
        # print("gpsCoords: " + str(gpsCoords))

        # define the model
        model = Birch(threshold=self.clusterThreshold, n_clusters=self.clusterCount)
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
            itemIdsI = [self.rItemIdsPool[itemIdsIndexI] for itemIdsIndexI in itemIdsIndexesI]
            # print("itemIdsI: " + str(itemIdsI))
            clustersOfItemIdsDict[clusterIdI] = list(itemIdsI)

        for clusterIdI in clustersOfItemIdsDict.keys():
            itemIdsI = clustersOfItemIdsDict[clusterIdI]
            # select rows and columns with index positions
            distancesSelDF = self._distancesDF.iloc[itemIdsI, itemIdsI]
            distance_matrix = distancesSelDF.to_numpy()

            permutationOfIndexes, distance = self.pythonTspHeuristicsFnc(distance_matrix)

            # use numpy.take() to retrieve elements
            # from input list at given indices
            permutation = np.take(itemIdsI, permutationOfIndexes)
            scores = [recommendationPool[itemIdI] for itemIdI in permutation]
            clustersOfItemIdsDict[clusterIdI] = Series(scores, index=permutation)

        #print(clustersOfItemIdsDict)
        return clustersOfItemIdsDict