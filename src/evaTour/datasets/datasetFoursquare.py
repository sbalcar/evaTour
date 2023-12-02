from typing import List
from pandas import DataFrame
from pandas import Series

import pandas as pd
import numpy as np
import os

#  https://sites.google.com/site/yangdingqi/home/foursquare-dataset

def _readOrigFiltred66Dataset(fileName:str):
    m_cols = ["UserID", "VenueID", "VenueCategoryID", "VenueCategoryName", "Latitude", "Longitude", "TimezoneOffsetInMinutes", "UTCTime"]
    datasetDF:DataFrame = pd.read_csv('data/dataset_tsmc2014/'+fileName, sep='\t',  names=m_cols, encoding='latin-1')

    #print(datasetDF.head().to_string())
    #print()

    nonTouristVenueCategoryNames:List = ['Latin American Restaurant', 'Ethiopian Restaurant', 'Car Wash', 'Asian Restaurant', 'Thrift / Vintage Store', 'Factory', 'Athletic & Sport', 'Portuguese Restaurant', 'Music Venue', 'Spiritual Center', 'Gas Station / Garage', 'Chinese Restaurant', 'Parking', 'Fair', 'Record Shop', 'Mall', 'Sporting Goods Shop', 'Antique Shop', 'Rest Area', 'Government Building', 'Ski Area', 'American Restaurant', 'Stadium', 'Bar', 'Embassy / Consulate', 'Bakery', 'Eastern European Restaurant',
    'Argentinian Restaurant', 'Korean Restaurant', 'Video Store', 'Drugstore / Pharmacy', 'Tanning Salon', 'Dim Sum Restaurant', 'Ferry', 'Toy / Game Store', 'Bowling Alley', 'Train Station', 'Winery', 'Distillery', 'College Theater', 'Music School', 'Burger Joint', 'Taco Place', 'Financial or Legal Service', 'Café',
    'Middle School', 'Law School', 'Swiss Restaurant', 'Community College', 'Beer Garden', 'Food Truck', 'Ice Cream Shop', 'Medical School', 'Bridal Shop', 'French Restaurant', 'Professional & Other Places', 'Mexican Restaurant', 'Smoke Shop', 'German Restaurant', 'Road', 'Housing Development', 'General Travel', 'Recycling Facility', 'Flea Market', 'Japanese Restaurant', 'Other Nightlife', 'Burrito Place', 'Pizza Place', 'Taxi', 'Bookstore', 'Hot Dog Joint', 'Newsstand', 'Hobby Shop', 'Market',
    'Hardware Store', 'Brazilian Restaurant', 'Post Office', 'Jewelry Store', 'Design Studio', 'Mediterranean Restaurant', 'Malaysian Restaurant', 'Light Rail', 'Australian Restaurant', 'Bike Rental / Bike Share', 'Filipino Restaurant', 'Internet Cafe', 'General College & University', 'Clothing Store', 'College Academic Building', 'Coffee Shop', 'Hotel', 'Indian Restaurant', 'Department Store', 'Salon / Barbershop',
    'Student Center', 'Deli / Bodega', 'Storage Facility', 'Greek Restaurant', 'Seafood Restaurant', 'Moroccan Restaurant', 'Mobile Phone Shop', 'Neighborhood', 'High School', 'Mac & Cheese Joint', 'Southern / Soul Food Restaurant', 'Gym / Fitness Center', 'Elementary School', 'Gaming Cafe', 'Turkish Restaurant', 'Bank', 'Bagel Shop', 'Arts & Crafts Store', 'BBQ Joint', 'Video Game Store', 'Candy Store', 'Nail Salon', 'Motorcycle Shop', 'School', 'Diner', 'Music Store', 'Tea Room', 'Sushi Restaurant', 'Gastropub', 'Breakfast Spot',
    'College & University', 'Bus Station', 'Casino', 'Nightlife Spot', 'Nursery School', 'Italian Restaurant', 'Donut Shop', 'South American Restaurant', 'Scandinavian Restaurant', 'Sorority House', 'Bike Shop', 'Ramen /  Noodle House', 'Animal Shelter', 'Rental Car Location', 'Salad Place', 'Peruvian Restaurant', 'Medical Center', 'Cajun / Creole Restaurant', 'Cuban Restaurant', 'Gift Shop', 'African Restaurant', 'Restaurant', 'University', 'Vietnamese Restaurant', 'Fried Chicken Joint', 'Afghan Restaurant', 'Paper / Office Supplies Store', 'Automotive Shop',
    'Airport', 'Trade School', 'Laundry Service', 'Moving Target', 'Racetrack', 'Arepa Restaurant', 'Cosmetics Shop', 'College Stadium', 'Car Dealership', 'Middle Eastern Restaurant', 'Comedy Club', 'City', 'Thai Restaurant', 'Electronics Store', 'Vegetarian / Vegan Restaurant', 'Snack Place', 'Travel Lounge', 'Fish & Chips Shop', 'Residential Building (Apartment / Condo)', 'Playground', 'Molecular Gastronomy Restaurant', 'Gluten-free Restaurant', 'Military Base', 'Fast Food Restaurant', 'Dessert Shop', 'Office', 'Convenience Store', 'Camera Store', 'Cupcake Shop', 'Board Shop',
    'Food & Drink Shop', 'Tapas Restaurant', 'Dumpling Restaurant', 'Subway', 'Funeral Home', 'Miscellaneous Shop', 'Soup Place', 'Fraternity House', 'Pet Service', 'Wings Joint', 'Home (private)', 'Food', 'Tattoo Parlor', 'Pet Store', 'Falafel Restaurant', 'Shop & Service', 'Flower Shop',
    'Spanish Restaurant', 'Steakhouse', 'Photography Lab', 'Caribbean Restaurant', 'Furniture / Home Store', 'Garden Center', 'Travel & Transport', 'Sandwich Place']

    touristVenueCategoryNames:List = ['Castle', 'Arcade', 'Pool', 'Public Art', 'Museum', 'Harbor / Marina', 'Zoo', 'Outdoors & Recreation', 'General Entertainment', 'Other Great Outdoors', 'River', 'Aquarium', 'Plaza', 'Library', 'Art Museum', 'Beach', 'Synagogue', 'Spa / Massage', 'Theater', 'Concert Hall', 'Event Space', 'Temple', 'Church', 'Garden', 'Performing Arts Venue', 'Shrine', 'Historic Site', 'Convention Center', 'Brewery', 'History Museum', 'Cemetery', 'Science Museum', 'Park', 'Scenic Lookout', 'Mosque', 'Pool Hall', 'Art Gallery', 'Building', 'Arts & Entertainment', 'Planetarium', 'Movie Theater', 'Campground', 'Sculpture Garden', 'Bridge']

    datasetTourDF:DataFrame = datasetDF.loc[datasetDF['VenueCategoryName'].isin(touristVenueCategoryNames)]
    #datasetTourDF = datasetDF

    userIDsWithDup:List = datasetTourDF["UserID"].values
    venueIDsWithDup:List = datasetTourDF["VenueID"].values
    venueCategoryIDsWithDup:List = datasetTourDF["VenueCategoryID"].values

    userIDs:List = sorted(list(set(userIDsWithDup)))

    venueIDs:List[str] = sorted(list(set(venueIDsWithDup)))
    venueIDToString:List = [(venueIDIndex, venueIDs[venueIDIndex]) for venueIDIndex in range(len(venueIDs))]
    venueStringToID:dict = [(strI,idI) for idI,strI in venueIDToString]

    venueIDToStringDict:dict = dict(venueIDToString)
    venueStringToIDDict:dict = dict(venueStringToID)


    venueCategoryIDs:List[str] = sorted(list(set(venueCategoryIDsWithDup)))
    venueCategoryIDToString:List = [(venueIDIndex, venueCategoryIDs[venueIDIndex]) for venueIDIndex in range(len(venueCategoryIDs))]
    venueCategoryStringToID:dict = [(strI,idI) for idI,strI in venueCategoryIDToString]

    venueCategoryIDToStringDict:dict = dict(venueCategoryIDToString)
    venueCategoryStringToIDDict:dict = dict(venueCategoryStringToID)


    print("len:              " + str(len(datasetTourDF)))
    print("userIDs:            " + str(len(userIDs)))
    print("venueIDs:          " + str(len(venueIDs)))
    print("venueCategoryIDs:    " + str(len(venueCategoryIDs)))
    print("")

    datasetTransfDF = datasetTourDF.copy()
    datasetTransfDF["VenueID"] = datasetTransfDF.apply(lambda row: venueStringToIDDict[row["VenueID"]], axis=1)
    datasetTransfDF["VenueCategoryID"] = datasetTransfDF.apply(lambda row: venueCategoryStringToIDDict[row["VenueCategoryID"]], axis=1)

    #print(datasetTransfDF.head().to_string())
    return datasetTransfDF

