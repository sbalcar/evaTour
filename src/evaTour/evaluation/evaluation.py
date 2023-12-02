import os
from decimal import Decimal
from typing import List

from pandas import Series
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import readDatasetNYC, readDatasetTKY, divideTrainTest
from evaTour.datasets.usersSimilarity import readSimilarityDFNYC, readSimilarityDFTKY
from evaTour.ea.toolDiversity import countAVGMinHammingDistanceFromIndiv, countAVGIntersectionsWithIndiv
from evaTour.ea.operators.roundtrip.fitness.fitnessKmTSPSolver import FitnessKmTSPSolver
from evaTour.recommenders.recommenderBirchTSPSolver import RecommenderBirchTSPSolver
from evaTour.recommenders.recommenderSVDS import RecommenderSVDS
from evaTour.recommenders.recommenderTSPEvolution import getRecTSPEvolution, RecommenderTSPEvolution
from evaTour.recommenders.recommenderTSPIslandModel import getRecTSPIslandModel, RecommenderTSPIslandModel
from evaTour.webServer.datamodels.TeamsModel import TeamsModel
from evaTour.webServer.datamodels.UsersModel import UsersModel

import numpy as np

class Evaluation:

    def __init__(self):
        self.ratingsNYcDF, self.itemsNYcDF, self.distancesNYcDF = readDatasetNYC()
        self.ratingsTkyDF, self.itemsTkyDF, self.distancesTkyDF = readDatasetTKY()
        self.ratingsTrainNYcDF, self.ratingsTestNYcDF = divideTrainTest(self.ratingsNYcDF, 50)
        self.ratingsTrainTkyDF, self.ratingsTestTkyDF = divideTrainTest(self.ratingsTkyDF, 50)

        self.similarityDFNYC = readSimilarityDFNYC()
        self.similarityDFTKY = readSimilarityDFTKY()

        self.usersModel = UsersModel.readModel()
        self.teamsModel = TeamsModel.readModel()


    def __getNumberOfIndiv(self, recommender):
        if isinstance(recommender, RecommenderSVDS):
            return 1
        if isinstance(recommender, RecommenderTSPEvolution):
            return recommender._ea._popSize
        if isinstance(recommender, RecommenderTSPIslandModel):
            return recommender._im._popSize * len(recommender._im._islands)

    def __getAVGMinHammingDistanceFromTheBestIndiv(self, recommender):
        if isinstance(recommender, RecommenderSVDS):
            return 1
        if isinstance(recommender, RecommenderTSPEvolution):
            populationOfIndiv = recommender._ea.lastPopulation
            indiv = recommender._ea.bestOfAllIndiv
            return countAVGMinHammingDistanceFromIndiv(populationOfIndiv, indiv, DEBUG=False)
        if isinstance(recommender, RecommenderTSPIslandModel):
            #return recommender._im._popSize * len(recommender._im._islands)
            return -1

    def __getAVGIntersectionSizeOfPopFromTheBestIndiv(self, recommender):
        if isinstance(recommender, RecommenderSVDS):
            return 1
        if isinstance(recommender, RecommenderTSPEvolution):
            populationOfIndiv = recommender._ea.lastPopulation
            indiv = recommender._ea.bestOfAllIndiv
            return countAVGIntersectionsWithIndiv(populationOfIndiv, indiv, DEBUG=False)
        if isinstance(recommender, RecommenderTSPIslandModel):
            #populationOfIndiv, _ = recommender._im.getDistributedPopulation()
            return -1


    def evalRoundtrip(self, recommenders:List, recomLabels:List[str], lengthOfRounftrip:int):
        DEBUG = 1

        # recommenders training
        for recomLabelI, recommenderI in zip(recomLabels, recommenders):
            print("Training " + str(recomLabelI) + " started")
            recommenderI.train(self.ratingsTrainNYcDF, self.itemsNYcDF, self.distancesNYcDF)
            print("Training " + str(recomLabelI) + " finished")
            print("")

        numberOfItemHitsInTestSetCounterDict = {}
        kmCounterDict = {}
        jaccardDistanceCounterDict = {}
        numberOfIndividualsCounterDict = {}
        AVGMinHammingDistanceOfPopFromTheBestIndivCounterDict = {}
        AVGIntersectionSizeOfPopFromTheBestIndivCounterDict = {}
        #diversityOfIndividualsCounterDict = {}
        # counter preprocessing
        for recomLabelI in recomLabels:
            numberOfItemHitsInTestSetCounterDict[recomLabelI] = 0
            kmCounterDict[recomLabelI] = 0
            jaccardDistanceCounterDict[recomLabelI] = 0
            AVGMinHammingDistanceOfPopFromTheBestIndivCounterDict[recomLabelI] = 0
            AVGIntersectionSizeOfPopFromTheBestIndivCounterDict[recomLabelI] = 0

        # loop over all users
        userIds:List = list(set(self.ratingsNYcDF['UserID'].values))
        userIds = userIds[:30]  # TODO
        for userIdI in userIds:
            if DEBUG:
                print("userIdI: " + str(userIdI))

            windowOfItemsIds:List = self.ratingsTestNYcDF[self.ratingsTestNYcDF['UserID'] == userIdI]["VenueID"].values.tolist()
            if DEBUG:
                print("windowOfItemsIds: " + str(windowOfItemsIds))

            for recomLabelI, recommenderI in zip(recomLabels, recommenders):
                recI:Series = recommenderI.recommend(userIdI, lengthOfRounftrip)
                recommOfItemsIdsI:List = recI.index.tolist()
                if DEBUG:
                    print(recomLabelI + " recommOfItemsIdsI: " + str(recommOfItemsIdsI))

                intersectionI:List = list(set(recommOfItemsIdsI) & set(windowOfItemsIds))
                numberOfItemHitsInTestSetCounterDict[recomLabelI] += len(intersectionI)

                kmI = FitnessKmTSPSolver(self.itemsNYcDF, self.distancesNYcDF).run(recommOfItemsIdsI)
                kmCounterDict[recomLabelI] += kmI

                jaccardDistanceI = len(intersectionI) / len(set(recommOfItemsIdsI).union(set(windowOfItemsIds)))
                jaccardDistanceCounterDict[recomLabelI] += jaccardDistanceI

                AVGMinHammingDistanceOfPopFromTheBestIndivCounterDict[recomLabelI] += self.__getAVGMinHammingDistanceFromTheBestIndiv(recommenderI)

                AVGIntersectionSizeOfPopFromTheBestIndivCounterDict[recomLabelI] += self.__getAVGIntersectionSizeOfPopFromTheBestIndiv(recommenderI)

        # counter postprocessing
        for kI, vI in jaccardDistanceCounterDict.items():
            jaccardDistanceCounterDict[kI] = vI / len(userIds)
        for kI, vI in AVGMinHammingDistanceOfPopFromTheBestIndivCounterDict.items():
            AVGMinHammingDistanceOfPopFromTheBestIndivCounterDict[kI] = vI / len(userIds)
        for kI, vI in AVGIntersectionSizeOfPopFromTheBestIndivCounterDict.items():
            AVGIntersectionSizeOfPopFromTheBestIndivCounterDict[kI] = vI / len(userIds)
        for recomLabelI, recommenderI in zip(recomLabels, recommenders):
            numberOfIndividualsCounterDict[recomLabelI] = self.__getNumberOfIndiv(recommenderI)

        print("")
        print("numberOfItemHitsInTestSetCounterDict: " + str(numberOfItemHitsInTestSetCounterDict))
        print("kmCounterDict: " + str(kmCounterDict))
        print("jaccardDistanceCounterDict: " + str(jaccardDistanceCounterDict))
        print("numberOfIndividualsCounterDict: " + str(numberOfIndividualsCounterDict))
        print("AVGMinHammingDistanceOfPopFromTheBestIndivCounterDict: " + str(AVGMinHammingDistanceOfPopFromTheBestIndivCounterDict))
        print("AVGIntersectionSizeOfPopFromTheBestIndivCounterDict: " + str(AVGIntersectionSizeOfPopFromTheBestIndivCounterDict))


        #numberOfItemHitsInTestSet: {'RecommenderSVDS': 50, 'RecTSPEvolution': 50, 'RecTSPIslandModel': 50}
        #kmCounterDict: {'RecommenderSVDS': 141609.4287249171, 'RecTSPEvolution': 68001.97991946219, 'RecTSPIslandModel': 54234.47305305238}

