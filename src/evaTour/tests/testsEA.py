import sys
from typing import List

from pandas import DataFrame
from pandas import Series

from evaTour.datasets.datasetFoursquare import readDatasetNYC, getNearestNeighbors
from evaTour.ea.individuals.individualClusters import IndividualClusters
from evaTour.ea.operators.clusters.crossover.crossoverCluUniform import CrossoverCluUniform
from evaTour.ea.operators.clusters.fitness.fitnessCluComplexTSP import FitnessCluComplexTSP
from evaTour.ea.operators.clusters.generator.generatorCluImproveSolution import GeneratorCluImproveSolution
from evaTour.ea.operators.clusters.mutation.mutationCluImprove import MutationCluImprove
from evaTour.ea.operators.clusters.mutation.mutationCluImproveCluster import MutationCluImproveCluster
from evaTour.ea.operators.oneHot.fitness.fitnessNegSum import FitnessNegSum
from evaTour.ea.operators.roundtrip.fitness.fitnessComplex import FitnessComplex
from evaTour.ea.operators.roundtrip.generator.generatorRtPerm import GeneratorRtPerm
from evaTour.ea.operators.selectionGeneral.selectionRandom import SelectionRandom
from evaTour.maps.openStreetMaps import showRouteMap, showRouteMaps

from evaTour.ea.easimple.ea import EvolutionAlgorithm
from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP

from evaTour.ea.operators.selectionGeneral.selectionRoulette import SelectionRoulette
from evaTour.ea.operators.selectionGeneral.selectionTournament import SelectionTournament
from evaTour.ea.operators.roundtrip.crossover.crossoverRtPMX import CrossoverRtPMX
from evaTour.ea.operators.roundtrip.crossover.crossoverRtOnePoint import CrossoverRtOnePoint
from evaTour.ea.operators.oneHot.mutation.mutationFlipOneBit import MutationFlipOneBit
from evaTour.ea.operators.roundtrip.mutation.mutationRt2Opt import MutationRt2Opt
from evaTour.ea.operators.oneHot.generator.generator01 import Generator01
from evaTour.ea.operators.roundtrip.generator.generatorRtRoulette import GeneratorRtRoulette

from pandas import Series
from typing import List
import os

from evaTour.recommenders.recommenderSVDS import RecommenderSVDS


def test01():
    print("test01")

    n_bits = 20
    iterCount = 20
    popSize = 20
    crossRate = 0.4
    mutRate = 0.5

    e = EvolutionAlgorithm()
    e.setIterCount(iterCount)
    e.setPopSize(popSize)
    e.setCrossRate(crossRate)
    e.setMutRate(mutRate)
    e.setPopGeneratorOpr(Generator01(n_bits))
    e.setFitnessOpr(FitnessNegSum())
    e.setSelectionOpr(SelectionTournament(2))
    e.setCrossoverOpr(CrossoverRtOnePoint(1))
    e.setMutationOpr(MutationFlipOneBit(0.01))

    bestIndiv, bestFitness = e.run()

    print("")
    print("bestIndiv:   " + str(bestIndiv))
    print("bestFitness: " + str(bestFitness))


def test02():
    print("test02")
    ratingsDF, itemsDF, distancesDF = readDatasetNYC()

    individual = [1,2,3,4,5,6,7]
    individual = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    individual = list(range(20,50))

    fitnessValue = FitnessKmPrecalculatedTSP(itemsDF, distancesDF).run(individual)
    print("FitnessValue: " + str(fitnessValue))
    print("")

    iterCount = 200
    popSize = 20
    crossRate = 0.5
    mutRate = 0.5

    e = EvolutionAlgorithm()
    e.setIterCount(iterCount)
    e.setPopSize(popSize)
    e.setCrossRate(crossRate)
    e.setMutRate(mutRate)
    #e.setPopGeneratorOpr(GeneratorRtRoulette(individual))
    e.setPopGeneratorOpr(GeneratorRtPerm(individual))
    e.setFitnessOpr(FitnessKmPrecalculatedTSP(itemsDF, distancesDF))
    e.setSelectionOpr(SelectionTournament(2))
    e.setCrossoverOpr(CrossoverRtPMX(1))
    #e.setMutationFnc(mutationNothingFnc, [])
    #e.setMutationFnc(mutationSwapFnc, [])
    e.setMutationOpr(MutationRt2Opt())

    bestIndiv, bestFitness = e.run()

    print("")
    print("BestIndiv:   " + str(bestIndiv))
    print("BestFitness: " + str(bestFitness))

    # BestFitness: 25.609221526422882
    showRouteMap(bestIndiv, itemsDF)


