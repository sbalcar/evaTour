import time

from evaTour.datasets.datasetFoursquare import readDatasetNYC, readDatasetTKY, getNearestNeighbors
from evaTour.ea.individuals.individualClusters import IndividualClusters
from evaTour.ea.operators.clusters.generator.generatorCluImproveSolution import GeneratorCluImproveSolution
from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP
from evaTour.ea.operators.roundtrip.fitness.fitnessKmTSP import FitnessKmTSP
from evaTour.ea.operators.roundtrip.fitness.fitnessKmTSPSolver import FitnessKmTSPSolver

from evaTour.ea.operators.roundtrip.generator.generatorRtPerm import GeneratorRtPerm
from evaTour.ea.operators.roundtrip.generator.generatorRtRoulette import GeneratorRtRoulette
from pandas import DataFrame
from pandas import Series
from typing import List
import os

from evaTour.ea.operators.selectionGeneral.selectionRandom import SelectionRandom
from evaTour.maps.openStreetMaps import showRouteMaps
from evaTour.recommenders.recommenderSVDS import RecommenderSVDS


def test01():
    print("test01")

    popSize = 5
    indivPerm = [0,1,2,3,4,5]
    a = GeneratorRtPerm(indivPerm).run(popSize)
    print(a)

def test02():
    print("test03")

    individual = [1,2,3,4,5,6,7]
    popSize = 20

    a = GeneratorRtPerm(individual).run(popSize)
    print(a)

def test03():
    print("test03")

    ratingsNYcDF:DataFrame = None
    itemsNYcDF:DataFrame = None
    distancesNYcDF:DataFrame = None
    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()

    r = RecommenderSVDS({RecommenderSVDS.ARG_K:8})
    r.train(ratingsNYcDF, itemsNYcDF, distancesNYcDF)

    uIdI = 1
    recommendation:Series = r.recommend(uIdI, 200)
    itemIDs:List = list(recommendation.keys())
    scores:List = list(recommendation.values)
    popSize = 5
    roundtripLength = 20

    genItems = GeneratorRtRoulette(roundtripLength, itemIDs, scores).run(popSize)
    print("itemIDs: " + str(itemIDs))
    print("scores: " + str(scores))
    print("genItems: " + str(genItems))


