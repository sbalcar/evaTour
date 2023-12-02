import time

from pandas import DataFrame
from typing import List
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import readDatasetNYC, readDatasetTKY, getNearestNeighbors
from evaTour.ea.easimple.ea import EvolutionAlgorithm
from evaTour.ea.individuals.individualClusters import IndividualClusters
from evaTour.ea.operators.clusters.crossover.crossoverCluUniform import CrossoverCluUniform
from evaTour.ea.operators.clusters.fitness.fitnessCluComplexTSP import FitnessCluComplexTSP

import os

from evaTour.ea.operators.clusters.generator.generatorCluImproveSolution import GeneratorCluImproveSolution
from evaTour.ea.operators.clusters.mutation.mutationCluImproveCluster import MutationCluImproveCluster
from evaTour.ea.operators.selectionGeneral.selectionRandom import SelectionRandom
from evaTour.ea.operators.selectionGeneral.selectionRoulette import SelectionRoulette
from evaTour.ea.operators.roundtrip.crossover.crossoverRtPMX import  CrossoverRtPMX
from evaTour.maps.openStreetMaps import showRouteMaps
from evaTour.recommenders.recommenderClusterEvolution import RecommenderClusterEvolution
from evaTour.recommenders.recommenderSVDS import RecommenderSVDS
from evaTour.recommenders.recommenderBirchTSPSolver import RecommenderBirchTSPSolver


