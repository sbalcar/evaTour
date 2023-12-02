from typing import List

from pandas import DataFrame

import numpy as np
from python_tsp.heuristics import solve_tsp_local_search


class IndividualCluster:

    def __init__(self, itemIds:List[int], isRaveled:bool=True):
        if not isinstance(itemIds, list):
            raise Exception("Argument itemIds is not list: " + str(itemIds))
        if not isinstance(isRaveled, bool):
            raise Exception("Argument isRaveled is not bool: " + str(isRaveled))

        self.itemIds:List[int] = itemIds
        self.isRaveled:bool = isRaveled

        self._unraveledItemIds:List[int] = None
        if not isRaveled:
            self._unraveledItemIds:dict[str, List[int]] = itemIds

    def clone(self):
        individual = IndividualCluster(self.itemIds, self.isRaveled)
        individual.itemIds = self.itemIds
        individual.isRaveled = self.isRaveled
        individual._unraveledItemIds = self._unraveledItemIds
        return individual

    def isValid(self):
        return True

    def setItemIds(self, clusterOfItemIds:List):
        self.itemIds = clusterOfItemIds
        self._unraveledItemIds = None
        self.isRaveled:bool = False

    def getItemIds(self):
        if not self.isRaveled:
            return self.itemIds
        return self._unraveledItemIds

    def getUnraveledItemIds(self, distancesDF:DataFrame):
        if self._unraveledItemIds != None:
            return self._unraveledItemIds

        self.exportUnraveledPermutation(distancesDF)
        return self._unraveledItemIds

    def exportUnraveledPermutation(self, distancesDF:DataFrame):
        if not isinstance(distancesDF, DataFrame):
            raise Exception("Argument distancesDF is not DataFrame: " + str(distancesDF))

        if self._unraveledItemIds != None:
            return IndividualCluster(self._unraveledItemIds, False)

        # select rows and columns with index positions
        distancesSelDF = distancesDF.iloc[self.itemIds, self.itemIds]
        distance_matrix = distancesSelDF.to_numpy()

        permutationOfIndexes, distance = solve_tsp_local_search(distance_matrix)

        # use numpy.take() to retrieve elements
        # from input list at given indices
        unraveledPermutation:List[int] = np.take(self.itemIds, permutationOfIndexes)

        self._unraveledItemIds = list(unraveledPermutation)

        return IndividualCluster(list(self._unraveledItemIds), False)