def test03():
    print("test03")

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

    #clustersOfItemIdsDict:dict = {0: [220, 2833, 2272, 1600, 303, 3849, 4677, 2015, 2831, 4300, 228, 3669, 1849]}

    #clustersOfScoreDict:dict = {0: [0.031270026177544194, 0.0002897205969065623, 0.0002909967886430366, 0.006509344586804132,
    #    0.0005839217933998298, 0.0002864629420171156, 0.0008487399443993746, 0.00028507977517135667, 0.0008487399443993746,
    #    0.00028867645936235027, 0.0002950481697191051, 0.0002858854397626146, 0.00028678722380063524]}

    ratingsNYcDF:DataFrame
    itemsNYcDF:DataFrame
    distancesNYcDF:DataFrame
    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()

    # Tokyo
    clustersOfItemIdsTKYDict:dict = {0: [379, 2954, 6054, 3801, 2374, 3603, 6225, 6674, 4474, 6641, 207, 354, 1601, 6501, 6224, 5199, 2007],
            1: [3131, 5443, 67, 1354, 5565, 5469, 1543, 4133, 2455], 2: [1856, 1166, 2332, 5088, 3248, 5646],
            3: [2534, 3432, 899, 2929, 1950], 4: [4892, 889, 166], 5: [825], 6: [102, 2523], 7: [723, 4029, 3331],
            8: [447, 236, 5398, 4059, 643, 2885, 185, 4053, 1059, 666, 387, 1861, 308, 3818, 3513, 2218, 1066, 2902, 1773, 4684,
            2472, 1477, 6071, 555, 60, 761, 441, 133, 4928, 407, 3263, 1790, 494, 582, 1240, 1265, 5234, 253, 4103, 1261, 1048, 1060,
            1176, 464, 1266, 1267, 3348, 1353, 1138, 873, 654, 5241], 9: [787, 3178]}
    clustersOfScoreTKYDict:dict = {0: [0.04231608506182822, 0.0015829751064522625, 0.0010729199144298037, 0.00220642049118625,
                              0.009965012502294947, 0.0003657764780260147, 0.004860981708436559, 0.0005304933602684391,
                              0.0003745624207329941, 0.00045336400698230817, 0.0029430002425602426,
                              0.0015812323945843547, 0.010981976493624392, 0.0011019596643417142, 0.0040161154130157585,
                              0.004268042644770704, 0.0004723853016150956],
                          1: [0.036981984956506044, 0.0008540279053731321, 0.00036546466406613874,
                              0.0003539883549275924, 0.0005426724008107013, 0.0013948102828430858,
                              0.0015859545064673376, 0.0040040921633235655, 0.032744843233934104],
                          2: [0.002487933389592963, 0.00035129163800557724, 0.0014488354259377197,
                              0.0004598947909575809, 0.0005586111047434236, 0.00039259342528012996],
                          3: [0.017117765416275372, 0.0003732740838640325, 0.0007630130304549453,
                              0.00037218992990717875, 0.0003728823511434701],
                          4: [0.0007116899211442769, 0.00045565087592186986, 0.0003314604281566678],
                          5: [0.00029529014269679457], 6: [0.020866831192421963, 0.00033803465063545087],
                          7: [0.0008474220504048329, 0.000364573628132742, 0.00042279858229849707],
                          8: [0.03112999746355705, 0.003427988595701744, 0.0003226382806265743, 0.00044298408432064985,
                              0.0016118795569093707, 0.002065917226085538, 0.0017689201077680508,
                              0.00036003079660307117, 0.0013371299504909557, 0.00043658205665461994,
                              0.027718867750389706, 0.0004744680597449623, 0.0008289244263087257,
                              0.00042258929741181383, 0.00037158009993302186, 0.0026188114744041748,
                              0.0007517501740481149, 0.0005162565171115403, 0.028801875113474557, 0.0003721253351364212,
                              0.0009734361682308415, 0.000973056080948516, 0.0009721963416873116, 0.005602069291920447,
                              0.0004192119766484396, 0.001114420492980758, 0.0005963035877874211, 0.0003018795677497193,
                              0.00039263708047188224, 0.010493574910234914, 0.002459303203139185, 0.0030192046741745666,
                              0.0006733916132539924, 0.0011173234359339178, 0.002318619223680231, 0.0021759228406495953,
                              0.00037225683815945906, 0.00047208597041908994, 0.00034157441503171844,
                              0.00029266484075929296, 0.0012237431186609992, 0.006365950638359184, 0.005731726903549573,
                              0.0058848519827345595, 0.0011892581334804868, 0.0021554529952400522, 0.002154531723187999,
                              0.002521878432195021, 0.002574006502793588, 0.00039462402326406027, 0.000464918504807336,
                              0.0003927141651167112], 9: [0.0006445010014191318, 0.0003416170030163728]}

    ratingsTKYDF:DataFrame
    itemsTKYDF:DataFrame
    distancesTKYDF:DataFrame
    ratingsTKYDF, itemsTKYDF, distancesTKYDF = readDatasetTKY()


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


    #showRouteMaps(clustersOfItemIdsDict.values(), itemsNYcDF)

    rItemIdsPool:List[int] = itemsDF['VenueID'].values[0:900]
    rItemIdsPoolScore:List[float] = [0.1]*len(rItemIdsPool)
    rItemIdsPoolDict:dict =  dict(zip(rItemIdsPool, rItemIdsPoolScore))

    nearestNeighborsOfItemIdsDict:dict = getNearestNeighbors(distancesDF, 5)

    userID = 2
    popSize = 10
    k = 100
    SELECTOR_THRESHOLD = 0.2
    DEBUG = False

    idealRoundtripLength:int = 20
    idealLandmarksCountInRoundtrip:int = 15

    individualBase = IndividualClusters(clustersOfItemIdsDict)
    generator = GeneratorCluImproveSolution(individualBase, clustersOfScoreDict, rItemIdsPoolDict,
                 itemsDF, distancesDF, nearestNeighborsOfItemIdsDict, idealRoundtripLength, idealLandmarksCountInRoundtrip,
                 SelectionRandom(), SELECTOR_THRESHOLD)

    # prvni jedinec ktery to vrati je vstupni bez uprav

    startTime = time.time()
    individualGen:IndividualClusters = generator.run(popSize,DEBUG)[1]
    endTime = time.time()

    individualOrderedGen:IndividualClusters = individualGen.exportUnraveledPermutation(distancesDF)
    clustersOfItemIdsDict:dict = individualOrderedGen.clustersOfItemIdsDict
    #print("clustersOfItemIdsDict: " + str(clustersOfItemIdsDict))

    orderedClustersOfDistancesDict:dict = {}
    for clusterIdI, clustersOfItemIdsI in clustersOfItemIdsDict.items():
        fI = FitnessKmPrecalculatedTSP(itemsDF, distancesDF)
        distanceI:float = fI.run(list(clustersOfItemIdsI))
        orderedClustersOfDistancesDict[clusterIdI] = distanceI

    clusterSizesDict:dict = [len(clustersOfItemIdsI) for clusterIdI, clustersOfItemIdsI in clustersOfItemIdsDict.items()]

    print()
    print("Measurement by clusters:")
    print("clusterSizesDict: " + str(clusterSizesDict))
    print("orderedClustersOfDistancesDict: " + str(orderedClustersOfDistancesDict))

    print()
    print("Duration: " + str(endTime-startTime))


    #showRouteMaps(orderedClustersOfItemIdsDict.values(), itemsDF)
    showRouteMaps(clustersOfItemIdsDict.values(), itemsDF)

if __name__ == "__main__":
    os.chdir('../../../')
    #test01()
    #test02()
    test03()