from numpy import sort
from typing import List

from pandas.core.frame import DataFrame  # class
from pandas.core.series import Series  # class

from scipy.sparse.linalg import svds
import numpy as np

class RecommenderSVDS:
    _ratingsDF:DataFrame = None
    _itemsDF:DataFrame = None
    _distancesDF:DataFrame = None

    _userIdToUserIndexDict:dict = {}
    _userIndexToUserIdDict:dict = {}

    ARG_K = "k"
    DEBUG = None

    def __init__(self, args:dict, DEBUG=False):
        self._args = args
        self._DEBUG = DEBUG

    def train(self, ratingsDF, itemsDF, distancesDF):
        self._ratingsDF = ratingsDF
        self._itemsDF = itemsDF
        self._distancesDF = distancesDF

        if self._DEBUG:
            print(self._ratingsDF.head(10))
        userIDs:List = sorted(list(set(self._ratingsDF['UserID'])))
        self._userIdToUserIndexDict = dict(zip(userIDs, range(len(userIDs))))
        self._userIndexToUserIdDict = dict(zip(self._userIdToUserIndexDict.values(), self._userIdToUserIndexDict.keys()))

        itemIDs:List = sorted(list(set(self._ratingsDF['VenueID'])))
        self._itemIdToItemIndexDict = dict(zip(itemIDs, range(len(itemIDs))))
        self._itemIndexToItemIdDict = dict(zip(self._itemIdToItemIndexDict.values(), self._itemIdToItemIndexDict.keys()))

        userIDs:int = len(self._userIdToUserIndexDict.keys())
        venueIDs:int = len(self._itemIdToItemIndexDict.keys())
        zeors_array = np.zeros((userIDs, venueIDs))
        #print("userIDs: " + str(userIDs))
        #print("venueIDs: " + str(venueIDs))

        for indexI, rowI in self._ratingsDF.iterrows():
            # print(rowI)
            userIdI = rowI['UserID']
            itemIdI = rowI['VenueID']
            # print("userID: " + str(userID))
            # print("venueID: " + str(venueID))
            userIndexI = self._userIdToUserIndexDict[userIdI]
            itemIndexI = self._itemIdToItemIndexDict[itemIdI]
            sizeI = rowI['size']
            zeors_array[userIndexI, itemIndexI] = sizeI

        if self._DEBUG:
            print("Training started")
        u4, s4, vT4 = svds(zeors_array, k=self._args[self.ARG_K])
        self._A4 = u4 @ np.diag(s4) @ vT4
        if self._DEBUG:
            print("Training finished")


    def recommend(self, userID:int, k:int=20):
        #print(self._userIdToUserIndexDict.keys())
        userIndex:int = self._userIdToUserIndexDict[userID]

        vectorOfPref:List = self._A4[userIndex]
        #print(len(vectorOfPref))
        indexedVectorOfPref:List = list(zip(range(len(vectorOfPref)), vectorOfPref))
        #print(str(list(a)))

        sortedIndexedVectorOfPref = sorted(indexedVectorOfPref, key = lambda x: x[1], reverse=True)[:k]
        itemIdToScoresDict:dict = dict([(self._itemIndexToItemIdDict[indexI], prefI)
                                          for indexI, prefI in sortedIndexedVectorOfPref])

        finalScores = itemIdToScoresDict.values()
        sortedItemIDs = itemIdToScoresDict.keys()
        return Series(finalScores,index=sortedItemIDs)