# editacni vzdalenost   `````



    def evalClusters(self, recommenders:List, recomLabels:List[str], lengthOfRounftrip:int):
        DEBUG = False

        # recommenders training
        for recomLabelI, recommenderI in zip(recomLabels, recommenders):
            print("Training " + str(recomLabelI) + " started")
            recommenderI.train(self.ratingsTrainNYcDF, self.itemsNYcDF, self.distancesNYcDF)
            print("Training " + str(recomLabelI) + " finished")
            print("")

        self.numberOfItemHitsInTestSetCounterDict = {}
        self.kmCounterDict = {}
        self.jaccardDistanceCounterDict = {}
        self.numberOfIndividualsCounterDict = {}
        self.AVGMinHammingDistanceOfPopFromTheBestIndivCounterDict = {}
        self.AVGIntersectionSizeOfPopFromTheBestIndivCounterDict = {}
        #diversityOfIndividualsCounterDict = {}
        # counter preprocessing
        for recomLabelI in recomLabels:
            self.numberOfItemHitsInTestSetCounterDict[recomLabelI] = 0
            self.kmCounterDict[recomLabelI] = 0
            self.jaccardDistanceCounterDict[recomLabelI] = 0
            self.AVGMinHammingDistanceOfPopFromTheBestIndivCounterDict[recomLabelI] = 0
            self.AVGIntersectionSizeOfPopFromTheBestIndivCounterDict[recomLabelI] = 0


        # loop over all users
        userIds:List = list(set(self.ratingsNYcDF['UserID'].values))
        userIds = userIds[:30]  # TODO
        for userIdI in userIds:
            print("userIdI: " + str(userIdI))

            windowOfItemsIds:List = self.ratingsTestNYcDF[self.ratingsTestNYcDF['UserID'] == userIdI]["VenueID"].values.tolist()
            print("windowOfItemsIds: " + str(windowOfItemsIds))

            for recomLabelI, recommenderI in zip(recomLabels, recommenders):
                recI:dict[Series] = recommenderI.recommendClusters(userIdI)
                if DEBUG:
                    print(recomLabelI + " recI: " + str(recI))

                clusterIdsI:List = recI.keys()
                scoreI:List = recI.values()

                self.userClusterSizeDict:dict = dict([(recomLabelI, {}) for recomLabelI in recomLabels])
                self.userKmLenDict:dict = dict([(recomLabelI, {}) for recomLabelI in recomLabels])
                self.userScoreDict:dict = dict([(recomLabelI, {}) for recomLabelI in recomLabels])
                self.userScoreAVGDict:dict = dict([(recomLabelI, {}) for recomLabelI in recomLabels])

                for clusterIdI in clusterIdsI:
                    recommClusterOfItemsIdsI = recI[clusterIdI]
                    self._evalClusters(recommClusterOfItemsIdsI, clusterIdI, recomLabelI, recommenderI, windowOfItemsIds)
                np.set_printoptions(suppress=True)

                print("userclusterSizeDict: " + str(self.userClusterSizeDict))
                print("userKmLenDict:       " + str(self.userKmLenDict))
                print("userScoreDict:       " + str(self.userScoreDict))
                print("userScoreAVGDict:    " + str(self.userScoreAVGDict))

        # counter postprocessing
        for kI, vI in self.jaccardDistanceCounterDict.items():
            self.jaccardDistanceCounterDict[kI] = vI / len(userIds)
        for kI, vI in self.AVGMinHammingDistanceOfPopFromTheBestIndivCounterDict.items():
            self.AVGMinHammingDistanceOfPopFromTheBestIndivCounterDict[kI] = vI / len(userIds)
        for kI, vI in self.AVGIntersectionSizeOfPopFromTheBestIndivCounterDict.items():
            self.AVGIntersectionSizeOfPopFromTheBestIndivCounterDict[kI] = vI / len(userIds)
        for recomLabelI, recommenderI in zip(recomLabels, recommenders):
            self.numberOfIndividualsCounterDict[recomLabelI] = self.__getNumberOfIndiv(recommenderI)


        print("")
        print("numberOfItemHitsInTestSetCounterDict: " + str(self.numberOfItemHitsInTestSetCounterDict))
        print("kmCounterDict: " + str(self.kmCounterDict))
        print("jaccardDistanceCounterDict: " + str(self.jaccardDistanceCounterDict))
        print("numberOfIndividualsCounterDict: " + str(self.numberOfIndividualsCounterDict))
        print("AVGMinHammingDistanceOfPopFromTheBestIndivCounterDict: " + str(self.AVGMinHammingDistanceOfPopFromTheBestIndivCounterDict))
        print("AVGIntersectionSizeOfPopFromTheBestIndivCounterDict: " + str(self.AVGIntersectionSizeOfPopFromTheBestIndivCounterDict))

        print("")


    def _evalClusters(self, recommOfItemsIdsSerI:Series, clusterIdI, recomLabelI, recommenderI, windowOfItemsIds):
        recommOfItemsIdsI = list(recommOfItemsIdsSerI.keys())
        scoreI = list(recommOfItemsIdsSerI.values)

        intersectionI: List = list(set(recommOfItemsIdsI) & set(windowOfItemsIds))
        self.numberOfItemHitsInTestSetCounterDict[recomLabelI] += len(intersectionI)

        kmI = fitnessKmPrecalculatedTSPFnc(recommOfItemsIdsI, self.itemsNYcDF, self.distancesNYcDF)
        self.kmCounterDict[recomLabelI] += kmI

        jaccardDistanceI = len(intersectionI) / len(set(recommOfItemsIdsI).union(set(windowOfItemsIds)))
        self.jaccardDistanceCounterDict[recomLabelI] += jaccardDistanceI

        #a = self.__getAVGMinHammingDistanceFromTheBestIndiv(recommenderI)
        #self.AVGMinHammingDistanceOfPopFromTheBestIndivCounterDict[recomLabelI] += a

        #self.AVGIntersectionSizeOfPopFromTheBestIndivCounterDict[
        #    recomLabelI] += self.__getAVGIntersectionSizeOfPopFromTheBestIndiv(recommenderI)

        self.userClusterSizeDict[recomLabelI][clusterIdI] = FancyFloat(len(recommOfItemsIdsSerI))
        self.userKmLenDict[recomLabelI][clusterIdI] = FancyFloat(kmI)
        self.userScoreDict[recomLabelI][clusterIdI] = FancyFloat(sum(scoreI))
        self.userScoreAVGDict[recomLabelI][clusterIdI] = FancyFloat(sum(scoreI)/len(recommOfItemsIdsSerI))


