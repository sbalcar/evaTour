from evaTour.datasets.datasetFoursquare import _readOrigFiltred66Dataset, transformDataset, getDistances
from evaTour.webServer.datamodels.TeamsModel import TeamsModel

from pandas import DataFrame
from typing import List

import os


def countDistancesNYC():
    datasetDF:DataFrame = _readOrigFiltred66Dataset("dataset_TSMC2014_NYC.txt")

    ratingsDF, itemsDF = transformDataset(datasetDF)
    ratingsDF.to_csv('data/dataset_tsmc2014/ratingsNYC.txt', index=True)
    itemsDF.to_csv('data/dataset_tsmc2014/itemsNYC.txt', index=True)

    distancesDF:DataFrame = getDistances(itemsDF)
    distancesDF.to_csv('data/dataset_tsmc2014/distancesNYC.txt', index=True)

def countDistancesTKY():
    datasetDF:DataFrame = _readOrigFiltred66Dataset("dataset_TSMC2014_TKY.txt")

    ratingsDF, itemsDF = transformDataset(datasetDF)

    ratingsDF.to_csv('data/dataset_tsmc2014/ratingsTKY.txt', index=True)
    itemsDF.to_csv('data/dataset_tsmc2014/itemsTKY.txt', index=True)

    distancesDF:DataFrame = getDistances(itemsDF)
    distancesDF.to_csv('data/dataset_tsmc2014/distancesTKY.txt', index=True)


if __name__ == "__main__":
    os.chdir('../../../../')

    countDistancesNYC()
    countDistancesTKY()