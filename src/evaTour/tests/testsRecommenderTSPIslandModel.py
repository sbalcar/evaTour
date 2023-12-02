from pandas import DataFrame

from evaTour.datasets.datasetFoursquare import readDatasetNYC

import os

from evaTour.recommenders.recommenderTSPIslandModel import getRecTSPIslandModel


def test01():
    print("test01")

    ratingsDF:DataFrame
    itemsDF:DataFrame
    distancesDF:DataFrame
    ratingsDF, itemsDF, distancesDF = readDatasetNYC()

    userID = 1
    k = 20

    recom = getRecTSPIslandModel(ratingsDF, itemsDF, distancesDF)
    recom.train(ratingsDF, itemsDF, distancesDF)
    recomendation = recom.recommend(userID, k)

    print("recomendation: " + str(recomendation))


if __name__ == "__main__":
    os.chdir('../../../')
    test01()