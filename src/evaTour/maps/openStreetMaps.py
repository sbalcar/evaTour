import imgkit as imgkit

from typing import List
from pandas import DataFrame
from evaTour.datasets.datasetFoursquare import readDatasetNYC
from evaTour.datasets.datasetFoursquare import readDatasetTKY
from evaTour.datasets.datasetFoursquare import transformDataset
from evaTour.datasets.datasetFoursquare import _getGPS

import folium as fl
import matplotlib.pyplot as plt
import seaborn as sns

def convertIndividualToGPS(individual:List, itemsDF:DataFrame):
    gpsCoords = []
    for itemIDI in individual:
        latitude1, longitude1 = _getGPS(itemsDF, itemIDI)
        gpsCoords.append((latitude1, longitude1))
    return gpsCoords

def showRouteMap(individual:List, itemsDF:DataFrame):
    gpsCoords = convertIndividualToGPS(individual, itemsDF)

    showCoordsRouteMap(gpsCoords, individual)

def showCoordsRouteMap(gpsCoords:List, descrs:List):
    #print(gpsCoords)
    #print(descrs)

    myMap = fl.Map((gpsCoords[0][0], gpsCoords[0][1]), zoom_start=13)
    for gpsI,descrI in zip(gpsCoords, descrs):
        marker = fl.Marker([gpsI[0], gpsI[1]], tooltip=descrI)  # latitude,longitude
        myMap.add_child(marker)

    wind_line = fl.PolyLine(gpsCoords + [gpsCoords[0]], weight=15, color='#8EE9FF')
    myMap.add_child(wind_line)

    myMap.show_in_browser()
    #myMap.save("myRouteMapNYC.html", True)


def showRouteMaps(individuals:List[List], itemsDF:DataFrame):

    NUM_COLORS:int = len(individuals)
    colorsRGB:List[tuple] = sns.color_palette('husl', n_colors=NUM_COLORS)
    colorsRGBConv:List[tuple] = [(int(colorRI * 256), int(colorGI * 256), int(colorBI * 256)) for colorRI, colorGI, colorBI in colorsRGB]
    colors:List[str] = ['#%02x%02x%02x' % colorI for colorI in colorsRGBConv]

    #colors = ['#DFFF00', '#FFBF00', '#FF7F50', '#DE3163', '#9FE2BF', '#40E0D0', '#6495ED', '#CCCCFF']
    listOfGPSCoordsList = []
    listOfDescriptionList = []

    for individualI in individuals:
        #print(individualI)

        gpsCoordsI = convertIndividualToGPS(individualI, itemsDF)
        listOfGPSCoordsList.append(gpsCoordsI)
        listOfDescriptionList.append(individualI)

    showCoordsRouteMaps(listOfGPSCoordsList, listOfDescriptionList, colors)


def showCoordsRouteMaps(listOfGPSCoordsLists:List[List], listOfDescrsLists:List[List], colors:List):
    if listOfGPSCoordsLists == []:
        raise Exception("Arg listOfGPSCoordsLists is empty")

    myMap = fl.Map((listOfGPSCoordsLists[0][0][0], listOfGPSCoordsLists[0][0][1]), zoom_start=13)

    for gpsCoords, descrs, colorI in zip(listOfGPSCoordsLists, listOfDescrsLists, colors):
        for gpsI,descrI in zip(gpsCoords, descrs):
            marker = fl.Marker([gpsI[0], gpsI[1]], tooltip=descrI)  # latitude,longitude
            myMap.add_child(marker)

        wind_line = fl.PolyLine(gpsCoords + [gpsCoords[0]], weight=15, color=colorI)
        myMap.add_child(wind_line)

    myMap.show_in_browser()
    #myMap.save("myRouteMapNYC.html", True)



def showMapOfPlaces(individual:List, itemsDF:DataFrame):
    gpsCoords = []
    for itemIDI in individual:
        latitude1, longitude1 = _getGPS(itemsDF, itemIDI)
        gpsCoords.append((latitude1, longitude1))

    showCoordsMapOfPlaces(gpsCoords, individual)

def showCoordsMapOfPlaces(gpsCoords:List, descrs:List):
    myMap = fl.Map((gpsCoords[0][0], gpsCoords[0][1]), zoom_start=13)
    for gpsI,descrI in zip(gpsCoords, descrs):
        marker = fl.Marker([gpsI[0], gpsI[1]], tooltip=descrI)  # latitude,longitude
        myMap.add_child(marker)

    myMap.show_in_browser()
    #myMap.save("../../myMapOfPlacesNYC.html", True)


def showMapOfAllPlacesNYC():
    datasetTransfDF:DataFrame = readDatasetNYC()
    ratingsDF, itemsDF = transformDataset(datasetTransfDF)

    individual:List = list(range(len(itemsDF.home)))
    showMapOfPlaces(individual, itemsDF)

def showMapOfAllPlacesTKY():
    datasetTransfDF:DataFrame = readDatasetTKY()
    ratingsDF, itemsDF = transformDataset(datasetTransfDF)

    individual:List = list(range(len(itemsDF.home)))
    showMapOfPlaces(individual, itemsDF)


if __name__ == "__main__":
    print("")
    #test01()
    showMapOfAllPlacesNYC()
    #showMapOfAllPlacesTKY()

    #gpsCoords:List = [(40.681842, -73.949239), (40.676145, -73.949882)]
    #descrs:List = [1,2]
    #showCoordsMapOfPlaces(gpsCoords, descrs)

#169147    37683              138  40.681842 -73.949239
#219374    37683              138  40.676145 -73.949882