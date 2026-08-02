"""Shared demo datasets for the ScatterChart examples.

One module, one seed, one generation ORDER — the sequences below are drawn
from a single seeded RNG exactly as the pre-migration page drew them, so
every example renders the same points it always has. Splitting the
generation into the per-example modules would re-seed per module and
silently reshuffle every cloud.
"""
import random

random.seed(42)

# Two clusters
cluster_a = [
    {'x': random.gauss(150, 40), 'y': random.gauss(300, 60), 'id': i}
    for i in range(50)
]
cluster_b = [
    {'x': random.gauss(350, 50), 'y': random.gauss(150, 45), 'id': i}
    for i in range(50)
]

# Correlated data with z-values
correlated = []
for i in range(80):
    x = random.uniform(0, 100)
    noise = random.gauss(0, 10)
    y = 2 * x + 20 + noise
    z = x + y  # z for color mapping
    correlated.append({'x': round(x, 1), 'y': round(y, 1), 'z': round(z, 1),
                       'id': i})

# Log-scale data (simulated processor data)
log_data_a = []
log_data_b = []
for i in range(40):
    year = 1990 + i * 0.8
    density_a = 10 ** (random.uniform(1, 2) + (year - 1990) * 0.06)
    density_b = 10 ** (random.uniform(0.8, 1.8) + (year - 1990) * 0.055)
    log_data_a.append({'x': round(year, 1), 'y': round(density_a), 'id': i})
    log_data_b.append({'x': round(year, 1), 'y': round(density_b), 'id': i})

# Small datasets for marker sizes
size_data_small = [
    {'x': random.uniform(10, 90), 'y': random.uniform(10, 90), 'id': i}
    for i in range(15)
]
size_data_large = [
    {'x': random.uniform(10, 90), 'y': random.uniform(10, 90), 'id': i}
    for i in range(20)
]