def transformDataset(datasetDF:DataFrame):
    ratingsDF:DataFrame = datasetDF.groupby(["UserID", "VenueID"], as_index=False).size()
    itemsDF:DataFrame = datasetDF[["VenueID", "VenueCategoryID", "VenueCategoryName", "Latitude", "Longitude"]].copy()
    itemsDF = itemsDF.drop_duplicates(subset="VenueID", keep="last")

    return ratingsDF, itemsDF

def getDistances(itemsDF:DataFrame):
    print("")
    distancesDF:DataFrame = pd.DataFrame(0, index=np.arange(len(itemsDF.index)), columns=np.arange(len(itemsDF.index)))
    for indexI in range(len(itemsDF.index)):
        print("Counted: " + str(indexI) + " / " + str(len(itemsDF.index)))
        for indexJ in range(len(itemsDF.index)):
            itemID1, itemID2 = indexI, indexJ
            distancesDF.loc[indexI,indexJ] = _getItemIDDistance(itemsDF, itemID1, itemID2)
            distancesDF.loc[indexJ, indexI] = distancesDF.loc[indexI,indexJ]
    print(distancesDF.head())
    return distancesDF


def _getDistance(latitude1, longitude1, latitude2, longitude2):
    import geopy.distance
    return geopy.distance.geodesic((latitude1, longitude1), (latitude2, longitude2)).km

