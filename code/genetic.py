import random
import matplotlib.pyplot as plt

from shared import Individual, generateRandomPath

class GeneticOptions:
    def __init__(self, tournament, roulette, mutate, elites, randoms):
        self.tournament = tournament
        self.roulette = roulette
        self.mutate = mutate
        self.elites = elites
        self.randoms = randoms

# analyse result
def analyseGenetic(top_elites, generations_num):
    fig, ax = plt.subplots()
    plt.get_current_fig_manager().set_window_title('Genetic metaheuristic analysis')
    if len(top_elites) > generations_num: 
        length = int(len(top_elites)/2)
        tournament = top_elites[:length]
        roulette = top_elites[length:]
        ax.plot(tournament, label='tournament')
        ax.plot(roulette, label='roulette')
    else:
        ax.plot(top_elites, label='elites')        

    ax.legend()
    ax.set(xlabel='generations', ylabel='fitness',
        title='graph of elites over generations')
    ax.grid()
    plt.show()

# init
def initPopulation(points, distances, size) -> list:
    population = []
    for _ in range(0, size):
        individual = Individual(points, distances, generateRandomPath(len(points)))
        population.append(individual)

    return sorted(population, key=lambda x: x.fitness, reverse=True)

# generate new generations
def crossover(first_parent, second_parent) -> list:
    length = len(first_parent)
    child_path = []

    rand_a = int(random.random() * length)
    rand_b = int(random.random() * length)

    for i in range(min(rand_a, rand_b), max(rand_a, rand_b)):
        child_path.append(first_parent[i])

    ending = [point_index for point_index in second_parent if point_index not in child_path]
    return child_path + ending

def getParentTournament(previous_population) -> Individual:
    tournament = random.sample(previous_population, round(len(previous_population)*0.1))
    return max(tournament, key=lambda x: x.fitness).path

def getParentRoulette(previous_population, sum_previous) -> Individual:
    pick = random.uniform(0, sum_previous)
    sum_fitness = 0
    for individual in previous_population:
        sum_fitness += individual.fitness
        if sum_fitness > pick:
            return individual.path

def mutate(path) -> list:
    if random.random() <= 0.1:
        path_length = len(path)
        mutate_index = random.randint(1, path_length - 1)
        if mutate_index != path_length - 1:
            tmp = path[mutate_index]
            path[mutate_index] = path[mutate_index + 1]
            path[mutate_index + 1] = tmp
        else:
            tmp = path[-1]
            path[-1] = path[0]
            path[0] = tmp
    return path

def appendChildren(points, distances, previous_population, amount, options:GeneticOptions) -> list:
    new_population = []
    if options.roulette:
        sum_previous = sum(chromosome.fitness for chromosome in previous_population)

    for _ in range(0, amount):
        if options.tournament:
            child_path = crossover(getParentTournament(previous_population), getParentTournament(previous_population))
        elif options.roulette:
            child_path = crossover(getParentRoulette(previous_population, sum_previous), getParentRoulette(previous_population, sum_previous))
        if options.mutate:
            child_path = mutate(child_path)
        new_population.append(Individual(points, distances, child_path))
    return new_population

def newGeneration(points, distances, previous_population, options) -> list:
    length_path = len(points)
    new_population = []
    
    new_population += appendChildren(points, distances, previous_population, len(previous_population) - options.elites - options.randoms, options)

    for i in range(0, options.elites):
        previous_population[i].path = mutate(previous_population[i].path)
        new_population.append(previous_population[i])

    for i in range(0, options.randoms):
        new_population.append(Individual(points,distances, generateRandomPath(length_path)))

    return sorted(new_population, key=lambda x: x.fitness, reverse=True)