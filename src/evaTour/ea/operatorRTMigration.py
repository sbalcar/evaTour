import random

from numpy.random import randint


def migrationTabu(islandId, generationNumber, sharedDataStructure, bestIndiv):
    print("migration island " + str(islandId) + " generationNumber " + str(generationNumber))

    sharedDataStructure[islandId] = bestIndiv