def test01():
    print("test01")

    clustersOfItemIdsNYcDict:dict = {0: [232, 848, 265, 17, 733, 4257, 3688, 247, 2118, 970, 281, 982, 3520, 1025, 422, 350, 325, 1890, 3726],
                1: [3880, 718, 1044, 4541], 2: [4507, 1294], 3: [173, 1510, 42, 963, 2479, 172, 351, 1576, 755, 268, 41,
                182, 2208, 5082, 30, 57, 33, 174, 4358, 566, 29, 3970, 21, 3053, 1128, 3056, 31, 1002, 81, 215, 3815, 736, 118, 16, 744],
                4: [298, 4700, 3341, 3114, 1056, 1272, 2073], 5: [355, 3439, 3857],
                6: [220, 2833, 2272, 1600, 303, 3849, 4677, 2015, 2831, 4300, 228, 3669, 1849], 7: [2834, 2717, 3905, 4126, 3308],
                8: [2607, 1845, 4010, 4640, 3813, 3180, 4994], 9: [59, 359, 950, 78, 954]}
    clustersOfScoreNYcDict:dict = {0: [0.005886076890602624, 0.0005658266295995828, 0.0002829133147997914, 0.0006352184441716416,
                              0.0005691417454223728, 0.0005661854894994004, 0.00028640593661970914,
                              0.00030770102146844666, 0.0009581247874624015, 0.0008520550602221642,
                              0.000299121738817854, 0.0002829133147997914, 0.0002834144722585526, 0.0003545957281717393,
                              0.001211775236615383, 0.0006099662600452371, 0.002508275039444267, 0.00051274275605387,
                              0.0005696749528926414],
                          1: [0.00505078465553887, 0.00028865400621581395, 0.00028304538514216675,
                              0.004346024005928797], 2: [0.0004200171076788962, 0.00030907581643177556],
                          3: [0.02813771574476772, 0.00031763159811517064, 0.0006588230045550372, 0.0006963794314984697,
                              0.0037241650586059025, 0.001699721632656881, 0.0003097713962731238,
                              0.00031768560890247326, 0.0005701793938930493, 0.00029766470397119, 0.0015550924047157627,
                              0.0005792041702700946, 0.000673250266749193, 0.0006694386167685867, 0.0003243116262822845,
                              0.0003011084335718356, 0.0011927459739805059, 0.0012300854001484525,
                              0.0002894942707993298, 0.0015576782483372664, 0.0005884868301125417,
                              0.0011338359802837634, 0.005041718309793004, 0.000296538023750162, 0.0016384792955017843,
                              0.0004926807175612416, 0.0035616006103565885, 0.0011326696325619369,
                              0.0004859950157946706, 0.0008276899030870006, 0.0011807347987328623,
                              0.00029721717818780214, 0.00038833896858213356, 0.0015204659477575189,
                              0.00030570267731954093],
                          4: [0.002779146780642218, 0.00029365027067086453, 0.0025284492615312137,
                              0.0021149678887832043, 0.0002829133147997914, 0.0003451276870569248,
                              0.0007637084789344694],
                          5: [0.0005099690588267543, 0.00032867856641941403, 0.00028299104395373975],
                          6: [0.031270026177544194, 0.0002897205969065623, 0.0002909967886430366, 0.006509344586804132,
                              0.0005839217933998298, 0.0002864629420171156, 0.0008487399443993746,
                              0.00028507977517135667, 0.0008487399443993746, 0.00028867645936235027,
                              0.0002950481697191051, 0.0002858854397626146, 0.00028678722380063524],
                          7: [0.003879337975848951, 0.0005658266295995828, 0.0006913388236364751, 0.000307261699393989,
                              0.0011316532591991656],
                          8: [0.006191556307455706, 0.0019560972314581187, 0.0025526591793896326, 0.0013034855384117278,
                              0.0024440353845219896, 0.0004344951794705759, 0.0003916825194311409],
                          9: [0.024787583203140732, 0.0004660185476559871, 0.000284192174283313, 0.0004426907353757534,
                              0.00035543285096377013]}

    ratingsNYcDF:DataFrame
    itemsNYcDF:DataFrame
    distancesNYcDF:DataFrame
    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()

    ratingsTKYDF:DataFrame
    itemsTKYDF:DataFrame
    distancesTKYDF:DataFrame
    ratingsTKYDF, itemsTKYDF, distancesTKYDF = readDatasetTKY()


    userID = 1001
    DEBUG = False

    IDEAL_ROUNDTRIP_LENGTH = 20
    IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP = 20

    ratingsDF:DataFrame = ratingsNYcDF
    itemsDF:DataFrame = itemsNYcDF
    distancesDF:DataFrame = distancesNYcDF
    clustersOfItemIdsDict:dict = clustersOfItemIdsNYcDict
    clustersOfScoreDict:dict = clustersOfScoreNYcDict

    #ratingsDF:DataFrame = ratingsTKYDF
    #itemsDF:DataFrame = itemsTKYDF
    #distancesDF:DataFrame = distancesTKYDF
    #clustersOfItemIdsDict:dict = clustersOfItemIdsTKYDict
    #clustersOfScoreDict:dict = clustersOfScoreTKYDict

    rItemIdsPool:List[int]  = itemsDF['VenueID'].values[0:900]
    rItemIdsPoolScore:List[float] = [0.1]*len(rItemIdsPool)

    argsClusterDict = {RecommenderBirchTSPSolver.ARG_RECOMMENDER_CLASS:RecommenderSVDS,
                RecommenderBirchTSPSolver.ARG_RECOMMENDER_ARGS:{RecommenderSVDS.ARG_K:8},
                RecommenderBirchTSPSolver.ARG_RECOMMENDATION_POOL_SIZE:100,
                RecommenderBirchTSPSolver.ARG_CLUSTER_COUNT:10,
                RecommenderBirchTSPSolver.ARG_PYTHON_TSP_HEURISTIC_FNC:solve_tsp_local_search}
    rClusterClass = RecommenderBirchTSPSolver

    iterCount = 50
    popSize = 20
    crossRate = 0.5
    mutRate = 0.5

    ea = EvolutionAlgorithm()
    ea.setIterCount(iterCount)
    ea.setPopSize(popSize)
    ea.setCrossRate(crossRate)
    ea.setMutRate(mutRate)
    ea.setPopGeneratorOpr(GeneratorCluImproveSolution(IndividualClusters(clustersOfItemIdsDict), clustersOfScoreDict, rItemIdsPool, rItemIdsPoolScore,
            itemsDF, distancesDF, IDEAL_ROUNDTRIP_LENGTH, IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP))
    ea.setFitnessOpr(FitnessCluComplexTSP(IDEAL_ROUNDTRIP_LENGTH, IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP, itemsDF, distancesDF))
    ea.setSelectionOpr(SelectionRoulette())
    ea.setCrossoverOpr(CrossoverCluUniform(itemsDF, distancesDF))
    ea.setMutationOpr(MutationCluImproveCluster())
    #bestIndiv, bestFitness = ea.run()

    argsDict = {RecommenderClusterEvolution.ARG_RECOMMENDER_CLASS:rClusterClass,
                RecommenderClusterEvolution.ARG_RECOMMENDER_ARGS:argsClusterDict,
                RecommenderClusterEvolution.ARG_RECOMMENDER_EA:ea}
    r = RecommenderClusterEvolution(argsDict, DEBUG)
    r.train(ratingsNYcDF, itemsNYcDF, distancesNYcDF)
    clustersOfItemIdsDict:dict = r.recommendClusters(userID)

    showRouteMaps(clustersOfItemIdsDict.values(), itemsNYcDF)



