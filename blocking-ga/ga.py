import blocking


POPULATION = 24

# Create population
strategies = [blocking.Strategy.createRandomStrategy(i) for i in range(POPULATION)]



# Determine fitness
