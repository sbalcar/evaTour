from pandas import DataFrame

from evaTour.datasets.datasetFoursquare import readDatasetTKY
from evaTour.datasets.datasetFoursquare import transformDataset
import os

def test02():

    datasetTransfDF:DataFrame = readDatasetTKY()
    ratingsDF, itemsDF = transformDataset(datasetTransfDF)

    print(ratingsDF.head().to_string())
    print(itemsDF.head().to_string())

    #print(datasetTransfDF.head(200).to_string())
    print("len: " + str(len(datasetTransfDF)))


if __name__ == "__main__":
    os.chdir('../../../')
    print("")
    #test01()
    test02()
    #test03()