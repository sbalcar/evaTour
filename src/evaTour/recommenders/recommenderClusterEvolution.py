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

from evaTour.datasets.datasetFoursquare import getNearestNeighbors
from evaTour.ea.individuals.individualClusters import IndividualClusters
from evaTour.ea.operators.clusters.generator.generatorCluImproveSolution import GeneratorCluImproveSolution
from evaTour.maps.openStreetMaps import convertIndividualToGPS


class RecommenderClusterEvolution:
    _ratingsDF:DataFrame = None
    _itemsDF:DataFrame = None
    _distancesDF:DataFrame = None

    ARG_RECOMMENDER_CLASS:str = "recommenderClass"
    ARG_RECOMMENDER_ARGS:str = "recommenderArgs"
    ARG_RECOMMENDER_EA:str = "recommenderEA"

    ARG_NEAREST_NEIGHBORS_COUNT:str = "nearestNeighborsCount"

    ARG_RECOMMENDATION_POOL_SIZE:str = "recommenderPoolSize"
    ARG_BIRCH_CLUSTER_COUNT:str = "birchCusteerCount"
    ARG_BIRCH_CLUSTER_THRESHOLD:str = "birchCusteerThreshold"

    DEBUG = None

    def __init__(self, args:dict, DEBUG:bool=False):
        self._args = args
        self._DEBUG = DEBUG

        recommenderClass = args[self.ARG_RECOMMENDER_CLASS]
        recommenderArgs = args[self.ARG_RECOMMENDER_ARGS]
        self.recommender = recommenderClass(recommenderArgs, DEBUG)

        self.ea = args[self.ARG_RECOMMENDER_EA]

        self.nearestNeighborsCount = args[self.ARG_NEAREST_NEIGHBORS_COUNT]

        self.recommenderPoolSize:int = args[self.ARG_RECOMMENDATION_POOL_SIZE]
        self.birchClusterThreshold:int = args[self.ARG_BIRCH_CLUSTER_THRESHOLD]
        self.birchClusterCount:int = args[self.ARG_BIRCH_CLUSTER_COUNT]


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
            print("Training RecommenderClusterEvolution started")
        self.recommender.train(ratingsDF, itemsDF, distancesDF)
        if self._DEBUG:
            print("Training RecommenderClusterEvolution finished")

        self.nearestNeighborsOfItemIdsDict:dict = getNearestNeighbors(distancesDF, self.nearestNeighborsCount)


    def recommendClusters(self, userID:int):

        clustersOfItemIdsSerDict:dict[Series] = self.recommender.recommendClusters(userID)
        rItemIdsPool:List = self.recommender.rItemIdsPool
        rItemIdsPoolScore:List = self.recommender.rItemIdsPoolScore

        clustersOfItemIdsDict:dict[List] = {clusterIdI:clusterOfSeriesI.keys() for clusterIdI, clusterOfSeriesI in clustersOfItemIdsSerDict.items()}
        indivBase:IndividualClusters = IndividualClusters(clustersOfItemIdsDict).exportUnraveledPermutation(self._distancesDF)

        #print("indivBase.clustersOfItemIdsDict: " + str(indivBase.clustersOfItemIdsDict))
        clustersOfScoresDict:dict = {}
        for clusterIdI, clusterItemIdsI in indivBase.clustersOfItemIdsDict.items():
            scoresOfClusterI:List[float] = [clustersOfItemIdsSerDict[clusterIdI][itemIdI] for itemIdI in clusterItemIdsI]
            clustersOfScoresDict[clusterIdI] = scoresOfClusterI

        oprGenerator = self.ea._popGeneratorOpr
        oprGenerator.setIndividualBase(indivBase)
        oprGenerator.individualScoreDict = clustersOfScoresDict
        oprGenerator.rItemIdsPoolScoreDict = dict(zip(rItemIdsPool, rItemIdsPoolScore))
        if isinstance(oprGenerator, GeneratorCluImproveSolution):
            oprGenerator.nearestNeighborsOfItemIdsDict = self.nearestNeighborsOfItemIdsDict

        oprFitness = self.ea._fitnessOpr
        oprFitness.rItemIdsPoolScoreDict = dict(zip(rItemIdsPool, rItemIdsPoolScore))


        bestOfAllIndiv, bestOfAllFitnessValue = self.ea.run(self.DEBUG)

        unraveledIndiv:IndividualClusters = bestOfAllIndiv.exportUnraveledPermutation(self._distancesDF)

        clustersOfScoreDict:dict = {}
        for clusterIdI, itemIdsI in unraveledIndiv.clustersOfItemIdsDict.items():
            scoresI = [dict(zip(rItemIdsPool, rItemIdsPoolScore)).get(itemIdI,0) for itemIdI in itemIdsI]
            clustersOfScoreDict[clusterIdI] = scoresI

        return bestOfAllIndiv, clustersOfScoreDict


    def recommendClusters_(self, userID:int):

        recommendationPoolSer:Series = self.recommender.recommend(userID, k=self.recommenderPoolSize)
        rItemIDsPool, rScoresPool = list(recommendationPoolSer.keys()), list(recommendationPoolSer.values)
        if self._DEBUG:
            print("rItemIDsPool: " + str(rItemIDsPool))
            print("rScoresPool: " + str(rScoresPool))

        gpsCoordsListOfTuple = convertIndividualToGPS(rItemIDsPool, self._itemsDF)
        gpsCoords = np.array(gpsCoordsListOfTuple)
        # print("gpsCoords: " + str(gpsCoords))

        # define the model
        #model = Birch(threshold=0.00001, branching_factor=2, n_clusters=None)
        model = Birch(threshold=self.birchClusterThreshold, n_clusters=self.birchClusterCount)
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
            itemIdsI = [rItemIDsPool[itemIdsIndexI] for itemIdsIndexI in itemIdsIndexesI]
            # print("itemIdsI: " + str(itemIdsI))
            clustersOfItemIdsDict[clusterIdI] = list(itemIdsI)

        indivBase:IndividualClusters = IndividualClusters(clustersOfItemIdsDict)
        #return indivBase

        clustersOfScoresDict:dict = {}
        for clusterIdI, clusterItemIdsI in indivBase.clustersOfItemIdsDict.items():
            scoresOfClusterI:List[float] = [recommendationPoolSer[ItemIdI] for ItemIdI in clusterItemIdsI]
            clustersOfScoresDict[clusterIdI] = scoresOfClusterI

        oprGenerator = self.ea._popGeneratorOpr
        oprGenerator.setIndividualBase(indivBase)
        oprGenerator.individualScoreDict = clustersOfScoresDict
        oprGenerator.rItemIdsPool:List[int] = rItemIDsPool
        oprGenerator.rItemIdsPoolScore:List[float] = rScoresPool

        oprFitness = self.ea._fitnessOpr
        oprFitness.rItemIdsPoolScoreDict = recommendationPoolSer


        bestOfAllIndiv, bestOfAllFitnessValue = self.ea.run(self.DEBUG)

        unraveledIndiv:IndividualClusters = bestOfAllIndiv.exportUnraveledPermutation(self._distancesDF)

        clustersOfScoreDict:dict = {}
        for clusterIdI, itemIdsI in unraveledIndiv.clustersOfItemIdsDict.items():
            scoresI = [recommendationPoolSer[itemIdI] for itemIdI in itemIdsI]
            clustersOfScoreDict[clusterIdI] = scoresI

        return bestOfAllIndiv, clustersOfScoreDict
