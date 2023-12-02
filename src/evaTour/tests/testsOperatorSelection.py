from evaTour.ea.operators.selectionGeneral.selectionTournament import SelectionTournament
from evaTour.ea.operators.selectionGeneral.selectionRoulette import SelectionRoulette

import os


def test01():
    print("test01")

    pop = ["a", "b", "c", "d", "e", "f"]
    fitnessValues = [1,1,1,1,50,50]
    countOfSelectedItem = 3
    k = 3

    sel = SelectionTournament(k).run(pop, fitnessValues, countOfSelectedItem)
    print("sel: " + str(sel))

def test02():
    print("test02")

    pop1 = [0,1,2,3,4,5,6]
    weights1 = [1,2,6,4,3,7,20]
    item = SelectionRoulette(True).run(pop1,weights1,1)
    print("pop1: " + str(pop1))
    print("weights1: " + str(weights1))
    print("item1: " + str(item))
    print("")

    pop2 = [0,1,2,3,4,5,6]
    weights2 = [1,2,2,2,2,2,2]
    index2 = SelectionRoulette(False).run(pop2,weights2,1)
    print("pop2: " + str(pop2))
    print("weights2: " + str(weights2))
    print("index2: " + str(index2))
    print("")

    countOfSelectedItem = 10
    pop3 = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
            "k", "l", "m", "n", "o", "p", "q", "r", "s", "t"]
    fitnessValues3 = [1,1,1,1,1, 1,1,1,1,1 ,1,1,1,1,1, 1,1,1,50,50]
    sel3 = SelectionRoulette(False).run(pop3, fitnessValues3, countOfSelectedItem)
    print("pop: " + str(pop3))
    print("fit: " + str(fitnessValues3))
    print("sel3: " + str(sel3))



if __name__ == "__main__":
    os.chdir('../../../')
    #test01()
    test02()
