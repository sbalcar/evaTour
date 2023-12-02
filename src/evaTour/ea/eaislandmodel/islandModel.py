# genetic algorithm search of the one max optimization problem

from typing import List
from typing import Dict

from pandas.core.frame import DataFrame  # class

from multiprocessing import Process

from evaTour.ea.toolDiversity import countMatrixOfIntersections
from evaTour.ea.easimple.ea import EvolutionAlgorithm
from evaTour.ea.eaislandmodel.islandEATabu import IslandEATabu

import multiprocessing

def runIsland(insland:EvolutionAlgorithm, inslandID:int, bestIndivDict:Dict, bestFitnessDict:Dict):

    bestIndiv, bestFitness = insland.run()

    bestIndivDict[inslandID] = bestIndiv
    bestFitnessDict[inslandID] = bestFitness


class IslandModel:
    ARG_MIGRATION_PERIOD:str = "migrationPeriod"
    ARG_SHARED_DATA_STRUCTURE:str = "sharedDataStructure"

    _islands:List = []

    # default constructor
    def __init__(self, islands:List):
        self._islands = islands

    def setMigrationFnc(self, migrationFnc: object, migrationFncArgs: List) -> object:
        self._migrationFnc = migrationFnc
        self._migrationFncArgs = migrationFncArgs


    def setIterCount(self, iterCount:int):
        self._iterCount: int = iterCount
    def setPopSize(self, popSize:int):
        self._popSize: int = popSize
    def setCrossRate(self, crossRate:float):
        self._crossRate: float = crossRate
    def setMutRate(self, mutRate:float):
        self._mutRate:float = mutRate

    #############################################################################

    def getDistributedPopulation(self):
        distPop = []
        distFitness = []
        for islandI in self._islands:
            popI:List = islandI.lastPopulation
            fitnessI:List[float] = islandI.lastPopFitness
            distPop.append(popI)
            distFitness.append(fitnessI)
        return (distPop, distFitness)

    def train(self, ratingsDF:DataFrame, itemsDF:DataFrame, distancesDF:DataFrame, DEBUG=False):

        #self._recommender.train(ratingsDF, itemsDF, distancesDF)

        for islandI in self._islands:
            islandI.train(ratingsDF, itemsDF, distancesDF, DEBUG)

    def run(self, DEBUG=False):

        manager = multiprocessing.Manager()

        bestIndivDict:Dict = manager.dict()
        bestFitnessDict:Dict = manager.dict()

        sharedTabuDict:Dict = manager.dict()

        threads:List = []
        for inslandIdI in range(len(self._islands)):
            inslandI:IslandEATabu = self._islands[inslandIdI]
            inslandI.setMigrationFnc(self._migrationFnc, self._migrationFncArgs)
            inslandI.setSharedDataStructure(sharedTabuDict, {})
            inslandI.setIterCount(self._iterCount)
            inslandI.setPopSize(self._popSize)
            inslandI.setCrossRate(self._crossRate)
            inslandI.setMutRate(self._mutRate)

            #bestIndiv, bestFitness = inslandI.run()
            ####################threadI = threading.Thread(target=inslandI.run, args=())
            threadI = Process(target=runIsland, args=(inslandI, inslandIdI, bestIndivDict, bestFitnessDict))
            threads.append(threadI)
            threadI.start()

        for threadI in threads:
            threadI.join()

        self.resultBestIndivDict = bestIndivDict
        self.resultBestFitnessDict = bestFitnessDict

        print("")
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print("bestIndivDict: " + str(bestIndivDict))
        print("bestFitnessDict: " + str(bestFitnessDict))
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")

        print("")
        print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
        matrix:List[List] = countMatrixOfIntersections(sharedTabuDict)
        for rI in matrix:
            print(rI)
        print("bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb")
        print("")


    def getTheBestIndividual(self):
        if self.resultBestFitnessDict == None or len(self.resultBestFitnessDict) == 0:
            return None

        fitnessValues:List[float] = self.resultBestFitnessDict.values()
        index:int = fitnessValues.index(min(fitnessValues))

        return self.resultBestIndivDict.values()[index]
