from numpy import sort
from typing import List

from pandas.core.frame import DataFrame  # class
from pandas.core.series import Series  # class

class RecommenderDummy:
    _ratingsDF:DataFrame = None
    _itemsDF:DataFrame = None
    _distancesDF:DataFrame = None

    def train(self, ratingsDF, itemsDF, distancesDF):
        self._ratingsDF = ratingsDF
        self._itemsDF = itemsDF
        self._distancesDF = distancesDF

    def recommend(self, userID:int):
        itemIDs:List[int] = self._itemsDF["VenueID"].values

        sortedItemIDs:List[int] = sort(itemIDs)

        finalScores = []
        for i in reversed(range(10)):
            n = round(len(sortedItemIDs) / 10)
            finalScores += [i] * n
        finalScores += [0] * 10
        finalScores = finalScores[0:len(sortedItemIDs)]

        return Series(finalScores,index=sortedItemIDs)