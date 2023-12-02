from pandas import DataFrame
from typing import List

from evaTour.datasets.datasetFoursquare import readDatasetNYC
from evaTour.maps.openStreetMaps import showMapOfPlaces

from evaTour.recommenders.recommenderSVDS import RecommenderSVDS

import os

def test01():
    print("test01")

    ratingsNYcDF:DataFrame = None
    itemsNYcDF:DataFrame = None
    distancesNYcDF:DataFrame = None

    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()
    #ratingsTkyDF, itemsTkyDF, distancesTkyDF = readDatasetTKY()

    userID:int = 1083

    r = RecommenderSVDS({RecommenderSVDS.ARG_K:8})
    r.train(ratingsNYcDF, itemsNYcDF, distancesNYcDF)
    recommendationI = r.recommend(userID, 500)
    print(recommendationI)

    showMapOfPlaces(recommendationI.keys(), itemsNYcDF)

def test02():
    print("test02")

    ratingsNYcDF:DataFrame = None
    itemsNYcDF:DataFrame = None
    distancesNYcDF:DataFrame = None

    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()

    r = RecommenderSVDS({RecommenderSVDS.ARG_K:8})
    r.train(ratingsNYcDF, itemsNYcDF, distancesNYcDF)

    itemIDs:List = []
    for uIdI in list(set(ratingsNYcDF['UserID'])):
        recommendationI = r.recommend(uIdI, 20)
        itemIDs = itemIDs + list(recommendationI.keys())

    itemIDs = list(set(itemIDs))

    showMapOfPlaces(itemIDs, itemsNYcDF)

if __name__ == "__main__":
    os.chdir('../../../')
    test01()
    #test02()
    #test03()