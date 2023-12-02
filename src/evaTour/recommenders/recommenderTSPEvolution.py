from typing import List

from pandas.core.frame import DataFrame  # class
from pandas.core.series import Series  # class

from evaTour.ea.easimple.ea import EvolutionAlgorithm
from evaTour.ea.operators.roundtrip.crossover.crossoverRtPMX import CrossoverRtPMX
from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP
from evaTour.ea.operators.roundtrip.fitness.fitnessKmTSPSolver import FitnessKmTSPSolver
from evaTour.ea.operators.roundtrip.generator.generatorRtPerm import GeneratorRtPerm
from evaTour.ea.operators.roundtrip.generator.generatorRtRoulette import GeneratorRtRoulette
from evaTour.ea.operators.roundtrip.mutation.mutationRt2Opt import MutationRt2Opt
from evaTour.ea.operators.selectionGeneral.selectionRoulette import SelectionRoulette
from evaTour.recommenders.recommenderSVDS import RecommenderSVDS


class RecommenderTSPEvolution:

    ARG_RECOMMENDER_CLASS:str = "recommenderClass"
    ARG_RECOMMENDER_CLASS_ARGS:str = "recommenderClassArgs"
    ARG_RECOMMENDER_EA:str = "recommenderEA"

    def __init__(self, args:dict):
        self._args:dict = args

        recommenderClass = args[self.ARG_RECOMMENDER_CLASS]
        recommenderClassArgs:dict = args[self.ARG_RECOMMENDER_CLASS_ARGS]

        self._recommender = recommenderClass(recommenderClassArgs)
        self._ea = args[self.ARG_RECOMMENDER_EA]


    def train(self, ratingsDF:DataFrame, itemsDF:DataFrame, distancesDF:DataFrame):
        self._ratingsDF = ratingsDF
        self._itemsDF = itemsDF
        self._distancesDF = distancesDF

        self._recommender.train(ratingsDF, itemsDF, distancesDF)

    def recommend(self, userID:int, k:int=20, DEBUG=False):
        recItemIDs:Series = self._recommender.recommend(userID, k)
        individual:List = recItemIDs.index.tolist()

        self._ea.setPopGeneratorOpr(generatorPermFnc, [individual])
        bestOfAllIndiv, bestOfAllFitnessValue = self._ea.run(DEBUG)

        return Series([1.0/len(bestOfAllIndiv)]*len(bestOfAllIndiv), index=bestOfAllIndiv)


def getRecTSPEvolution(ratingsDF:DataFrame, itemsDF:DataFrame, distancesDF:DataFrame):
    print("")

    iterCount = 200
    popSize = 20
    crossRate = 0.5
    mutRate = 0.5

    individual = range(0,30)

    ea = EvolutionAlgorithm()
    ea.setIterCount(iterCount)
    ea.setPopSize(popSize)
    ea.setCrossRate(crossRate)
    ea.setMutRate(mutRate)
    ea.setPopGeneratorOpr(GeneratorRtPerm(individual))
    ea.setFitnessOpr(FitnessKmPrecalculatedTSP(itemsDF, distancesDF))
    ea.setSelectionOpr(SelectionRoulette())
    ea.setCrossoverOpr(CrossoverRtPMX())
    #ea.setMutationFnc(mutationNothingFnc, [])
    #ea.setMutationFnc(mutationSwapFnc, [])
    ea.setMutationOpr(MutationRt2Opt())
    #bestIndiv, bestFitness = ea.run()


    argsDict = {RecommenderTSPEvolution.ARG_RECOMMENDER_CLASS:RecommenderSVDS,
                RecommenderTSPEvolution.ARG_RECOMMENDER_CLASS_ARGS:{RecommenderSVDS.ARG_K:5},
                RecommenderTSPEvolution.ARG_RECOMMENDER_EA:ea}
    recommender = RecommenderTSPEvolution(argsDict)

    return recommender


def getRecTSPEvolution2(ratingsDF:DataFrame, itemsDF:DataFrame, distancesDF:DataFrame, rItemIDs, rScores):
    print("")

    iterCount = 50
    popSize = 20
    crossRate = 0.5
    mutRate = 0.5

    indivSize = 20

    ea = EvolutionAlgorithm()
    ea.setIterCount(iterCount)
    ea.setPopSize(popSize)
    ea.setCrossRate(crossRate)
    ea.setMutRate(mutRate)
    ea.setPopGeneratorOpr(GeneratorRtRoulette(indivSize, rItemIDs, rScores))
    ea.setFitnessOpr(FitnessKmTSPSolver(itemsDF, distancesDF))
    ea.setSelectionOpr(SelectionRoulette())
    ea.setCrossoverOpr(CrossoverRtPMX())
    ea.setMutationOpr(MutationRt2Opt())
    #bestIndiv, bestFitness = ea.run()


    argsDict = {RecommenderTSPEvolution.ARG_RECOMMENDER_CLASS:RecommenderSVDS,
                RecommenderTSPEvolution.ARG_RECOMMENDER_CLASS_ARGS:{RecommenderSVDS.ARG_K:5},
                RecommenderTSPEvolution.ARG_RECOMMENDER_EA:ea}
    recommender = RecommenderTSPEvolution(argsDict)

    return recommender