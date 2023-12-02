import os

from evaTour.webServer.datamodels.UsersModel import UsersModel

if __name__ == "__main__":
    os.chdir('../../../../')

    model = UsersModel.generateModel()
    model.saveModel()

