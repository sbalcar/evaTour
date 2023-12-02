import sys
from typing import List

from pandas import DataFrame
from pandas import Series
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import _getItemIDDistance

import numpy as np

from evaTour.ea.individuals.individualClusters import IndividualClusters
from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP
from evaTour.ea.operators.roundtrip.fitness.fitnessKmTSP import FitnessKmTSP
from evaTour.ea.operators.roundtrip.fitness.fitnessKmTSPSolver import FitnessKmTSPSolver
from evaTour.ea.operators.selectionGeneral.selectionRoulette import SelectionRoulette


class GeneratorCluImproveSolution:

    def __init__(self, individualBase:IndividualClusters, individualScoreDict:dict, rItemIdsPoolScoreDict:dict[int, float],
                 itemsDF:DataFrame, distancesDF:DataFrame, nearestNeighborsOfItemIdsDict:dict,
                 idealRoundtripLength:int, idealLandmarksCountInRoundtrip:int, selector, selectorThreshold:float,
                 debug:bool = False):
        if not isinstance(individualBase, IndividualClusters):
            raise Exception("Argument individualBase is not " + str(IndividualClusters) + ": " + str(individualBase))
        if not isinstance(individualScoreDict, dict):
            raise Exception("Argument individualScoreDict is not " + str(dict) + ": " + str(individualScoreDict))
        if not isinstance(rItemIdsPoolScoreDict, dict):
            raise Exception("Argument rItemIdsPoolScoreDict is not " + str(dict) + ": " + str(rItemIdsPoolScoreDict))
        if not isinstance(itemsDF, DataFrame):
            raise Exception("Argument itemsDF is not " + str(DataFrame) + ": " + str(itemsDF))
        if not isinstance(distancesDF, DataFrame):
            raise Exception("Argument distancesDF is not " + str(DataFrame) + ": " + str(distancesDF))
        if not isinstance(nearestNeighborsOfItemIdsDict, dict):
            raise Exception("Argument nearestNeighborsOfItemIdsDict is not " + str(dict) + ": " + str(nearestNeighborsOfItemIdsDict))

        self.individualScoreDict:dict = individualScoreDict
        self.rItemIdsPoolScoreDict:dict[int,float] = rItemIdsPoolScoreDict
        self.itemsDF:DataFrame = itemsDF
        self.distancesDF:DataFrame = distancesDF
        self.nearestNeighborsOfItemIdsDict:dict[int,Series] = nearestNeighborsOfItemIdsDict
        self.idealRoundtripLength:int = idealRoundtripLength
        self.idealLandmarksCountInRoundtrip:int = idealLandmarksCountInRoundtrip
        self.selector = selector
        self.selectorThreshold:float = selectorThreshold

        self.setIndividualBase(individualBase, debug)

    def setIndividualBase(self, individualBase:IndividualClusters, debug:bool=False):
        self.individualBase:IndividualClusters = individualBase
        individualUnraveledBase:IndividualClusters = individualBase.exportUnraveledPermutation(self.distancesDF)
        clustersDict:dict = individualUnraveledBase.individualsDict
        print("clustersDict: " + str(clustersDict))
        self.fitnessOfClustersKmDict:dict = {clusterIdI:FitnessKmPrecalculatedTSP(self.itemsDF, self.distancesDF).run(clusterI, debug)
                                             for clusterIdI, clusterI in clustersDict.items()}

    def run(self, popSize:int, debug:bool=False):
        population:List[dict] = [self.individualBase]
        for i in range(popSize -1):
            newIndivDict:dict = self.generateIndividual(self.individualBase, debug)
            population.append(newIndivDict)
        return population

    def generateIndividual(self, individualBase:IndividualClusters, debug:bool=False):
        if not isinstance(individualBase, IndividualClusters):
            raise Exception("Argument individualBase is not " + str(IndividualClusters) + ": " + str(individualBase))
        individualUnraveledBase:IndividualClusters = individualBase.exportUnraveledPermutation(self.distancesDF)
        individualBaseDict:dict[List[int]] = individualUnraveledBase.individualsDict

        newIndivDict:dict = {}
        for clusterIdI, itemIdsOfCluI in individualBaseDict.items():
            clusterSizeI = len(itemIdsOfCluI.getUnraveledItemIds(self.distancesDF))
            if clusterSizeI > self.idealLandmarksCountInRoundtrip:
                # budeme mazat mesta -> vymazeme ty s tim nejmensim raitingem
                # print("clusterSizeI: " + str(clusterSizeI))
                landmarksCountInRoundtripToDel:int = clusterSizeI - self.idealLandmarksCountInRoundtrip
                itemIdsOfNewCluI:List[int] = self._improveClusterDel(clusterIdI, itemIdsOfCluI, landmarksCountInRoundtripToDel, debug)
                newIndivDict[clusterIdI] = itemIdsOfNewCluI
            elif clusterSizeI < self.idealLandmarksCountInRoundtrip:
                # budeme pridavat mesta
                landmarksCountInRoundtripToAdd:int = self.idealLandmarksCountInRoundtrip - clusterSizeI
                itemIdsOfNewCluI:List[int] = self._improveClusterAdd(clusterIdI, itemIdsOfCluI, landmarksCountInRoundtripToAdd, debug)
                newIndivDict[clusterIdI] = itemIdsOfNewCluI
            else:
                # budeme menit mesta
                a = 1
                # todo
                newIndivDict[clusterIdI] = itemIdsOfCluI.clone()
        return IndividualClusters(newIndivDict)

    def _improveClusterDel(self, clusterIdI:int, clusterOfItemIDs:List[int], landmarksCountInRoundtripToRemove:int, debug:bool=False):
        scores:List[float] = self.individualScoreDict[clusterIdI]
        selectedItemIds:List[int] = self.selector.run(clusterOfItemIDs, scores, landmarksCountInRoundtripToRemove)

        if debug:
            print("clusterOfItemIDs: " + str(len(clusterOfItemIDs)))
            print("selectedItemIds: " + str(len(selectedItemIds)))

        newIndiv:List = [eI for eI in clusterOfItemIDs if eI not in selectedItemIds]
        return newIndiv

    def _improveClusterAdd(self, clusterIdI:int, clusterOfItemIDs:List[int], landmarksCountInRoundtripToAdd:int, debug:bool=False):

        distanceOfItemIdsDict:dict = {}
        for itemIdI in clusterOfItemIDs:
            neighborsOfItemIdsSer:Series = self.nearestNeighborsOfItemIdsDict[itemIdI]
            for nghItemIdJ, nghDistanceJ in neighborsOfItemIdsSer.items():
                curDistanceJ = distanceOfItemIdsDict.get(nghItemIdJ, sys.maxsize)
                if nghDistanceJ < curDistanceJ:
                    distanceOfItemIdsDict[nghItemIdJ] = nghDistanceJ

        for itemIdI in clusterOfItemIDs:
            distanceOfItemIdsDict.pop(itemIdI, None)

        selectionOpr = SelectionRoulette(False)
        selItemIds:List = selectionOpr.run(list(distanceOfItemIdsDict.keys()), list(distanceOfItemIdsDict.values()), landmarksCountInRoundtripToAdd)

        return list(clusterOfItemIDs) + selItemIds


    def _improveClusterAdd2(self, clusterIdI:int, clusterOfItemIDs:List[int], landmarksCountInRoundtripToAdd:int, debug:bool=False):
        itemIdsPoolDisjointScoreDict:dict = {rItemIdI:rItemIdsPoolScoreI for rItemIdI, rItemIdsPoolScoreI in
                zip(self.rItemIdsPoolScoreDict.keys(), self.rItemIdsPoolScoreDict.values()) if rItemIdI not in clusterOfItemIDs}
        if debug:
            print("itemIdsPoolDisjointScoreDict: " + str(itemIdsPoolDisjointScoreDict))
            print("self.rItemIdsPool: " + str(self.rItemIdsPool))

        itemIdsPoolDisjointDistanceDict:dict = {}
        for rItemIdI, rItemIdsPoolScoreI in itemIdsPoolDisjointScoreDict.items():
            # vzdalenosti itemu z poolu ke vsem itemum v klastru
            distancesSerI:Series = self.distancesDF.iloc[rItemIdI][clusterOfItemIDs]
            #print("distancesSerI: " + str(distancesSerI))
            # nejmensi vzdalenost ke klastru
            minDistanceOfItemFromCluster:int = min(distancesSerI.values)
            #print("minDistanceOfItemFromCluster: " + str(minDistanceOfItemFromCluster))
            theNearstRItemIdIToCluster:float = distancesSerI[distancesSerI == minDistanceOfItemFromCluster].index[0]
            #print("theNearstRItemIdIToCluster: " + str(theNearstRItemIdIToCluster))
            itemIdsPoolDisjointDistanceDict[rItemIdI] = minDistanceOfItemFromCluster

        if debug:
            print("itemIdsPoolDisjointDistanceDict: " + str(itemIdsPoolDisjointDistanceDict))
        currentClusterDistance:int = self.fitnessOfClustersKmDict[clusterIdI]
        itemIdsPoolDisjointDistanceDict:dict = {itemIdI:distanceI for itemIdI, distanceI
                in itemIdsPoolDisjointDistanceDict.items()
                if 0.33 * distanceI * landmarksCountInRoundtripToAdd < self.idealRoundtripLength - currentClusterDistance}

        if debug:
            print("self.idealRoundtripLength: " + str(self.idealRoundtripLength))
            print("currentClusterDistance: " + str(currentClusterDistance))

        itemIdsPoolDisjointReverzDistanceDict:dict = {cI:1/dI for cI, dI in itemIdsPoolDisjointDistanceDict.items() if 1 / dI > self.selectorThreshold}

        itemIds:List[int] = []
        if len(itemIdsPoolDisjointReverzDistanceDict) != 0:
            itemIds = list(self.selector.run(list(itemIdsPoolDisjointReverzDistanceDict.keys()),
                    list(itemIdsPoolDisjointReverzDistanceDict.values()), landmarksCountInRoundtripToAdd))

        if debug:
            print("clusterOfItemIDs: " + str(clusterOfItemIDs))
            #print("itemIds: " + str(itemIds))

        return list(clusterOfItemIDs) + itemIds
