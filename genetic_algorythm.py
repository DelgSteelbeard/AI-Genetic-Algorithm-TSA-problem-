import random
import math

# Function to calculate a distance between 2 points it take into account the curvature of the earth
# the "111" is the approximation of 1 degree of latitude in kilometers
def calculate_distance(x1, y1, x2, y2):
    try:
        width_differance = (x2 - x1) * 111
        length_differance = (y2 - y1) * (111 * math.cos(math.radians(x1)))

        return math.sqrt(width_differance ** 2 + length_differance ** 2)

    except Exception as e:
        print(f"Distance calculation error: {e}")

# Generates a distance-based cost array for pairs of clients using their coordinates
def generate_cost_array(clients):
    cost_array = {}

    try:
        for client_1 in clients.values():
            cost_array[client_1.id] = {}
            for client_2 in clients.values():
                if client_1 != client_2:
                    cost = calculate_distance(client_1.coordinate_x, client_1.coordinate_y,
                                              client_2.coordinate_x, client_2.coordinate_y)
                    cost_array[client_1.id][client_2.id] = cost

    except Exception as e:
        print(f"Cost array generation error: {e}")

    return cost_array

# Generates a population of individuals with chromosomes obtained by randomly permuting the input array
def encode_genotype(array, population_size):
    starting_population = []
    for _ in range(population_size):
        chromosome = random.sample(array, len(array))
        starting_population.append(chromosome)
    return starting_population

# Calculates the total cost of a given route based on the cost_array
def cost_sum(route, cost_array):
    cost = 0
    try:
        for iterator in range(len(route)-1):
            client_current = route[iterator]
            client_next = route[iterator+1]
            cost += cost_array[client_current][client_next]

    except KeyError as e:
        print(f"Error: missing key {e} of the cost array!")
    except Exception as e:
        print(f"Sum cost Error: {e}")

    return cost

# Performs tournament selection on a given population based on grade scores.
def tournament_selection(population, grade_score, tournament_size):
    new_population = []
    for _ in range(len(population)):
        tournament = random.sample(list(enumerate(grade_score)), tournament_size)
        tournament_winner = min(tournament, key=lambda x: x[1])[0]
        new_population.append(population[tournament_winner])
    return new_population

# Performs single-point crossover between two parents to create two children.
def single_point_crossing(parent_1, parent_2):
    split_point = random.randint(0, len(parent_1) - 1)
    child_1 = parent_1[:split_point] + [gen for gen in parent_2 if gen not in parent_1[:split_point]]
    child_2 = parent_2[:split_point] + [gen for gen in parent_1 if gen not in parent_2[:split_point]]
    return child_1, child_2

# Applies city change mutation to a chromosome with a given probability
# If the mutation occurs, two random indices are selected, and the cities at those positions are swapped.
def city_change_mutation(chromosome, mutation_probability):
    if random.random() < mutation_probability:
        index_1, index_2 = random.sample(range(len(chromosome)), 2)
        chromosome[index_1], chromosome[index_2] = chromosome[index_2], chromosome[index_1]
    return chromosome


