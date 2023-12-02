from pandas import DataFrame

from evaTour.datasets.datasetFoursquare import _getDistance, _getVenueCategoryName, getVisitedPlacesOfUser, divideTrainTest
from evaTour.datasets.datasetFoursquare import _getGPS
from evaTour.datasets.datasetFoursquare import readDatasetNYC
from evaTour.datasets.datasetFoursquare import transformDataset
from evaTour.ea.operators.roundtrip.fitness.fitnessKmPrecalculatedTSP import FitnessKmPrecalculatedTSP

import pandas as pd
import os

def test01():
    # Arts & Crafts Store
    latitude1 = 40.719810375488535
    longitude1 = -74.00258103213994
    # Bridge
    latitude2 = 40.60679958140643
    longitude2 = -74.04416981025437

    km = _getDistance(latitude1, longitude1, latitude2, longitude2)
    print("km: " + str(km))

def test02():

    ratingsDF:DataFrame
    itemsDF:DataFrame
    distancesDF:DataFrame
    ratingsDF, itemsDF, distancesDF = readDatasetNYC()

    print(ratingsDF.head().to_string())
    print(itemsDF.head().to_string())

    #print(datasetTransfDF.head(200).to_string())
    print("selRatings: " + str(len(ratingsDF)))

    # Arts & Crafts Store
    venueID1 = itemsDF.iloc[0]["VenueID"]
    # Bridge
    venueID2 = itemsDF.iloc[1]["VenueID"]

    latitude1, longitude1 = _getGPS(itemsDF, int(venueID1))
    latitude2, longitude2 = _getGPS(itemsDF, int(venueID2))

    km = _getDistance(latitude1, longitude1, latitude2, longitude2)
    print("km: " + str(km))


def test03():
    datasetTransfDF:DataFrame = readDatasetNYC()
    ratingsDF, itemsDF = transformDataset(datasetTransfDF)

    #print(datasetTransfDF.head(200).to_string())
#    print("len: " + str(len(datasetTransfDF)))

    individual = [1,2,3,4]
    fitnessValue = FitnessKmPrecalculatedTSP(itemsDF).run(individual)
    print("fitnessValue: " + str(fitnessValue))


def test04():
    import numpy
    R = numpy.array([
         [5,3,0,1],
         [4,0,0,1],
         [1,1,0,5],
         [1,0,0,4],
         [0,1,5,4],
        ])

    from sklearn.decomposition import NMF
    model = NMF(n_components=4)

    A = model.fit_transform(R)
    B = model.components_

    n = numpy.dot(A, B)
    print(n)

def test05():
    ratingsDF:DataFrame
    itemsDF:DataFrame
    distancesDF:DataFrame
    ratingsDF, itemsDF, distancesDF = readDatasetNYC()

    print(_getVenueCategoryName(itemsDF))

    userID:int = 1
    a = getVisitedPlacesOfUser(userID, ratingsDF, itemsDF)
    print(a)

def test06():
    data = [[1, 10, 1], [1, 15, 1], [1, 20, 1]]
    ratingsDF:DataFrame = pd.DataFrame(data, columns=['UserID', 'VenueID', 'size'])

    trainDF, testDF = divideTrainTest(ratingsDF, 49)

    print("trainDF:")
    print(trainDF.head())

    print("testDF:")
    print(testDF.head())

if __name__ == "__main__":
    os.chdir('../../../')
    print("")
    #test01()
    #test02()
    #test03()
    #test04()
    #test05()
    test06()