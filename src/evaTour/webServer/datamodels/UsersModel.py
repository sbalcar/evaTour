#!/usr/bin/python3

from abc import ABC, abstractmethod

from evaTour.datasets.datasetFoursquare import readDatasetNYC
from evaTour.datasets.datasetFoursquare import readDatasetTKY

from pandas import DataFrame
from pandas import Series
from typing import List


import pandas as pd
import os

class UsersModel(object):
    _modelDF = None

    @classmethod
    def generateModel(self):
        ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()
        ratingsTkyDF, itemsTkyDF, distancesTkyDF = readDatasetTKY()

        data:List[List] = []

        usersIDNYC = list(set(ratingsNYcDF['UserID']))
        usersIDNYC.sort()
        for uIDNYcI in usersIDNYC:
            rowI = [10*1000 + uIDNYcI, "nyc" + str(uIDNYcI), ["NYC"], "123"]
            data.append(rowI)

        usersIDTky = list(set(ratingsTkyDF['UserID']))
        usersIDTky.sort()
        for uIDTkyI in usersIDTky:
            rowI = [20*1000 + uIDTkyI, "tky" + str(uIDTkyI), ["TKY"], "123"]
            data.append(rowI)

        df = pd.DataFrame(data, columns=['UserID', 'Login', 'Destinations', 'Passwd'])

        model = UsersModel()
        model._modelDF = df
        return model

    @classmethod
    def readModel(self):
        df = pd.read_csv("userModel.csv")
        model = UsersModel()
        model._modelDF = df
        return model

    def saveModel(self):
        self._modelDF.to_csv("userModel.csv")

    def authorize(self, userName:str, passwd:str):
        selUsers:Series = self._modelDF[self._modelDF["Login"] == userName]
        if len(selUsers) == 0:
            return False

        if str(selUsers["Passwd"].iloc[0]) == passwd:
            return True
        return False

    def getUsername(self, userID:int):
        selUsers:Series = self._modelDF[self._modelDF["UserID"] == userID]
        #print(selUsers)
        if len(selUsers) == 0:
            return None

        userName:str = str(selUsers["Login"].iloc[0])
        return userName

    def getUserIDFromUserName(self, userName:str):
        selUsers:Series = self._modelDF[self._modelDF["Login"] == userName]
        if len(selUsers) == 0:
            return None

        return str(selUsers["UserID"].iloc[0])

    def getNYCUserIDFromUserID(self, userID:int):
        selUsers:Series = self._modelDF[self._modelDF["UserID"] == userID]
        #print(selUsers)
        if len(selUsers) == 0:
            return None

        userName:str = str(selUsers["Login"].iloc[0])
        if not userName.startswith("nyc"):
            return None

        return int(userName[3:])

    def getTKYUserIDFromUserID(self, userID:int):
        selUsers:Series = self._modelDF[self._modelDF["UserID"] == userID]
        if len(selUsers) == 0:
            return None

        userName:str = str(selUsers["Login"].iloc[0])
        if not userName.startswith("tky"):
            return None

        return int(userName[3:])

    def translateUserIdToDatasetUserId(self, userId:int):
        if 10000 < userId and userId < 20000:
            return userId -10000
        elif 20000 < userId and userId < 30000:
            return userId -20000
        else:
            print("chyba")

    def exportUserModelOfDestionation(self, destination:str):
        if destination == None:
            return self

        selUsersModel = UsersModel()
        selUsersModel._modelDF = self._modelDF[self._modelDF['Destinations'].str.contains(destination)]

        return selUsersModel