class FancyFloat(float):
    def __repr__(self):
        return format(Decimal(self), ".8f")

def test1():
    print("test1")

    e = Evaluation()

    LENGTH_OF_ROUNDTRIP:int = 15

    recomLabels = ["RecommenderSVDS", "RecTSPEvolution", "RecTSPIslandModel"]
    recommenders = [RecommenderSVDS({RecommenderSVDS.ARG_K: 8}),
                    getRecTSPEvolution(e.ratingsTrainNYcDF, e.itemsNYcDF, e.distancesNYcDF),
                    getRecTSPIslandModel(e.ratingsTrainNYcDF, e.itemsNYcDF, e.distancesNYcDF)]
    e.evalRoundtrip(recommenders, recomLabels, LENGTH_OF_ROUNDTRIP)


def test2():
    print("test2")

    DEBUG = False
    LENGTH_OF_ROUNDTRIP = 15

    argsBirchTSPSolverDict = {RecommenderBirchTSPSolver.ARG_RECOMMENDER_CLASS:RecommenderSVDS,
                RecommenderBirchTSPSolver.ARG_RECOMMENDER_ARGS:{RecommenderSVDS.ARG_K:8},
                RecommenderBirchTSPSolver.ARG_RECOMMENDATION_POOL_SIZE:100,
                RecommenderBirchTSPSolver.ARG_CLUSTER_COUNT:10,
                RecommenderBirchTSPSolver.ARG_PYTHON_TSP_HEURISTIC_FNC:solve_tsp_local_search}
    rBirchTSPSolver = RecommenderBirchTSPSolver(argsBirchTSPSolverDict, DEBUG)


    recomLabels = ["RecBirchTSPSolver"]
    recommenders = [rBirchTSPSolver]

    e = Evaluation()
    e.evalClusters(recommenders, recomLabels, LENGTH_OF_ROUNDTRIP)


if __name__ == '__main__':
    os.chdir('../')
    os.chdir('../')
    os.chdir('../')

    #test1()
    test2()