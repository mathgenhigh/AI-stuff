import random 

# Datasets
items = [
    {'weight': 2, 'value': 3},
    {'weight': 3, 'value': 4},
    {'weight': 4, 'value': 5},
    {'weight': 5, 'value': 8},
    {'weight': 9, 'value': 10}
]

capacity = 15
population_size = 6
generations = 10
mutation_rate = 0.1

# Fitness function
def fitness(chromosome):
    total_weight = sum(gene * item['weight'] for gene, item in zip(chromosome, items))
    total_value = sum(gene * item['value'] for gene, item in zip(chromosome, items))
    if total_weight > capacity:
        return 0
    else:
        return total_value
    
# Generate initial population
def generate_population():
    return [[random.randint(0, 1) for _ in items] for _ in range(population_size)]

# Selection (Top 2)
def selection(pop, fitnesses):
    sorted_pop = [x for _, x in sorted(zip(fitnesses, pop), reverse=True)]
    return sorted_pop[:2]

# Crossover (single-point)
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent2[point:]
    return child1, child2

# Mutation
def mutate(chromosome):
    for i in range(len(chromosome)):
        if random.random() < mutation_rate:
            chromosome[i] = 1 - chromosome[i]
    return chromosome

# Run GA
population = generate_population()
for gen in range(generations):
    fitnesses = [fitness(chromo) for chromo in population]
    best_fit = max(fitnesses)
    print(f"Generation {gen + 1} best fitness: {best_fit}")

    # Selection
    parents = selection(population, fitnesses)

    # Crossover & Mutation
    new_population = []
    while len(new_population) < population_size:
        c1, c2 = crossover(parents[0], parents[-1])
        c1 = mutate(c1)
        c2 = mutate(c2)
        new_population.extend([c1, c2])
    population = new_population[:population_size]

# Show best solution
fitnesses = [fitness(chromo) for chromo in population]
best_idx = fitnesses.index(max(fitnesses))
best_chromosome = population[best_idx]
selected_items = [i + 1 for i, gene in enumerate(best_chromosome) if gene == 1]
print(f"\nBest solution: items {selected_items} with value {max(fitnesses)}")