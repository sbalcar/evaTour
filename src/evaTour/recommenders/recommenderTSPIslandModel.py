from typing import List

from pandas.core.frame import DataFrame  # class
from pandas.core.series import Series  # class

from evaTour.ea.eaislandmodel.islandModel import IslandModel
from evaTour.ea.eaislandmodel.islandEATabu import IslandEATabu
from evaTour.ea.operators.roundtrip.crossover.crossoverRtPMX import CrossoverRtPMX
from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP
from evaTour.ea.operators.roundtrip.generator.generatorRtPerm import GeneratorRtPerm
from evaTour.ea.operatorRTMigration import migrationTabu
from evaTour.ea.operators.roundtrip.mutation.mutationRt2Opt import MutationRt2Opt
from evaTour.ea.operators.selectionGeneral.selectionRoulette import SelectionRoulette
from evaTour.recommenders.recommenderSVDS import RecommenderSVDS


class RecommenderTSPIslandModel:

    ARG_RECOMMENDER_CLASS:str = "recommenderClass"
    ARG_RECOMMENDER_CLASS_ARGS:str = "recommenderClassArgs"
    ARG_ISLAND_MODEL:str = "islandModel"

    def __init__(self, args:dict):
        self._args:dict = args

        recommenderClass = args[self.ARG_RECOMMENDER_CLASS]
        recommenderClassArgs:dict = args[self.ARG_RECOMMENDER_CLASS_ARGS]

        self._recommender = recommenderClass(recommenderClassArgs)
        self._im = args[self.ARG_ISLAND_MODEL]


    def train(self, ratingsDF:DataFrame, itemsDF:DataFrame, distancesDF:DataFrame):
        self._ratingsDF = ratingsDF
        self._itemsDF = itemsDF
        self._distancesDF = distancesDF

        self._recommender.train(ratingsDF, itemsDF, distancesDF)
        self._im.train(ratingsDF, itemsDF, distancesDF)

    def recommend(self, userID:int, k:int=20):
        recItemIDs:Series = self._recommender.recommend(userID, k)
        individual:List = recItemIDs.index.tolist()

        for islandI in self._im._islands:
            islandI.setPopGeneratorOpr(GeneratorRtPerm(individual))
        self._im.run()

        bestOfAllIndiv = self._im.getTheBestIndividual()

        return Series([1.0/len(bestOfAllIndiv)]*len(bestOfAllIndiv), index=bestOfAllIndiv)


def getRecTSPIslandModel(ratingsDF:DataFrame, itemsDF:DataFrame, distancesDF:DataFrame):
    print("")

    n_bits = 20
    iterCount = 100
    popSize = 20
    crossRate = 0.5
    mutRate = 0.2

    numberOfIslands = 8
    roundtripLength = 15

    islands:List = []
    for islandNumberI in range(numberOfIslands):
        eI = IslandEATabu(islandNumberI)
        #eI.setPopGeneratorFnc(generatorRouletteFnc, [roundtripLength, itemIDs, scores])
        eI.setFitnessFnc(FitnessKmPrecalculatedTSP(itemsDF, distancesDF))
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

    argsDict = {RecommenderTSPIslandModel.ARG_RECOMMENDER_CLASS:RecommenderSVDS,
                RecommenderTSPIslandModel.ARG_RECOMMENDER_CLASS_ARGS:{RecommenderSVDS.ARG_K:5},
                RecommenderTSPIslandModel.ARG_ISLAND_MODEL:eim}
    recommender = RecommenderTSPIslandModel(argsDict)

    return recommender