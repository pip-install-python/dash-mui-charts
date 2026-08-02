"""Shared 52-week data for the BarChart Pro zoom demos — same seed and
draw order as the pre-migration page (the stacked demo's three series were
drawn AFTER weekly_sales/weekly_returns from the same stream)."""
import random

random.seed(42)

categories = [f'W{i+1}' for i in range(52)]
weekly_sales = [random.randint(20, 100) for _ in categories]
weekly_returns = [random.randint(2, 20) for _ in categories]

online = [random.randint(10, 40) for _ in categories]
retail = [random.randint(5, 30) for _ in categories]
wholesale = [random.randint(3, 15) for _ in categories]
