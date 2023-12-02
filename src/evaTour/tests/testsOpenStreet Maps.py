from pandas import DataFrame

from evaTour.datasets.datasetFoursquare import readDatasetNYC
from evaTour.ea.operators.oneHot.fitness.fitnessNegSum import FitnessNegSum
from evaTour.maps.openStreetMaps import showCoordsRouteMap
from evaTour.maps.openStreetMaps import showMapOfPlaces

from evaTour.ea.easimple.ea import EvolutionAlgorithm
from evaTour.ea.operators.oneHot.generator.generator01 import Generator01
from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP
from evaTour.ea.operators.selectionGeneral.selectionTournament import SelectionTournament
from evaTour.ea.operators.roundtrip.crossover.crossoverRtOnePoint import CrossoverRtOnePoint
from evaTour.ea.operators.oneHot.mutation.mutationFlipOneBit import MutationFlipOneBit

from evaTour.recommenders.recommenderDummy import RecommenderDummy
import os

def test01():
    print("test01")

    itineraire = [(33.5649577, -7.5822778), (33.5651468, -7.5823494), (33.5656444, -7.582575300000001), (33.565812, -7.582148500000001), (33.5658939, -7.5819043), (33.5659518, -7.5816994), (33.5660413, -7.581388799999999), (33.566598, -7.581672499999999), (33.5671508, -7.5819214)]

    showCoordsRouteMap(itineraire)


def test02():
    print("test02")

    ratingsDF:DataFrame
    itemsDF:DataFrame
    distancesDF: DataFrame
    ratingsDF, itemsDF, distancesDF = readDatasetNYC()


    individual = [1,2,3,4,5,6,7]
    fitnessValue = FitnessKmPrecalculatedTSP(itemsDF, distancesDF).run(individual)
    print("FitnessValue: " + str(fitnessValue))

    n_bits = 20
    iterCount = 20
    popSize = 20
    crossRate = 0.5
    mutRate = 0.2

    e = EvolutionAlgorithm()
    e.setPopGeneratorOpr(Generator01(n_bits))
    e.setFitnessOpr(FitnessNegSum())
    e.setSelectionOpr(SelectionTournament())
    e.setCrossoverOpr(CrossoverRtOnePoint())
    e.setMutationOpr(MutationFlipOneBit())

    e.run(iterCount, popSize, crossRate, mutRate)

    showMapOfPlaces(individual, itemsDF)


def test03():
    print("test03")

    ratingsDF:DataFrame
    itemsDF:DataFrame
    distancesDF:DataFrame
    ratingsDF, itemsDF, distancesDF = readDatasetNYC()

    rcmndr = RecommenderDummy()
    rcmndr.train(ratingsDF, itemsDF, distancesDF)
    r = rcmndr.recommend(5)
    print(r)

if __name__ == "__main__":
    os.chdir('../../../')
    #test01()
    test02()
    #test03()