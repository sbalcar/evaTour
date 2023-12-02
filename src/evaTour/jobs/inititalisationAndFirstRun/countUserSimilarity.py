
from pandas import DataFrame
from typing import List

import pandas as pd
import numpy as np

import os

def getSimilarity(ratingsDF:DataFrame):
    print("")
    userIDsWithDup:List = ratingsDF["UserID"].values
    userIDs:List = sorted(list(set(userIDsWithDup)))

    distancesDF:DataFrame = pd.DataFrame(0, index=np.arange(len(userIDs)), columns=np.arange(len(userIDs)))
    for indexI in range(len(userIDs)):
        print("Counted: " + str(indexI) + " / " + str(len(userIDs)))
        userIdI = userIDs[indexI]
        itemIDsI = ratingsDF[ratingsDF["UserID"] == userIdI]["VenueID"].values
        for indexJ in range(len(userIDs)):
            userIdJ = userIDs[indexJ]
            itemIDsJ = ratingsDF[ratingsDF["UserID"] == userIdJ]["VenueID"].values
            intersectionSize = len(set(itemIDsI) & set(itemIDsJ))
            distancesDF.loc[indexI,indexJ] = intersectionSize
            distancesDF.loc[indexJ, indexI] = intersectionSize
    print(distancesDF.head())
    return distancesDF


def countUserNYCSimilarity():
    print("")
    ratingsDF:DataFrame = pd.read_csv('data/dataset_tsmc2014/ratingsNYC.txt', index_col=0)

    print(ratingsDF.head())
    distancesDF:DataFrame = getSimilarity(ratingsDF)
    distancesDF.to_csv('data/dataset_tsmc2014/userSimilarityNYC.txt', index=True)


def countUserTKYSimilarity():
    print("")
    ratingsDF:DataFrame = pd.read_csv('data/dataset_tsmc2014/ratingsTKY.txt', index_col=0)

    print(ratingsDF.head())
    distancesDF:DataFrame = getSimilarity(ratingsDF)
    distancesDF.to_csv('data/dataset_tsmc2014/userSimilarityTKY.txt', index=True)


if __name__ == "__main__":
    os.chdir('../../../../')

    #countUserNYCSimilarity()
    countUserTKYSimilarity()