from random import Random


def evolutionary_circle(children, population_size=40, generations=8000, seed=2026):
    rng = Random(seed)
    n = len(children)
    distances = [[sum(a != b for a, b in zip(x, y)) for y in children] for x in children]

    def fitness(order):
        return sum(distances[order[i]][order[(i + 1) % n]] for i in range(n))

    def crossover(parent1, parent2):
        neighbors = {i: set() for i in range(n)}
        for parent in (parent1, parent2):
            for i, child in enumerate(parent):
                neighbors[child].update((parent[i - 1], parent[(i + 1) % n]))

        result = [0]
        unused = set(range(1, n))
        while unused:
            choices = neighbors[result[-1]] & unused or unused
            next_child = max(choices, key=lambda x: (distances[result[-1]][x], rng.random()))
            result.append(next_child)
            unused.remove(next_child)
        return result

    def mutate(order):
        start = rng.randrange(1, n)
        end = min(n, start + rng.randint(1, 3))
        block = order[start:end]
        rest = order[:start] + order[end:]
        at = rng.randrange(1, len(rest) + 1)
        return rest[:at] + block + rest[at:]

    population = [[0] + rng.sample(range(1, n), n - 1) for _ in range(population_size)]
    best = max(population, key=fitness)[:]

    for step in range(generations):
        parent1 = max(rng.sample(population, 3), key=fitness)
        parent2 = max(rng.sample(population, 3), key=fitness)
        child = crossover(parent1, parent2)
        if n > 2 and rng.random() < 0.7:
            child = mutate(child)

        worst = min(range(population_size), key=lambda i: fitness(population[i]))
        if fitness(child) > fitness(population[worst]):
            population[worst] = child
        if fitness(child) > fitness(best):
            best = child[:]
        if (step + 1) % 100 == 0:
            population[worst] = [0] + rng.sample(range(1, n), n - 1)

    return best, fitness(best)


rng = Random(42)
children = [[rng.choice((False, True)) for _ in range(20)] for _ in range(20)]
order, score = evolutionary_circle(children)
print('Best score:', score)
print('Arrangement:', ' -> '.join(str(i) for i in order + order[:1]))
