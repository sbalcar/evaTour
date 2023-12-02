from scipy.spatial.distance import hamming

from evaTour.ea.toolDiversity import countMatrixOfMinOfHammingDistances, printMatrix

import os


def test01():
    print("test01")

    perm1 = [0,1,2,3,4]
    perm2 = [0,1,3,2,4]
    a = hamming(perm1, perm2)
    print("Result:" + str(a))  # 0.4
    print()

    perm1 = [0,10,20,30,40]
    perm2 = [0,10,30,20,40]
    a = hamming(perm1, perm2)
    print("Result:" + str(a))  # 0.4
    print()

    perm1 = [0,1,2,3,4,5,6,7,8,90]
    perm2 = [9,8,7,6,5,4,3,2,1,0]
    a =     [9,7,5,3,1,1,3,5,7,9]   # (n-1)*n/2
    a = hamming(perm1, perm2)
    print("Result:" + str(a))  # 0.4

def test02():
    print("test02")

    perm1 = [0,1,2,3,4,5,6,7,8,9]
    perm2 = [9,8,7,6,5,4,3,2,1,0]
    perm3 = [8,9,7,6,5,4,3,2,1,0]

    matrix = countMatrixOfMinOfHammingDistances([perm1, perm2, perm3], False)
    #matrix = _countMinOfHammingDistances(perm1, perm2, True)
    #print("Result:" + str(matrix))
    printMatrix(matrix)


if __name__ == "__main__":
    os.chdir('../../../')
    #test01()
    test02()