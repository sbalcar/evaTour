# genetic algorithm search of the one max optimization problem

import sys
from typing import List
from typing import Dict

from pandas.core.frame import DataFrame  # class
from pandas.core.series import Series  # class


class IslandEATabu:
    _id = None
    _popGeneratorFnc = None
    _popGeneratorFncArgs = None
    _fitnessFnc = None
    _fitnessFncArgs = None
    _selectionFnc = None
    _selectionFncArgs = None
    _crossoverFnc = None
    _crossoverFncArgs = None
    _mutationFnc = None
    _mutationFncArgs = None
    _migrationFnc = None
    _migrationFncArgs = None
    _sharedDataStructure = None
    _sharedDataStructureArgs = None

    ARG_MIGRATION_GEN_PERIOD:str = "MigrationGenPeriod"

    def __init__(self, id=0):
        self._id = id

    def setPopGeneratorFnc(self, popGeneratorFnc, popGeneratorFncArgs:Dict):
        self._popGeneratorFnc = popGeneratorFnc
        self._popGeneratorFncArgs = popGeneratorFncArgs

    def setFitnessFnc(self, fitnessFnc, fitnessFncArgs:Dict):
        self._fitnessFnc = fitnessFnc
        self._fitnessFncArgs = fitnessFncArgs

    def setSelectionFnc(self, selectionFnc, selectionFncArgs:Dict):
        self._selectionFnc = selectionFnc
        self._selectionFncArgs = selectionFncArgs

    def setCrossoverFnc(self, crossoverFnc, crossoverFncArgs:Dict):
        self._crossoverFnc = crossoverFnc
        self._crossoverFncArgs = crossoverFncArgs

    def setMutationFnc(self, mutationFnc, mutationFncArgs:Dict):
        self._mutationFnc = mutationFnc
        self._mutationFncArgs = mutationFncArgs

    def setMigrationFnc(self, migrationFnc, migrationFncArgs:Dict):
        self._migrationFnc = migrationFnc
        self._migrationFncArgs = migrationFncArgs

    def setSharedDataStructure(self, sharedDataStructure, sharedDataStructureArgs:Dict):
        self._sharedDataStructure = sharedDataStructure
        self._sharedDataStructureArgs = sharedDataStructureArgs

    def setIterCount(self, iterCount:int):
        self._iterCount: int = iterCount
    def setPopSize(self, popSize:int):
        self._popSize: int = popSize
    def setCrossRate(self, crossRate:float):
        self._crossRate: float = crossRate
    def setMutRate(self, mutRate:float):
        self._mutRate:float = mutRate

    #############################################################################

    def train(self, ratingsDF:DataFrame, itemsDF:DataFrame, distancesDF:DataFrame, DEBUG=False):
        print("")

    # genetic algorithm
    def run(self):
        print("RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR")
        if self._iterCount == None:
            raise Exception("Value iterCount is not initialised.")
        if self._popSize == None:
            raise Exception("Value popSize is not initialised.")
        if self._crossRate == None:
            raise Exception("Value crossRate is not initialised.")
        if self._mutRate == None:
            raise Exception("Value mutRate is not initialised.")

        # initial population of random bitstring
        pop:List = self._popGeneratorFnc(self._popSize, *self._popGeneratorFncArgs)
        # keep track of best solution
        bestIndivIJ, bestFitnessIJ = pop[0], self._fitnessFnc(pop[0], *self._fitnessFncArgs)
        # enumerate generations
        for genI in range(self._iterCount):
            print("Generation: %s" % genI)

            if genI % self._migrationFncArgs.get(
                    IslandEATabu.ARG_MIGRATION_GEN_PERIOD) == 0:
                print("Mutation")
                self._migrationFnc(self._id, genI, self._sharedDataStructure, bestIndivIJ)

            # evaluate all candidates in the population
            fitnessValuesI = [self._fitnessFnc(cI, *self._fitnessFncArgs) for cI in pop]
            # check for new best solution
            for indexJ in range(self._popSize):
                if fitnessValuesI[indexJ] < bestFitnessIJ:
                    bestIndivIJ, bestFitnessIJ = pop[indexJ], fitnessValuesI[indexJ]
            print("Best individual f(%s) = %.3f" % (bestIndivIJ, bestFitnessIJ))
            # select parents
            selectedI = self._selectionFnc(pop, fitnessValuesI, len(pop), *self._selectionFncArgs)
            # create the next generation
            childrenI = list()
            for indexJ in range(0, self._popSize, 2):
                # get selected parents in pairs
                p1, p2 = selectedI[indexJ], selectedI[indexJ + 1]
                # crossover and mutation
                ch1, ch2 = self._crossoverFnc(list(p1), list(p2), self._crossRate, *self._crossoverFncArgs)
                # mutation
                chNew1 = self._mutationFnc(ch1, self._mutRate, *self._mutationFncArgs)
                chNew2 = self._mutationFnc(ch2, self._mutRate, *self._mutationFncArgs)
                # store for next generation
                childrenI.append(chNew1)
                childrenI.append(chNew2)
            # replace population
            #print(childrenI)
            pop = childrenI

            for indivI in pop:
                if len(set(indivI)) != len(indivI):
                    raise Exception("Not the right length of individual")

        self.lastPopulation:List = pop
        self.lastPopFitness:List[float] = [self._fitnessFnc(indivI, *self._fitnessFncArgs) for indivI in pop]

        bestOfAllIndiv = None
        bestOfAllFitnessValue = sys.maxsize
        for indivI, fitnessI in zip(self.lastPopulation, self.lastPopFitness):
            if fitnessI < bestOfAllFitnessValue:
                bestOfAllIndiv = indivI
                bestOfAllFitnessValue = fitnessI

        return (bestOfAllIndiv, bestOfAllFitnessValue)


    def getPopAndFitnessValues(self, indivCount:int):
        sortedPopFitness, sortedPopulation = zip(*sorted(zip(self.lastPopFitness, self.lastPopulation)))
        return (list(sortedPopulation)[:indivCount], list(sortedPopFitness)[:indivCount])
