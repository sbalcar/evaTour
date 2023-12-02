# genetic algorithm search of the one max optimization problem

import sys
from typing import List

from evaTour.maps.openStreetMaps import showRouteMaps


class EvolutionAlgorithm:

    _popGeneratorOpr = None
    _fitnessOpr = None
    _selectionOpr = None
    _crossoverOpr = None

    _iterCount:int = None
    _popSize:int = None
    _crossRate:float = None
    _mutRate:float = None


    def setPopGeneratorOpr(self, popGeneratorOpr):
        self._popGeneratorOpr = popGeneratorOpr

    def setFitnessOpr(self, fitnessOpr):
        self._fitnessOpr = fitnessOpr

    def setSelectionOpr(self, selectionOpr):
        self._selectionOpr = selectionOpr

    def setCrossoverOpr(self, crossoverOpr):
        self._crossoverOpr = crossoverOpr

    def setMutationOpr(self, mutationOpr):
        self._mutationOpr = mutationOpr


    def setIterCount(self, iterCount:int):
        self._iterCount: int = iterCount
    def setPopSize(self, popSize:int):
        self._popSize: int = popSize
    def setCrossRate(self, crossRate:float):
        self._crossRate: float = crossRate
    def setMutRate(self, mutRate:float):
        self._mutRate:float = mutRate

    #############################################################################

    # genetic algorithm
    def run(self, DEBUG=False):
        if self._popGeneratorOpr == None:
            raise Exception("Value popGeneratorFnc is not initialised.")
        if self._fitnessOpr == None:
            raise Exception("Value fitnessFnc is not initialised.")
        if self._selectionOpr == None:
            raise Exception("Value selectionFnc is not initialised.")
        if self._crossoverOpr == None:
            raise Exception("Value crossoverFnc is not initialised.")
        if self._iterCount == None:
            raise Exception("Value iterCount is not initialised.")
        if self._popSize == None:
            raise Exception("Value popSize is not initialised.")
        if self._crossRate == None:
            raise Exception("Value crossRate is not initialised.")
        if self._mutRate == None:
            raise Exception("Value mutRate is not initialised.")

        # initial population of random bitstring
        pop:List = self._popGeneratorOpr.run(self._popSize)
        #print("(len(pop)" + str(len(pop)))
        #print("_popSize" + str(self._popSize))
        indivType = type(pop[0])
        # keep track of best solution
        bestIndivIJ, bestFitnessIJ = pop[1], self._fitnessOpr.run(pop[1])

        #showRouteMaps(bestIndivIJ.exportUnraveledPermutation(self.itemsDF).clustersOfItemIdsDict.values(), self.itemsDF)

        # enumerate generations
        for genI in range(self._iterCount):
            if DEBUG:
                print("Generation: %s" % genI)
            print("Generation: %s" % genI)
            # evaluate all candidates in the population
            fitnessValuesI = [self._fitnessOpr.run(cI) for cI in pop]
            print("fitnessValuesI: " + str(fitnessValuesI))
            # check for new best solution
            for indexJ in range(len(pop)):
                isBetterMin = (not self._selectionOpr.isMaximization()) and fitnessValuesI[indexJ] < bestFitnessIJ
                isBetterMax = self._selectionOpr.isMaximization() and fitnessValuesI[indexJ] > bestFitnessIJ
                if isBetterMin or isBetterMax:
                    bestIndivIJ, bestFitnessIJ = pop[indexJ], fitnessValuesI[indexJ]
            if DEBUG:
                print("Best individual f(%s) = %.3f" % (bestIndivIJ, bestFitnessIJ))
            print("Best individual f(%s) = %.3f" % (bestIndivIJ, bestFitnessIJ))
            #self._fitnessOpr.run(bestIndivIJ, debug=DEBUG)
            # select parents
            #print("self._selectionOpr: " + str(self._selectionOpr))
            #selectedI = self._selectionOpr.run(pop, fitnessValuesI, len(pop))
            selectedI = self._selectionOpr.run(pop, fitnessValuesI, self._popSize)
            # create the next generation
            childrenI = list()
            for indexJ in range(0, len(selectedI), 2):
                # get selected parents in pairs
                p1, p2 = selectedI[indexJ], selectedI[indexJ + 1]
                # crossover and mutation
                ch1, ch2 = self._crossoverOpr.run(p1, p2)
                # mutation
                chNew1 = self._mutationOpr.run(ch1, self._mutRate)
                if type(chNew1) != indivType:
                    raise Exception("Individual is not " + indivType  + ": " + str(chNew1))
                chNew2 = self._mutationOpr.run(ch2, self._mutRate)
                if type(chNew2) != indivType:
                    raise Exception("Individual is not " + indivType  + ": " + str(chNew2))
                # store for next generation
                childrenI.append(chNew1)
                childrenI.append(chNew2)
            # replace population
            pop = childrenI
            #pop = pop[-self._popSize:] # take last N individuals
            #pop.extend(childrenI)

        self.lastPopulation:List = pop
        self.lastPopFitness:List[float] = [self._fitnessOpr.run(indivI) for indivI in pop]

        self.bestOfAllIndiv = self.lastPopulation[0]
        self.bestOfAllFitnessValue = self.lastPopFitness[0]
        for indivI, fitnessI in zip(self.lastPopulation, self.lastPopFitness):
            isBetterMin = (not self._selectionOpr.isMaximization()) and fitnessI < self.bestOfAllFitnessValue
            isBetterMax = self._selectionOpr.isMaximization() and fitnessI > self.bestOfAllFitnessValue
            if isBetterMin or isBetterMax:
                self.bestOfAllIndiv = indivI
                self.bestOfAllFitnessValue = fitnessI

        return (self.bestOfAllIndiv, self.bestOfAllFitnessValue)


    def getPopAndFitnessValues(self, indivCount:int):
        sortedPopFitness, sortedPopulation = zip(*sorted(zip(self.lastPopFitness, self.lastPopulation)))
        return (list(sortedPopulation)[:indivCount], list(sortedPopFitness)[:indivCount])
