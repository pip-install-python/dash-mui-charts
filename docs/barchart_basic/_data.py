"""Shared demo data for the BarChart basics examples — one seeded RNG in
the pre-migration draw ORDER, so every bar keeps its height."""
import random

random.seed(42)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
revenue = [random.randint(30, 90) for _ in months]
expenses = [random.randint(20, 65) for _ in months]
profit = [r - e for r, e in zip(revenue, expenses)]

# The stacked example's draws came AFTER revenue/expenses in the original
# module — same stream position preserved here.
organic = [random.randint(10, 30) for _ in months]
paid = [random.randint(8, 25) for _ in months]
referral = [random.randint(5, 15) for _ in months]
