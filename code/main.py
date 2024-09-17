from genetic import GeneticOptions
from tests import testTabu, testGenetic, testCompareGenetic, testCompareTabu

def choice(question) -> bool:
    while True:
        print(question)
        console = input()
        match console:
            case 'y':
                return True
            case 'n':
                return False

def crossingChoice() -> bool:
    while True:
        print("Tournament or Roulette t\\r ?")
        console = input()
        match console:
            case 't':
                return True
            case 'r':
                return False

def numberInput(question, low_bound):
    num = -1
    while num < low_bound:
        while True:
            try:
                num = input(question)
                num = int(num)
                break
            except ValueError:
                print("invalid input")
    return num

def geneticDefaultChoice(tournament, mutate):
    population_size = numberInput("population size: ", 1)
    generations_num = numberInput("number of generations: ", 1)
    elites = randoms = population_size
    while elites + randoms > population_size:
        elites = numberInput("(elites + randoms have to be less than population size)\nnumber of elites: ", 0)
        randoms = numberInput("number of randoms: ", 0)

    options = GeneticOptions(True, False, mutate, elites, randoms) if tournament else GeneticOptions(False, True, mutate, elites, randoms)
    testGenetic(None, population_size, generations_num, options)

def tabuDefaultChoice():
    climbs = numberInput("number of climbs: ", 1)
    tabu_size = numberInput("tabu list size: ", 1)
    testTabu(climbs, tabu_size)

def main():
    print("Artificial Intelligence 2022 Slizik Jan\nAssignment 2: Travelling salesman problem")
    while True:
        print("\nSelect option:\
        \n\t(1) Random positions [genetic algorithm]\
        \n\t(2) Genetic Algorithm Crossing Comparison\
        \n\t(3) Random positions [tabu search]\
        \n\t(4) Tabu Search List Lenght Comparison\
        \n\tPress -x- to exit\n");        
        
        selection = input()
        match selection:
            case '1':
                mutate = choice("Mutate y\\n ?")
                tournament = crossingChoice()
                if choice("Do you wish to change basic options y\\n ?\nIndividuals in a population 100, Number of generations 1000, Elites 10, Randoms 0"):
                    geneticDefaultChoice(tournament, mutate)
                else:
                    options = GeneticOptions(True, False, mutate, 10, 1) if tournament else GeneticOptions(False, True, mutate, 10, 1)
                    testGenetic(None, 100, 1000, options)
            case '2':
                testCompareGenetic()
            case '3':
                if choice("Do you wish to change basic options y\\n ?\nNumber of climbs 250, Tabu list size 50"):
                    tabuDefaultChoice()
                else:
                    testTabu(250, 50)
            case '4':
                testCompareTabu()
            case 'x':
                print("Exiting..")
                break
            case _:
                print("You have selected wrong option try again.")

if __name__ == "__main__":
    main()