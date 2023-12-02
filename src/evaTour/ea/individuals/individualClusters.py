from typing import List

from pandas import DataFrame

import numpy as np
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.ea.individuals.individualCluster import IndividualCluster


class IndividualClusters:

    def __init__(self, individualsDict:dict[int, IndividualCluster]):
        if not isinstance(individualsDict, dict):
            raise Exception("Argument individualsDict is not dict: " + str(individualsDict))
        for clusterIdI, clusterI in individualsDict.items():
            if not isinstance(clusterI, IndividualCluster):
                raise Exception("Argument clusterI is not IndividualCluster: " + str(clusterI))

        self.individualsDict:dict = individualsDict

    @classmethod
    def constructFromDictOfList(cls, clustersOfItemIdsDict:dict[int, List], isRaveled:bool=True):
        if not isinstance(clustersOfItemIdsDict, dict):
            raise Exception("Argument clustersOfItemIdsDict is not dict: " + str(clustersOfItemIdsDict))
        if not isinstance(isRaveled, bool):
            raise Exception("Argument isRaveled is not bool: " + str(isRaveled))

        clustersOfIndivDict:dict = {clusterIdI:IndividualCluster(list(clusterI), isRaveled)
            for clusterIdI, clusterI in clustersOfItemIdsDict.items()}

        myInstance = cls(clustersOfIndivDict)
        return myInstance

    def clone(self):
        clustersOfIndivDict:dict = {clusterIdI:clusterI.clone()
                for clusterIdI, clusterI in self.individualsDict.items()}
        return IndividualClusters(clustersOfIndivDict)

    def isValid(self):
        for clusterIdI, clusterI in self.individualsDict.items():
            if not clusterI.isValid():
                return False
        return True

    def getClusterByClusterId(self, clusterId:str):
        return self.individualsDict[clusterId]

    def setIndivClusterByClusterId(self, clusterId:str, cluster:IndividualCluster):
        if not isinstance(cluster, IndividualCluster):
            raise Exception("Argument cluster is not IndividualCluster: " + str(cluster))
        self.individualsDict[clusterId] = cluster

    def exportUnraveledPermutation(self, distancesDF:DataFrame):
        if not isinstance(distancesDF, DataFrame):
            raise Exception("Argument distancesDF is not DataFrame: " + str(distancesDF))

        clustersOfUnraveledItemIdsDict:dict = {}
        for clusterIdI, clusterI in self.individualsDict.items():

            clusterNewI:IndividualCluster = clusterI.exportUnraveledPermutation(distancesDF)
            clustersOfUnraveledItemIdsDict[clusterIdI] = clusterNewI

        return IndividualClusters(clustersOfUnraveledItemIdsDict)

    def exportAsListOfList(self):
        clustersListOfList:List = []
        for clusterIdI, clusterI in self.individualsDict.items():
            clustersListOfList.append(clusterI.getItemIds())
        return clustersListOfList