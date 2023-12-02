from evaTour.webServer.datamodels.TeamsModel import TeamsModel

import os


def test01():
    print("test01")

    teamName = "testTeam"

    userId1 = 10001
    userId2 = 10002

    teamsModel = TeamsModel()
    teamID = teamsModel.addTeam(teamName, TeamsModel.DESTINATION_NYC)
    teamsModel.addUserToTeam(userId1, teamID)
    teamsModel.addUserToTeam(userId2, teamID)

    teamsModel.saveModel()

    #userIDsOfMyTeam = teamsModel.getTeamIDsWhereUserIDBelongs(userId)
    #print(userIDsOfMyTeam)


def test02():
    print("test02")

    teamID1 = 1
    teamID2 = 2
    teamName = "newTeam"

    userId1 = 10001
    userId2 = 10002
    userId3 = 10003

    teamsModel = TeamsModel.readModel()
    teamsModel.addTeam(teamName, TeamsModel.DESTINATION_NYC)
    print(teamsModel._modelDF.head())

    teamsModel.addUserToTeam(userId1, teamID2)
    teamsModel.addUserToTeam(userId2, teamID2)
    #teamsModel.removeTeam(teamID2)
    print(teamsModel._modelDF.head())

    teamsModel.addUserToTeam(userId2, teamID1)
    teamsModel.addUserToTeam(userId3, teamID1)
    print(teamsModel._modelDF.head())

    teamsModel.addUserToTeam(userId3, teamID1)
    teamsModel.removeUserFromTeam(userId3, teamID1)
    #teamsModel.removeUserFromTeam(userId1, teamID1)
    teamsModel.removeUserFromTeam(userId2, teamID1)

    a = teamsModel.getTeamIDsWhereUserIDBelongs(userId1)
    print(a)

    teamsModel.exportTeamModelOfTeamIDs([1,2])

    print(teamsModel._modelDF.head())


if __name__ == "__main__":
    os.chdir('../../../')
    #test01()
    test02()