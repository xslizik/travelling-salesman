import matplotlib.pyplot as plt

from shared import Individual

# analyse result
def analyseClimber(climbed_fitness, best_fitness, climbs):
    fig, ax = plt.subplots()
    plt.get_current_fig_manager().set_window_title('Tabu search metaheuristic analysis')
    if len(climbed_fitness) > climbs: 
        length_climbed = int(len(climbed_fitness)/2)
        first_climbed = climbed_fitness[:length_climbed]
        second_climbed = climbed_fitness[length_climbed:]

        length_best = int(len(best_fitness)/2)
        first_best = best_fitness[:length_best]
        second_best = best_fitness[length_best:]

        ax.plot(first_climbed, label='5 tabu fitness')
        ax.plot(first_best, label='5 tabu best')
        ax.plot(second_climbed, label='100 tabu fitness')
        ax.plot(second_best, label='100 tabu best')
    else:
        ax.plot(climbed_fitness, label='fitness')
        ax.plot(best_fitness, label='best')
    
    ax.legend()
    ax.set(xlabel='climb', ylabel='fitness',
        title='graph of climbed fitness')
    ax.grid()
    plt.show()

# climber functions
def swap(path, first_index, second_index):
    new_path = path.copy()
    tmp = new_path[first_index]
    new_path[first_index] = new_path[second_index]
    new_path[second_index] = tmp
    
    return new_path

def getNeighbours(points, distances, current : Individual) -> list:
    neighbours = []
    lenght = len(current.path)
    for i in range (0, lenght):
        if i != lenght - 1:
            for j in range(i+1, lenght):
                neighbours.append(Individual(points, distances, swap(current.path, i, j)))
    
    return sorted(neighbours, key=lambda x: x.fitness, reverse=True)