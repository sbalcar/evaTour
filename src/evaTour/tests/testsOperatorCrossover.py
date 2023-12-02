from evaTour.ea.operators.clusters.crossover.crossoverCluUniform import CrossoverCluUniform
from evaTour.ea.operators.roundtrip.crossover.crossoverRtPMX import CrossoverRtPMX
from evaTour.ea.operators.roundtrip.crossover.crossoverRtOnePoint import CrossoverRtOnePoint

from typing import List
import os

def test01():
    crossRate = 0.99
    individual1 = [0,0,0,0]
    individual2 = [1,1,1,1]
    indivNew1, indivNew2 = CrossoverRtOnePoint(crossRate).run(individual1, individual2)

    print("indivNew1: " + str(indivNew1))
    print("indivNew2: " + str(indivNew2))

def test02():
    print("test06")

    #parent1:List = [1, 2, 3, 4, 5, 6, 7]
    #parent2:List = [7, 6, 5, 4, 3, 2, 1]
    parent1:List = [1, 4, 2, 8, 5, 7, 3, 6, 9]
    parent2:List = [7, 5, 3, 1, 9, 8, 6, 4, 2]
    crossRate:float = 1.0

    # Result for sliceIndex1 = 3, sliceIndex2 = 7
    # [7, 4, 2, 1, 9, 8, 6, 3, 5], [1, 9, 6, 8, 5, 7, 3, 4, 2]
    a = CrossoverRtPMX(crossRate).run(parent1, parent2)
    print(a)

def test03():
    crossRate = 0.99
    individual1 = [2530, 2345, 136, 41, 1166, 31, 4257, 4541, 103, 4021, 1294, 136, 993, 4358, 3053, 3664, 950, 17, 29, 2118]
    individual2 = [103, 2345, 136, 993, 136, 1294, 4021, 2530, 41, 733, 31, 1166, 168, 4358, 3053, 3664, 950, 17, 29, 2118]
    indivNew1, indivNew2 = CrossoverRtPMX(crossRate).run(individual1, individual2)

    print("indivNew1: " + str(indivNew1))
    print("indivNew2: " + str(indivNew2))

def test04():
    individual1 = dict({0:[2530, 2345, 136, 41], 1:[1166, 31, 4257, 4541, 103], 2:[4021, 1294, 136]})
    individual2 = dict({0:[103, 2345, 136, 993], 1:[136, 1294, 4021, 2530, 41], 2:[733, 31, 1166, 168]})
    indivNew1, indivNew2 = CrossoverCluUniform().run(individual1, individual2)

    print("indivNew1: " + str(indivNew1))
    print("indivNew2: " + str(indivNew2))



if __name__ == "__main__":
    os.chdir('../../../')
    #test01()
    #test02()
    #test03()
    test04()