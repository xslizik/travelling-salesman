import time
import copy
from genetic import GeneticOptions, analyseGenetic, initPopulation, newGeneration
from shared import Individual, draw, generateRandomPath, initBase
from tabu import analyseClimber, getNeighbours  

LAST_YEAR_POSITIONS = "./positions/thisYearPositions.txt"

def testCompareGenetic(): 
    population_size = 100
    generations_num = 1000
    base = initBase(LAST_YEAR_POSITIONS)
    options = GeneticOptions(True, False, True, 10, 0)
    top_elites = []

    first_population = initPopulation(base[0],base[1], population_size) 
    print(f"Tournament and Roulette Comparison\nPopulation size {population_size}, Number of generations {generations_num}, Elites 10, Mutate Yes\n")   

    for i in range(2):
        print("Roulette") if i+2 % 2 else print("Tournament")
        
        current_population = first_population 
        best_first_individual = copy.deepcopy(current_population[0])
        
        start_time = time.time()
        for _ in range (0, generations_num):
            top_elites.append(current_population[0].fitness)
            current_population = newGeneration(base[0], base[1], current_population, options) 
            if best_first_individual.fitness < current_population[0].fitness:
                best_first_individual = copy.deepcopy(current_population[0])
        end_time = time.time()

        print(f"Time {end_time - start_time}s")
        print(f"Distance {1/best_first_individual.fitness}")
        draw(base[0], best_first_individual.path)
        options = GeneticOptions(False, True, True, 10, 0)
    
    analyseGenetic(top_elites, generations_num)

def testGenetic(file, population_size, generations_num, options):
    base = initBase(file)
    top_elites = []

    current_population = initPopulation(base[0], base[1], population_size) 
    best_first_individual = copy.deepcopy(current_population[0])

    start_time = time.time()
    for _ in range (0, generations_num):
        top_elites.append(current_population[0].fitness)
        current_population = newGeneration(base[0], base[1], current_population, options) 
        if best_first_individual.fitness < current_population[0].fitness:
            best_first_individual = copy.deepcopy(current_population[0])
    end_time = time.time()

    print(f"Time {end_time - start_time}s")
    print(f"Distance {1/best_first_individual.fitness}")
    draw(base[0], best_first_individual.path)
    analyseGenetic(top_elites, generations_num)

def testCompareTabu():
    base = initBase(LAST_YEAR_POSITIONS)
    initial_path = generateRandomPath(len(base[0]))
    climbs = 250
    tabu_lenght = 5
    climbed_fitness = []
    best_fitness = []

    print(f"Tabu Search with different list lenghts comparison\nNumber of climbs {climbs}\n")   

    for i in range (2):
        print(f"Tabu Length {tabu_lenght}") if i+2 % 2 else print(f"Tabu Length {tabu_lenght}")
        current = Individual(base[0], base[1], initial_path)
        best = current
        tabu = []

        start_time = time.time()
        for _ in range(0, climbs):
            neighbours = getNeighbours(base[0], base[1], current)
            for candidate in neighbours:
                if str(candidate.path) not in tabu:
                    if candidate.fitness < current.fitness:
                        if len(tabu) > tabu_lenght:
                            tabu = tabu[1:]
                        tabu.append(str(current.path)) 
                    current = candidate
                    break
            
            if current.fitness > best.fitness:
                best = current
            
            climbed_fitness.append(current.fitness)
            best_fitness.append(best.fitness)
        end_time = time.time()
        
        print(f"Time {end_time - start_time}s")
        print(f"Distance {1/best.fitness}")
        draw(base[0], best.path)
        tabu_lenght = 100
    analyseClimber(climbed_fitness, best_fitness, climbs)

def testTabu(climbs, tabu_length):
    base = initBase(None)
    
    current = Individual(base[0], base[1], generateRandomPath(len(base[0])))
    best = current
    tabu = []
    
    climbed_fitness = []
    best_fitness = []

    start_time = time.time()
    for _ in range(0,climbs):
        neighbours = getNeighbours(base[0], base[1], current)
        for candidate in neighbours:
            if str(candidate.path) not in tabu:
                if candidate.fitness < current.fitness:
                    if len(tabu) > tabu_length:
                        tabu = tabu[1:]
                    tabu.append(str(current.path)) 
                current = candidate
                break
        
        if current.fitness > best.fitness:
            best = current
        
        climbed_fitness.append(current.fitness)
        best_fitness.append(best.fitness)
    end_time = time.time()

    print(f"Time {end_time - start_time}s")
    print(f"Distance {1/best.fitness}")
    draw(base[0], best.path)
    analyseClimber(climbed_fitness, best_fitness, climbs)