def test02():
    print("test02")

    ratingsNYcDF:DataFrame
    itemsNYcDF:DataFrame
    distancesNYcDF:DataFrame
    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()

    ratingsTKYDF:DataFrame
    itemsTKYDF:DataFrame
    distancesTKYDF:DataFrame
    ratingsTKYDF, itemsTKYDF, distancesTKYDF = readDatasetTKY()

    userID = 1001
    DEBUG = True

    IDEAL_ROUNDTRIP_LENGTH:int = 15
    IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP:int = 20
    RECOMMENDATION_POOL_SIZE:int = 200
    BIRCH_CLUSTER_THRESHOLD = 0.001
    BIRCH_CLUSTER_COUNT = 8


    ratingsDF:DataFrame = ratingsNYcDF
    itemsDF:DataFrame = itemsNYcDF
    distancesDF:DataFrame = distancesNYcDF

    #ratingsDF:DataFrame = ratingsTKYDF
    #itemsDF:DataFrame = itemsTKYDF
    #distancesDF:DataFrame = distancesTKYDF
    #clustersOfItemIdsDict:dict = clustersOfItemIdsTKYDict
    #clustersOfScoreDict:dict = clustersOfScoreTKYDict

    #rItemIdsPool:List[int]  = itemsDF['VenueID'].values[0:RECOMMENDATION_POOL_SIZE]
    #rItemIdsPoolScore:List[float] = [0.1]*len(rItemIdsPool)
    #rScorePoolDict:dict = dict(zip(rItemIdsPool, rItemIdsPoolScore))

    argsClusterDict:dict = {RecommenderBirchTSPSolver.ARG_RECOMMENDER_CLASS:RecommenderSVDS,
                RecommenderBirchTSPSolver.ARG_RECOMMENDER_ARGS:{RecommenderSVDS.ARG_K:8},
                RecommenderBirchTSPSolver.ARG_RECOMMENDATION_POOL_SIZE:RECOMMENDATION_POOL_SIZE,
                RecommenderBirchTSPSolver.ARG_CLUSTER_THRESHOLD:BIRCH_CLUSTER_THRESHOLD,
                RecommenderBirchTSPSolver.ARG_CLUSTER_COUNT:BIRCH_CLUSTER_COUNT,
                RecommenderBirchTSPSolver.ARG_PYTHON_TSP_HEURISTIC_FNC:solve_tsp_local_search}
    rClusterClass = RecommenderBirchTSPSolver

    iterCount = 50
    popSize = 20
    crossRate = 0.1
    mutRate = 0.5

    ea = EvolutionAlgorithm()
    ea.itemsDF = itemsDF
    ea.distancesDF = distancesDF
    ea.setIterCount(iterCount)
    ea.setPopSize(popSize)
    ea.setCrossRate(crossRate)
    ea.setMutRate(mutRate)
    ea.setPopGeneratorOpr(GeneratorCluImproveSolution(IndividualClusters({}), {}, [], [],
            itemsDF, distancesDF, IDEAL_ROUNDTRIP_LENGTH, IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP))
    ea.setFitnessOpr(FitnessCluComplexTSP(IDEAL_ROUNDTRIP_LENGTH, IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP, {}, itemsDF, distancesDF))
    ea.setSelectionOpr(SelectionRoulette())
    ea.setCrossoverOpr(CrossoverCluUniform(itemsDF, distancesDF))
    ea.setMutationOpr(MutationCluImproveCluster())
    #bestIndiv, bestFitness = ea.run()

    argsDict:dict = {RecommenderClusterEvolution.ARG_RECOMMENDER_CLASS:rClusterClass,
                RecommenderClusterEvolution.ARG_RECOMMENDER_ARGS:argsClusterDict,
                RecommenderClusterEvolution.ARG_RECOMMENDER_EA:ea,
                RecommenderClusterEvolution.ARG_RECOMMENDATION_POOL_SIZE:RECOMMENDATION_POOL_SIZE,
                RecommenderClusterEvolution.ARG_BIRCH_CLUSTER_THRESHOLD:BIRCH_CLUSTER_THRESHOLD,
                RecommenderClusterEvolution.ARG_BIRCH_CLUSTER_COUNT:BIRCH_CLUSTER_COUNT}
    r = RecommenderClusterEvolution(argsDict, DEBUG)
    r.train(ratingsDF, itemsDF, distancesDF)


    bestOfAllIndiv:IndividualClusters
    bestOfAllIndiv, clustersOfScoreDict = r.recommendClusters(userID)

    individualResult:IndividualClusters = bestOfAllIndiv.exportUnraveledPermutation(distancesDF)

    showRouteMaps(individualResult.clustersOfItemIdsDict.values(), itemsDF)


