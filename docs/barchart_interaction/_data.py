"""Shared demo data for the BarChart interaction examples — same seed and
draw order as the pre-migration page."""
import random

random.seed(42)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
revenue = [random.randint(30, 90) for _ in months]
expenses = [random.randint(20, 65) for _ in months]

PRE_STYLE = {
    'fontSize': '12px',
    'margin': 0,
    'padding': '10px 14px',
    'borderRadius': '6px',
    'background': 'var(--mantine-color-body)',
    'border': '1px solid var(--mantine-color-default-border)',
    'maxHeight': '120px',
    'overflow': 'auto',
    'color': 'var(--mantine-color-text)',
}
