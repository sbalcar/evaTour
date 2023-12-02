from typing import List
from pandas import DataFrame
from pandas import Series

import pandas as pd
import numpy as np
import os

def userSimilarity(userID1:int, userID2:int, similarityNYCDF:DataFrame, similarityTKYDF:DataFrame):
    #print("userID1: " + str(userID1))
    #print("userID2: " + str(userID2))
    #print("len(similarityNYCDF): " + str(len(similarityNYCDF)))
    #print("len(similarityTKYDF): " + str(len(similarityTKYDF)))
    if userID1 < 20000 and userID2 < 11053:  # 11083
        return similarityNYCDF.loc[userID1-10001][userID2-10001]
    elif userID1 > 20000 and 20000 < userID2 and userID2 < 22238:
        return similarityTKYDF.iloc[userID1-20001][userID2-20001]
    else:
        return -1

def readSimilarityDFNYC():
    similarityDF:DataFrame = pd.read_csv('data/dataset_tsmc2014/userSimilarityNYC.txt', index_col=0)
    return similarityDF

def readSimilarityDFTKY():
    similarityDF:DataFrame = pd.read_csv('data/dataset_tsmc2014/userSimilarityTKY.txt', index_col=0)
    return similarityDF