def test03():
    print("test03")

    ratingsNYcDF:DataFrame
    itemsNYcDF:DataFrame
    distancesNYcDF:DataFrame
    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()

    ratingsTKYDF:DataFrame
    itemsTKYDF:DataFrame
    distancesTKYDF:DataFrame
    ratingsTKYDF, itemsTKYDF, distancesTKYDF = readDatasetTKY()

    userID:int = 1001
    DEBUG:bool = False

    IDEAL_ROUNDTRIP_LENGTH:int = 25
    IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP:int = 20
    ARG_NEAREST_NEIGHBORS_COUNT:int = 5
    RECOMMENDATION_POOL_SIZE:int = 200
    BIRCH_CLUSTER_THRESHOLD:float = 0.001
    BIRCH_CLUSTER_COUNT:int = 8
    SELECTOR_THRESHOLD = 0.2

    ratingsDF:DataFrame = ratingsNYcDF
    itemsDF:DataFrame = itemsNYcDF
    distancesDF:DataFrame = distancesNYcDF

    #ratingsDF:DataFrame = ratingsTKYDF
    #itemsDF:DataFrame = itemsTKYDF
    #distancesDF:DataFrame = distancesTKYDF
    #clustersOfItemIdsDict:dict = clustersOfItemIdsTKYDict
    #clustersOfScoreDict:dict = clustersOfScoreTKYDict

    nearestNeighborsOfItemIdsDict:dict = getNearestNeighbors(distancesDF, 5)

    #rItemIdsPool:List[int]  = itemsDF['VenueID'].values[0:RECOMMENDATION_POOL_SIZE]
    #rItemIdsPoolScore:List[float] = [0.1]*len(rItemIdsPool)
    #rScorePoolDict:dict = dict(zip(rItemIdsPool, rItemIdsPoolScore))

    argsClusterDict:dict = {RecommenderBirchTSPSolver.ARG_RECOMMENDER_CLASS:RecommenderSVDS,
                RecommenderBirchTSPSolver.ARG_RECOMMENDER_ARGS:{RecommenderSVDS.ARG_K:8},
                RecommenderBirchTSPSolver.ARG_RECOMMENDATION_POOL_SIZE:RECOMMENDATION_POOL_SIZE,
                RecommenderBirchTSPSolver.ARG_CLUSTER_THRESHOLD:BIRCH_CLUSTER_THRESHOLD,
                RecommenderBirchTSPSolver.ARG_CLUSTER_COUNT:BIRCH_CLUSTER_COUNT,
                RecommenderBirchTSPSolver.ARG_PYTHON_TSP_HEURISTIC_FNC:solve_tsp_local_search}
    rClusterClass = RecommenderBirchTSPSolver

    iterCount:int = 5
    popSize:int = 10
    crossRate:float = 0.1
    mutRate:float = 0.5

    ea = EvolutionAlgorithm()
    ea.setIterCount(iterCount)
    ea.setPopSize(popSize)
    ea.setCrossRate(crossRate)
    ea.setMutRate(mutRate)
    ea.setPopGeneratorOpr(GeneratorCluImproveSolution(IndividualClusters({}), {}, {}, itemsDF, distancesDF, nearestNeighborsOfItemIdsDict,
            IDEAL_ROUNDTRIP_LENGTH, IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP, SelectionRandom(), SELECTOR_THRESHOLD, debug=DEBUG))
    ea.setFitnessOpr(FitnessCluComplexTSP(IDEAL_ROUNDTRIP_LENGTH, IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP, {}, itemsDF, distancesDF))
    ea.setSelectionOpr(SelectionRoulette(True))
    #ea.setSelectionOpr(SelectionRandom())
    ea.setCrossoverOpr(CrossoverCluUniform(itemsDF, distancesDF))
    ea.setMutationOpr(MutationCluImproveCluster(itemsDF, distancesDF, nearestNeighborsOfItemIdsDict,
                 IDEAL_ROUNDTRIP_LENGTH, IDEAL_LANDMARKS_COUNT_IN_ROUNDTRIP))
    #bestIndiv, bestFitness = ea.run()

    argsDict:dict = {RecommenderClusterEvolution.ARG_RECOMMENDER_CLASS:rClusterClass,
                RecommenderClusterEvolution.ARG_RECOMMENDER_ARGS:argsClusterDict,
                RecommenderClusterEvolution.ARG_RECOMMENDER_EA:ea,
                RecommenderClusterEvolution.ARG_NEAREST_NEIGHBORS_COUNT:ARG_NEAREST_NEIGHBORS_COUNT,
                RecommenderClusterEvolution.ARG_RECOMMENDATION_POOL_SIZE:RECOMMENDATION_POOL_SIZE,
                RecommenderClusterEvolution.ARG_BIRCH_CLUSTER_THRESHOLD:BIRCH_CLUSTER_THRESHOLD,
                RecommenderClusterEvolution.ARG_BIRCH_CLUSTER_COUNT:BIRCH_CLUSTER_COUNT}

    r = RecommenderClusterEvolution(argsDict, DEBUG)
    r.train(ratingsDF, itemsDF, distancesDF)

    startTime = time.time()
    bestOfAllIndiv:IndividualClusters
    clustersOfScoreDict:dict
    bestOfAllIndiv, clustersOfScoreDict = r.recommendClusters(userID)
    endTime = time.time()

    individualResult:IndividualClusters = bestOfAllIndiv.exportUnraveledPermutation(distancesDF)

    print("Duration: " + str(endTime-startTime))

    showRouteMaps(individualResult.clustersOfItemIdsDict.values(), itemsDF)


if __name__ == "__main__":
    os.chdir('../../../')
    print("")
    #test01()
    #test02()
    test03()