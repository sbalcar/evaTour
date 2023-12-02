import os

from evaTour.webServer.datamodels.UsersModel import UsersModel


def test01():
    print("test01")

    model = UsersModel.readModel()

    is1 = model.authorize("nyc1", "123")
    print("is1: " + str(is1))

    is2 = model.authorize("nyc1", "1234")
    print("is2: " + str(is2))

    is3 = model.authorize("none", "1234")
    print("is3: " + str(is3))


def test02():
    print("test02")

    model = UsersModel.readModel()

    userID1 = 10001
    userNYCID1:str = model.getNYCUserIDFromUserID(userID1)
    print("NYCuserID: " + str(userNYCID1))

    userIDa = 10242
    userName = model.getUsername(int(userIDa))
    print("userName: " + str(userName))

    userID2 = 20002
    userName2:str = model.getTKYUserIDFromUserID(userID2)
    print("NYCuserID: " + str(userName2))


if __name__ == "__main__":
    os.chdir('../../../')
#    test01()
    test02()