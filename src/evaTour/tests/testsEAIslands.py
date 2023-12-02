from evaTour.datasets.datasetFoursquare import readDatasetNYC
from evaTour.ea.eaislandmodel.islandEATabu import IslandEATabu
from evaTour.ea.operatorRTMigration import migrationTabu
from evaTour.maps.openStreetMaps import showRouteMaps

from evaTour.ea.eaislandmodel.islandModel import IslandModel
from evaTour.ea.operators.roundtrip.generator.generatorRtPerm import GeneratorRtPerm
from evaTour.ea.operators.roundtrip.generator.generatorRtRoulette import GeneratorRtRoulette
from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP
from evaTour.ea.operators.selectionGeneral.selectionTournament import SelectionTournament
from evaTour.ea.operators.selectionGeneral.selectionRoulette import SelectionRoulette


from evaTour.ea.operators.roundtrip.crossover.crossoverRtPMX import CrossoverRtPMX
from evaTour.ea.operators.roundtrip.mutation.mutationRt2Opt import MutationRt2Opt

from pandas import Series
from typing import List
import os
import time
import copy

from evaTour.recommenders.recommenderSVDS import RecommenderSVDS


def test01():
    print("test01")

    ratingsDF, itemsDF, distancesDF = readDatasetNYC()

    individual = list(range(20,50))

    n_bits = 20
    iterCount = 100
    popSize = 20
    crossRate = 0.5
    mutRate = 0.2

    numberOfIslands = 8

    islands:List = []
    for islandNumberI in range(numberOfIslands):
        eI = IslandEATabu(islandNumberI)
        eI.setPopGeneratorFnc(GeneratorRtPerm(copy.deepcopy(individual)))
        eI.setFitnessFnc(FitnessKmPrecalculatedTSP(itemsDF, distancesDF))
        eI.setSelectionFnc(SelectionTournament(2))
        eI.setCrossoverFnc(CrossoverRtPMX())
        eI.setMutationFnc(MutationRt2Opt())

        islands.append(eI)

    eim = IslandModel(islands)
    eim.setMigrationFnc(migrationTabu, {IslandEATabu.ARG_MIGRATION_GEN_PERIOD:10})
    eim.setIterCount(iterCount)
    eim.setPopSize(popSize)
    eim.setCrossRate(crossRate)
    eim.setMutRate(mutRate)

    # get the start time
    st = time.time()

    #bestIndiv, bestFitness = e1.run()
    eim.run()

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')


def test02():
    print("test02")

    ratingsDF, itemsDF, distancesDF = readDatasetNYC()

    individual = list(range(20,50))

    n_bits = 20
    iterCount = 100
    popSize = 20
    crossRate = 0.5
    mutRate = 0.2

    numberOfIslands = 8

    islands:List = []
    for islandNumberI in range(numberOfIslands):
        eI = IslandEATabu(islandNumberI)
        eI.setPopGeneratorFnc(GeneratorRtPerm(copy.deepcopy(individual)))
        eI.setFitnessFnc(FitnessKmPrecalculatedTSP(itemsDF, distancesDF))
        eI.setSelectionFnc(SelectionTournament(2))
        eI.setCrossoverFnc(CrossoverRtPMX())
        eI.setMutationFnc(MutationRt2Opt())

        islands.append(eI)

    eim = IslandModel(islands)
    eim.setMigrationFnc(migrationTabu, {IslandEATabu.ARG_MIGRATION_GEN_PERIOD:10})
    eim.setIterCount(iterCount)
    eim.setPopSize(popSize)
    eim.setCrossRate(crossRate)
    eim.setMutRate(mutRate)

    # get the start time
    st = time.time()

    #bestIndiv, bestFitness = e1.run()
    eim.run()

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')


def test03():
    print("test03")

    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()

    n_bits = 20
    iterCount = 100
    popSize = 20
    crossRate = 0.5
    mutRate = 0.2

    numberOfIslands = 8
    roundtripLength = 15

    uIdI = 1

    r = RecommenderSVDS({RecommenderSVDS.ARG_K:8})
    r.train(ratingsNYcDF, itemsNYcDF, distancesNYcDF)

    recommendation:Series = r.recommend(uIdI, 200)
    itemIDs:List = list(recommendation.keys())
    scores:List = list(recommendation.values)

    islands:List = []
    for islandNumberI in range(numberOfIslands):
        eI = IslandEATabu(islandNumberI)
        eI.setPopGeneratorFnc(GeneratorRtRoulette(roundtripLength, itemIDs, scores))
        eI.setFitnessFnc(FitnessKmPrecalculatedTSP(itemsNYcDF, distancesNYcDF))
        eI.setSelectionFnc(SelectionRoulette())
        eI.setCrossoverFnc(CrossoverRtPMX())
        eI.setMutationFnc(MutationRt2Opt())

        islands.append(eI)

    eim = IslandModel(islands)
    eim.setMigrationFnc(migrationTabu, {IslandEATabu.ARG_MIGRATION_GEN_PERIOD:10})
    eim.setIterCount(iterCount)
    eim.setPopSize(popSize)
    eim.setCrossRate(crossRate)
    eim.setMutRate(mutRate)


    # get the start time
    st = time.time()

    eim.run()

    # get the end time
    et = time.time()

    # get the execution time
    elapsed_time = et - st
    print('Execution time:', elapsed_time, 'seconds')

    showRouteMaps(eim.resultBestIndivDict.values(), itemsNYcDF)

if __name__ == "__main__":
    os.chdir('../../../')
    test01()
    #test02()
    #test03()