def test03():
    print("test03")
    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()

    iterCount = 200
    popSize = 40
    crossRate = 0.95
    mutRate = 0.95
    idealLengthOfRoundtrip = 15
    idealLandmarksCountInRoundtrip = 15

    uIdI = 1

    r = RecommenderSVDS({RecommenderSVDS.ARG_K:8})
    r.train(ratingsNYcDF, itemsNYcDF, distancesNYcDF)

    recommendation:Series = r.recommend(uIdI, 200)
    recomItemIDs:List = list(recommendation.keys())
    recomScores:List = list(recommendation.values)

    individualBaseDict = {}
    individualBaseDict[0] = recomItemIDs[0:5]
    individualBaseDict[1] = recomItemIDs[5:10]
    individualBaseDict[2] = recomItemIDs[10:15]
    print(individualBaseDict)

    showRouteMaps(individualBaseDict.values(), itemsNYcDF)

    e = EvolutionAlgorithm()
    e.setIterCount(iterCount)
    e.setPopSize(popSize)
    e.setCrossRate(crossRate)
    e.setMutRate(mutRate)
    e.setPopGeneratorOpr(GeneratorCluImproveSolution(individualBaseDict, recomItemIDs, recomScores, itemsNYcDF, distancesNYcDF, idealLengthOfRoundtrip, idealLandmarksCountInRoundtrip))
    e.setFitnessOpr(FitnessCluComplexTSP(idealLandmarksCountInRoundtrip, idealLengthOfRoundtrip, itemsNYcDF, distancesNYcDF))
    e.setSelectionOpr(SelectionRoulette())
    e.setCrossoverOpr(CrossoverCluUniform())
    e.setMutationOpr(MutationCluImprove(0))

    bestIndiv, bestFitness = e.run()

    print("")
    print("BestIndiv:   " + str(bestIndiv))
    print("BestFitness: " + str(bestFitness))

    # BestFitness: 25.609221526422882
    showRouteMap(bestIndiv, itemsNYcDF)

def test04():
    print("test04")

    ratingsDF:DataFrame
    itemsDF:DataFrame
    distancesDF:DataFrame
    ratingsDF, itemsDF, distancesDF = readDatasetNYC()

    iterCount:int = 5
    popSize:int = 10
    crossRate:float = 0.1
    mutRate:float = 0.5

    IDEAL_ROUNDTRIP_LENGTH:int = 25
    IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP:int = 20
    SELECTOR_THRESHOLD = 0.2
    DEBUG = False

    nearestNeighborsOfItemIdsDict:dict = getNearestNeighbors(distancesDF, 5)

    itemIds:List = [2717, 3664, 718, 2530, 3214, 1044, 3880, 4548, 2545, 1652, 3380, 1295, 2567, 3592, 2475, 1246, 1703, 1989, 3123, 3414]

    individualScoreDict:dict = {2717:0.1, 3664:0.1, 718:0.1, 2530:0.1, 3214:0.1, 1044:0.1, 3880:0.1, 4548:0.1, 2545:0.1, 1652:0.1, 3380:0.1, 1295:0.1, 2567:0.1, 3592:0.1, 2475:0.1, 1246:0.1, 1703:0.1, 1989:0.1, 3123:0.1, 3414:0.1}
    rItemIdsPoolScoreDict:dict[int, float] = {}


    ea = EvolutionAlgorithm()
    ea.setIterCount(iterCount)
    ea.setPopSize(popSize)
    ea.setCrossRate(crossRate)
    ea.setMutRate(mutRate)
    ea.setPopGeneratorOpr(GeneratorCluImproveSolution(IndividualClusters.constructFromDictOfList({0:itemIds}), individualScoreDict,
            rItemIdsPoolScoreDict, itemsDF, distancesDF, nearestNeighborsOfItemIdsDict, IDEAL_ROUNDTRIP_LENGTH,
            IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP, SelectionRandom(), SELECTOR_THRESHOLD, debug=DEBUG))
    ea.setFitnessOpr(FitnessCluComplexTSP(IDEAL_ROUNDTRIP_LENGTH, IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP, {}, itemsDF, distancesDF))
    ea.setSelectionOpr(SelectionRoulette(True))
    #ea.setSelectionOpr(SelectionRandom())
    ea.setCrossoverOpr(CrossoverCluUniform(itemsDF, distancesDF))
    ea.setMutationOpr(MutationCluImproveCluster(itemsDF, distancesDF, nearestNeighborsOfItemIdsDict,
                 IDEAL_ROUNDTRIP_LENGTH, IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP))
    bestIndiv, bestFitness = ea.run()

    individualResult:IndividualClusters = bestIndiv.exportUnraveledPermutation(distancesDF)

    showRouteMaps(individualResult.exportAsListOfList(), itemsDF)



if __name__ == "__main__":
    os.chdir('../../../')
    #test01()
    #test02()
    #test03()
    test04()