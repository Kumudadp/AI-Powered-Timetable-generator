import random

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# Fitness function to evaluate timetable
def fitness(timetable, teachers, time_slots):
    score = 0

    # Example constraints
    used_slots = set()
    for day, slots in timetable.items():
        for slot, session in slots.items():
            if session:
                teacher = session.split("-")[1]
                # Avoid duplicate usage of teachers or timeslots
                if (teacher, slot) in used_slots:
                    score -= 1
                else:
                    score += 1
                    used_slots.add((teacher, slot))
    return score


# Generate initial random population
def initialize_population(teachers, subjects, time_slots, population_size=10):
    population = []
    for _ in range(population_size):
        timetable = {day: {slot: None for slot in time_slots} for day in DAYS}

        for day in DAYS:
            for slot in time_slots:
                subject = random.choice(subjects)
                teacher = random.choice(teachers)
                timetable[day][slot] = f"{subject}-{teacher}"

        population.append(timetable)
    return population


# Crossover: Combine two timetables
def crossover(parent1, parent2):
    child = {day: {} for day in DAYS}
    for day in DAYS:
        for i, slot in enumerate(parent1[day]):
            if i % 2 == 0:
                child[day][slot] = parent1[day][slot]
            else:
                child[day][slot] = parent2[day][slot]
    return child


# Mutation: Randomly modify a timetable
def mutate(timetable, teachers, subjects, time_slots, mutation_rate=0.1):
    for day in DAYS:
        for slot in time_slots:
            if random.random() < mutation_rate:
                subject = random.choice(subjects)
                teacher = random.choice(teachers)
                timetable[day][slot] = f"{subject}-{teacher}"
    return timetable


# Genetic Algorithm to optimize timetable
def genetic_algorithm(teachers, subjects, time_slots, generations=50, population_size=10):
    population = initialize_population(teachers, subjects, time_slots, population_size)

    for generation in range(generations):
        # Evaluate fitness
        population = sorted(population, key=lambda t: fitness(t, teachers, time_slots), reverse=True)

        # Select top individuals
        new_population = population[:2]  # Elitism: Keep best 2

        # Crossover and mutation
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:5], 2)
            child = crossover(parent1, parent2)
            child = mutate(child, teachers, subjects, time_slots)
            new_population.append(child)

        population = new_population

    # Return best timetable
    return max(population, key=lambda t: fitness(t, teachers, time_slots))