def _getGPS(itemsDF:DataFrame, itemID):
    #print("itemID: " + str(itemID))
    #print(itemsDF.head().to_string())
    row = itemsDF.loc[itemsDF["VenueID"] == itemID].iloc[0]
    return (row["Latitude"], row["Longitude"])

def _getVenueCategoryName(itemsDF:DataFrame):
    categoryNames:List = list(set(itemsDF["VenueCategoryName"]))
    return categoryNames

def _getItemIDDistance(itemsDF:DataFrame, itemID1, itemID2):
    latitude1, longitude1 = _getGPS(itemsDF, itemID1)
    latitude2, longitude2 = _getGPS(itemsDF, itemID2)
    return _getDistance(latitude1, longitude1, latitude2, longitude2)

#############################################################################################################

def readDatasetNYC():
    #print(os.getcwd())
    #from pathlib import Path
    #Path('frantajede.txt').touch()
    ratingsDF:DataFrame = pd.read_csv('data/dataset_tsmc2014/ratingsNYC.txt', index_col=0)
    itemsDF:DataFrame = pd.read_csv('data/dataset_tsmc2014/itemsNYC.txt', index_col=0)
    distancesDF:DataFrame = pd.read_csv('data/dataset_tsmc2014/distancesNYC.txt', index_col=0)
    distancesDF.index = [int(keyI) for keyI in distancesDF.keys()]
    distancesDF.columns = [int(columnI) for columnI in distancesDF.columns]

    return (ratingsDF, itemsDF, distancesDF)

def readDatasetTKY():
    ratingsDF:DataFrame = pd.read_csv('data/dataset_tsmc2014/ratingsTKY.txt', index_col=0)
    itemsDF:DataFrame = pd.read_csv('data/dataset_tsmc2014/itemsTKY.txt', index_col=0)
    distancesDF:DataFrame = pd.read_csv('data/dataset_tsmc2014/distancesTKY.txt', index_col=0)
    distancesDF.index = [int(keyI) for keyI in distancesDF.keys()]
    distancesDF.columns = [int(columnI) for columnI in distancesDF.columns]

    return (ratingsDF, itemsDF, distancesDF)


def getVisitedPlacesOfUser(userID:int, ratingsDF:DataFrame, itemsDF:DataFrame):
    rowsOfUserDF = ratingsDF[ratingsDF["UserID"] == userID]
    venueIDs:List = list(rowsOfUserDF["VenueID"])

    venueCategoryNames:List = []
    gpss:List = []
    for venueIdI in venueIDs:
        rowsI:Series = itemsDF.loc[itemsDF["VenueID"] == venueIdI]
        venueCategoryName = rowsI["VenueCategoryName"].values[0]
        latitude = rowsI["Latitude"].values[0]
        longitude = rowsI["Longitude"].values[0]
#        print("venueCategoryName: " + str(venueCategoryName))
#        print("latitude: " + str(latitude))
#        print("longitude: " + str(longitude))
        venueCategoryNames.append(venueCategoryName)
        gpss.append((latitude,longitude))

#    print(venueIDs)
#    print(itemsDF.head(10))
    print("gpss: " + str(gpss))

    return venueIDs, venueCategoryNames, gpss


def divideTrainTest(ratingsDF:DataFrame, procents:int):

    trainDFs:List = []
    testDFs:List = []
    userIds:List = list(set(ratingsDF['UserID'].values))
    for userIdI in userIds:
        raitingsOfUserI = ratingsDF[ratingsDF['UserID'] == userIdI]
        borderI = int(len(raitingsOfUserI)*(procents/100))
        if borderI == 0:
            borderI += 1
        trainRaitingsDFI = raitingsOfUserI[0:borderI]
        testRaitingsDFI = raitingsOfUserI[borderI:]

        trainDFs.append(trainRaitingsDFI)
        testDFs.append(testRaitingsDFI)

    trainDF = pd.concat(trainDFs, axis=0)
    testDF = pd.concat(testDFs, axis=0)

    return trainDF, testDF


def getNearestNeighbors(distancesDF:DataFrame, nearestNeighborsCount:int):

    nearestNeighborsOfItemIdsDict:dict[int,Series] = {}
    itemIds: List = [itemIdsI for itemIdsI in distancesDF.keys()]
    for itemIdI in itemIds:
        rowSerI:Series = distancesDF.iloc[itemIdI,:]
        rowSortedSerI:Series = rowSerI.sort_values(inplace=False)
        rowSortedSerI.drop(itemIdI, inplace=True)
        nearestNeighborsOfItemIdsDict[itemIdI] = rowSortedSerI.head(nearestNeighborsCount)

    return nearestNeighborsOfItemIdsDict