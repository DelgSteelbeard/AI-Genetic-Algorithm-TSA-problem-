from genetic_algorythm import *
from classClient import Client
import csv
import random
import folium

# Genetic algorithm parameters
population_size = 2000
generation_count = 20

tournament_size = 8
crossover_count = 200
elite_count = 250

mutation_probability = 0.4

# Stop condition variables
count_of_generations_without_improvement = 50
generations_without_improvement = 0
previous_best = float('inf')

# Load clients' data from CSV
Clients = {}
with open('clientData.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for data_set in reader:
        new_client = Client()
        new_client.assing(','.join(data_set))
        Clients[new_client.id] = new_client

# Generate the cost array
cost_array = generate_cost_array(Clients)

# Initialize the population
population = encode_genotype(list(Clients.keys()), population_size)

# Main Genetic Algorithm Loop
for generation in range(generation_count):
    # Evaluate the fitness of the current population
    grade_score = [cost_sum(route, cost_array) for route in population]

    # Tournament Selection
    new_population = tournament_selection(population, grade_score, tournament_size)

    # Single-point crossover
    for _ in range(crossover_count):
        parent_1_index, parent_2_index = random.sample(range(len(new_population)), 2)
        parent_1, parent_2 = new_population[parent_1_index], new_population[parent_2_index]
        child_1, child_2 = single_point_crossing(parent_1, parent_2)
        new_population.extend([child_1, child_2])

    # Mutation
    for iterator in range(len(new_population)):
        new_population[iterator] = city_change_mutation(new_population[iterator], mutation_probability)

    # Evaluate the fitness of the new population
    new_population_score = [cost_sum(route, cost_array) for route in new_population]

    # Elitism
    score_indexes = range(len(new_population_score))
    sorted_indexes = sorted(score_indexes, key=lambda k: new_population_score[k])
    best_indexes = sorted_indexes[:elite_count]
    new_population = [new_population[index] for index in best_indexes]

    population = new_population

    # Check for improvement
    best_score = min(grade_score)
    if best_score >= previous_best:
        generations_without_improvement += 1
    else:
        generations_without_improvement = 0
    previous_best = best_score

    # Stop condition
    if generations_without_improvement >= count_of_generations_without_improvement:
        break

# Extract the best solution
best_solution = population[grade_score.index(min(grade_score))]

# Extract the coordinates of the first city in the best route
first_city = best_solution[0]
first_city_coordinates = [Clients[first_city].coordinate_x, Clients[first_city].coordinate_y]

# Calculate and display the cost of the best solution
best_solution_cost = cost_sum(best_solution, cost_array)

# Convert the solution IDs to city names for display
best_solution_names = [Clients[mark].name for mark in best_solution]

# Display the best route and the cost of that route
print("Best Route:", best_solution_names)
print("Best Route Cost:", best_solution_cost)

# Create a folium map centered around the first city in the best route
map = folium.Map(location=first_city_coordinates, zoom_start=10)
color = 'darkred'

# Add markers for all cities
for client_id, client in Clients.items():
    city = client.name
    coordinates = [client.coordinate_x, client.coordinate_y]
    folium.Marker(location=coordinates, popup=city, icon=folium.Icon(color=color)).add_to(map)

# Add polyline for the best route
for i in range(len(best_solution) - 1):
    start = best_solution[i]
    target = best_solution[i + 1]

    if start in Clients and target in Clients:
        start_coords = [Clients[start].coordinate_x, Clients[start].coordinate_y]
        target_coords = [Clients[target].coordinate_x, Clients[target].coordinate_y]

        folium.PolyLine(locations=[start_coords, target_coords], color=color).add_to(map)
    else:
        print(f"Error: Coordinates not found for cities {start} or {target}")

map.save("map.html")


