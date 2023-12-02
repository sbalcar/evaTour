import os

import numpy as np
from pandas import DataFrame
from python_tsp.exact import solve_tsp_dynamic_programming
from python_tsp.heuristics import solve_tsp_local_search

from evaTour.datasets.datasetFoursquare import readDatasetNYC
from evaTour.maps.openStreetMaps import showRouteMaps


def test01():
    print("test01")

    distance_matrix = np.array([
        [0,  5, 4, 10],
        [5,  0, 8,  5],
        [4,  8, 0,  3],
        [10, 5, 3,  0]
    ])
    # https://github.com/fillipe-gsm/python-tsp
    permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
    permutation, distance = solve_tsp_local_search(distance_matrix)

    print(permutation)
    print(distance)

def test02():
    print("test02")

    ratingsDF:DataFrame
    itemsDF:DataFrame
    distancesDF: DataFrame
    ratingsNYcDF, itemsNYcDF, distancesNYcDF = readDatasetNYC()

    individual = range(1,100)
    #individual = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]

    # select rows and columns with index positions
    distancesSelDF = distancesNYcDF.iloc[individual, individual]
    distance_matrix = distancesSelDF.to_numpy()

#    permutationOfIndexes, distance = solve_tsp_local_search(distance_matrix)
    permutationOfIndexes, distance = solve_tsp_local_search(distance_matrix)

    # use numpy.take() to retrieve elements
    # from input list at given indices
    permutation = np.take(individual, permutationOfIndexes)

    showRouteMaps([permutation], itemsNYcDF)


if __name__ == "__main__":
    os.chdir('../../../')
#    test01()
    test02()