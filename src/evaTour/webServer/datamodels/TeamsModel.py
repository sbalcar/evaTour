#!/usr/bin/python3

from abc import ABC, abstractmethod

from evaTour.datasets.datasetFoursquare import readDatasetNYC
from evaTour.datasets.datasetFoursquare import readDatasetTKY

from typing import List
from pandas import DataFrame
from pandas import Series

import pandas as pd
import os

class TeamsModel(object):
    DESTINATION_NYC = "NYC"
    DESTINATION_TKY = "TKY"

    _modelDF = None

    def __init__(self):
        self._modelDF = pd.DataFrame([], columns=['TeamID', 'TeamName', 'Destination', 'MemberIDs'])

    @classmethod
    def readModel(self):
        df = pd.read_csv("teamsModel.csv", index_col=0)
        model = TeamsModel()
        model._modelDF = df
        return model

    def saveModel(self):
        self._modelDF.to_csv("teamsModel.csv")

    def addTeam(self, teamName:str, destination:str):
        #print("adding Team")
        teamID = len(self._modelDF)+1
        df = DataFrame({'TeamID':[teamID], 'TeamName':[teamName], 'Destination':destination, 'MemberIDs':[[]]})
        self._modelDF = pd.concat([self._modelDF, df], ignore_index=True)
        return teamID

    def removeTeam(self, teamID:str):
        #print("removing Team")
        index = self._modelDF.index[self._modelDF['TeamID'] == teamID].tolist()[0]
        #print("index: " + str(index))
        self._modelDF = self._modelDF.drop(index)

    def getTeamDestination(self, teamID:int):
        #print("teamID: " + str(teamID))
        if teamID == None:
            return None
        index = self._modelDF.index[self._modelDF['TeamID'] == int(teamID)].tolist()[0]

        destination = self._modelDF.loc[index, 'Destination']
        #print("destination: " + str(destination))
        return destination

    def getUserIDsOfTeam(self, teamID:int):
        #print("teamID: " + str(teamID))

        index = self._modelDF.index[self._modelDF['TeamID'] == int(teamID)].tolist()[0]
        #print("index: " + str(index))
        #print(self._modelDF)
        members = self._modelDF.loc[index, 'MemberIDs']

        if str(members) == "[]":
            #print("is empty")
            return []
        else:
            membersStr = str(members)[1:-1]
            #print("membersStr: " + str(membersStr))
            membersListOfStrI = list(membersStr.split(", "))
            #print("membersListOfStrI: " + str(membersListOfStrI))
            membersListI = [int(vI) for vI in membersListOfStrI]
            return membersListI


    def addUserToTeam(self, userID:int, teamID:int):
        #print("userID: " + str(userID))
        #print("teamID: " + str(teamID))

        index = self._modelDF.index[self._modelDF['TeamID'] == int(teamID)].tolist()[0]
        members = self._modelDF['MemberIDs'].iloc[index]
        #print("type(members)): " + str(type(members)))
        #print("members: " + str(members))

        members = self.getUserIDsOfTeam(teamID)
        members.append(int(userID))

        self._modelDF['MemberIDs'].at[index] = str(members)
        #print(self._modelDF.head(10))

    def removeUserFromTeam(self, userID:int, teamID:int):
        #print("userID: " + str(userID))
        #print("teamID: " + str(teamID))

        index = self._modelDF.index[self._modelDF['TeamID'] == teamID].tolist()[0]
        members = self._modelDF['MemberIDs'].iloc[index]
        #print("type(members)): " + str(type(members)))
        #print("members: " + str(members))

        membersStr = str(members)[1:-1]
        #print("membersStr: " + str(membersStr))
        membersListOfStrI = list(membersStr.split(", "))
        #print("membersListOfStrI: " + str(membersListOfStrI))
        membersListI = [int(vI) for vI in membersListOfStrI]
        membersListI.remove(userID)

        self._modelDF['MemberIDs'].at[index] = str(membersListI)

    def isMember(self, userID:int, selTeamID:int):
        #print("selTeamID: " + str(selTeamID))
        teamMembers = self.getUserIDsOfTeam(int(selTeamID))
        if userID in teamMembers:
            return True
        return False

    def getTeamIDsWhereUserIDBelongs(self, userID:int):

        selTeamsIds = []
        for rowI in self._modelDF.itertuples():
            teamIdI:int = rowI[1]
            membersSeriesI:str = rowI[4]

            membersStrI = str(membersSeriesI).strip("[]")
            #print("membersStrI: " + str(membersStrI))
            membersListOfStrI = list(membersStrI.split(", "))
            #print("len(membersListOfStrI): " + str(len(membersListOfStrI)))
            #print("membersListOfStrI: " + str(membersListOfStrI))
            if membersListOfStrI == ['']:
                continue
            membersListI = [int(vI) for vI in membersListOfStrI]

            #print("teamIdI: " + str(teamIdI))
            #print("teamNameI: " + str(teamNameI))

            if userID in membersListI:
                selTeamsIds.append(teamIdI)

        return selTeamsIds

    def exportTeamModelOfTeamIDs(self, teamIDs:List):

        selRowsDF = self._modelDF[self._modelDF['TeamID'].isin(teamIDs)]

        selTeamsModel = TeamsModel()
        selTeamsModel._modelDF = selRowsDF

        return selTeamsModel