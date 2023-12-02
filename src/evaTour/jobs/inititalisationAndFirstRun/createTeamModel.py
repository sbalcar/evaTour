import os

from evaTour.webServer.datamodels.TeamsModel import TeamsModel

if __name__ == "__main__":
    os.chdir('../../../../')

    teamName1 = "testTeam1"

    userID1 = 10001
    userID2 = 10010
    userID3 = 10011

    teamsModel = TeamsModel()
    teamID1 = teamsModel.addTeam(teamName1)
    print(teamsModel._modelDF.head())

    teamsModel.addUserToTeam(userID1, teamID1)
    teamsModel.addUserToTeam(userID2, teamID1)
    teamsModel.addUserToTeam(userID3, teamID1)


    teamsModel.saveModel()