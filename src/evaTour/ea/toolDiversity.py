from typing import List


def countAVGIntersectionsWithIndiv(populationOfIndiv:List, indiv, DEBUG=False):
    intersectionCounter:float = 0
    for popIndivI in populationOfIndiv:
        intersectionI = len(list(set(popIndivI) & set(indiv)))
        AVGlen = (len(popIndivI) + len(indiv)) / 2
        intersectionCounter += intersectionI / AVGlen
    return intersectionCounter / len(populationOfIndiv)

def countMatrixOfIntersections(populationOfIndiv:List):

    rows, cols = (len(populationOfIndiv), len(populationOfIndiv))
    matrix = [list([0] * cols) for _ in range(rows)]
    for rIndexI in range(rows):
        for cIndexJ in range(cols):
            matrix[rIndexI][cIndexJ] = len(
                list(set(populationOfIndiv[rIndexI]) & set(populationOfIndiv[cIndexJ])))

    return matrix

def countAVGMinHammingDistanceFromIndiv(populationOfIndiv:List, indiv, DEBUG=False):
    hammingDistanceCounter = 0
    for popIndivI in populationOfIndiv:
        intersectionOfPerm1I = [value for value in popIndivI if value in indiv]
        intersectionOfPerm2I = [value for value in indiv if value in popIndivI]
        distance1I = _countMinOfHammingDistances(intersectionOfPerm1I, intersectionOfPerm2I, DEBUG)
        revIntersectionOfPerm2I = list(intersectionOfPerm2I)
        revIntersectionOfPerm2I.reverse()
        distance2I = _countMinOfHammingDistances(intersectionOfPerm1I, revIntersectionOfPerm2I, DEBUG)
        hammingDistanceCounter += min(distance1I, distance2I)
    return hammingDistanceCounter / len(populationOfIndiv)

def countMatrixOfMinOfHammingDistances(populationOfIndiv:List, DEBUG=False):

    rows, cols = (len(populationOfIndiv), len(populationOfIndiv))
    matrix = [list([0] * cols) for _ in range(rows)]
    for rIndexI in range(rows):
        for cIndexJ in range(cols):
            permI:List = populationOfIndiv[rIndexI]
            permJ:List = populationOfIndiv[cIndexJ]
            intersectionOfPermI = [value for value in permI if value in permJ]
            intersectionOfPermJ = [value for value in permJ if value in permI]
            distance1I = _countMinOfHammingDistances(intersectionOfPermI, intersectionOfPermJ, DEBUG)
            revIntersectionOfPermJ = list(intersectionOfPermJ)
            revIntersectionOfPermJ.reverse()
            distance2I = _countMinOfHammingDistances(intersectionOfPermI, revIntersectionOfPermJ, DEBUG)
            matrix[rIndexI][cIndexJ] = min(distance1I, distance2I)

    return matrix

def _countMinOfHammingDistances(inputPerm1:List, inputPerm2:List, DEBUG=False):
    if set(inputPerm1) != set(inputPerm2):
        raise Exception("Two permutaions " + str(inputPerm1) + " "  + str(inputPerm2) + "are not basen on the same set")

    perTranslatorDict = dict(zip(inputPerm1, range(len(inputPerm1))))
    perm1 = [perTranslatorDict[vI] for vI in inputPerm1]
    perm2 = [perTranslatorDict[vI] for vI in inputPerm2]

    distances:List[int] = []
    for i in range(0, len(perm1)-1):
        beginPartOfPermI:List = perm1[:i]
        endPartOfPermI:List = perm1[i:]
        perm1NewI = endPartOfPermI + beginPartOfPermI

        sumOfDifferenceI = sum([abs(v1I - v2I) for v1I, v2I in zip(perm1NewI, perm2)])
        maxValue = (len(perm1)) * len(perm1) / 2
        distanceI = float(sumOfDifferenceI) / maxValue
        if DEBUG:
            print("Perm1: " + str(perm1NewI))
            print("Perm2: " + str(perm2))
            print("Distance: " + str(distanceI))
            print("  sumOfDifferenceI: " + str(sumOfDifferenceI))
            print("  maxValue: " + str(maxValue))
        distances.append(distanceI)

    return min(distances)


def printMatrix(matrix:List[List]):
    for rowI in matrix:
        print(rowI)

#countMatrixOfPermDistances([])

#matrix = countMatrixOfMinOfHammingDistances([[0,1,2,3],[3,2,1,10]])
#matrix = _countMinOfHammingDistances([0,1,2,3],[0,1,2,3])
#print(matrix)