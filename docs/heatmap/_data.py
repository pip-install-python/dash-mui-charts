"""Shared demo datasets for the Heatmap examples — one definition, used by
every section, exactly as the pre-migration page defined them."""

# Weekly activity (7 days x 4 weeks)
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4']

# Activity data as [x_index, y_index, value]
activity_data = [
    # Week 1
    [0, 0, 8], [1, 0, 7], [2, 0, 9], [3, 0, 6], [4, 0, 5], [5, 0, 2], [6, 0, 1],
    # Week 2
    [0, 1, 7], [1, 1, 8], [2, 1, 8], [3, 1, 9], [4, 1, 6], [5, 1, 3], [6, 1, 2],
    # Week 3
    [0, 2, 9], [1, 2, 8], [2, 2, 7], [3, 2, 8], [4, 2, 7], [5, 2, 4], [6, 2, 3],
    # Week 4
    [0, 3, 6], [1, 3, 7], [2, 3, 8], [3, 3, 9], [4, 3, 8], [5, 3, 5], [6, 3, 2],
]

# Correlation matrix data
variables = ['Revenue', 'Users', 'Sessions', 'Conversion', 'Bounce Rate']
correlation_data = [
    [0, 0, 1.00], [1, 0, 0.85], [2, 0, 0.78], [3, 0, 0.65], [4, 0, -0.42],
    [0, 1, 0.85], [1, 1, 1.00], [2, 1, 0.92], [3, 1, 0.58], [4, 1, -0.55],
    [0, 2, 0.78], [1, 2, 0.92], [2, 2, 1.00], [3, 2, 0.48], [4, 2, -0.62],
    [0, 3, 0.65], [1, 3, 0.58], [2, 3, 0.48], [3, 3, 1.00], [4, 3, -0.38],
    [0, 4, -0.42], [1, 4, -0.55], [2, 4, -0.62], [3, 4, -0.38], [4, 4, 1.00],
]

# Temperature data (hours x days)
hours = ['6am', '9am', '12pm', '3pm', '6pm', '9pm']
temp_days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
temperature_data = [
    # Monday
    [0, 0, 58], [0, 1, 65], [0, 2, 72], [0, 3, 75], [0, 4, 70], [0, 5, 62],
    # Tuesday
    [1, 0, 55], [1, 1, 62], [1, 2, 70], [1, 3, 73], [1, 4, 68], [1, 5, 60],
    # Wednesday
    [2, 0, 60], [2, 1, 68], [2, 2, 78], [2, 3, 82], [2, 4, 76], [2, 5, 65],
    # Thursday
    [3, 0, 62], [3, 1, 70], [3, 2, 80], [3, 3, 85], [3, 4, 78], [3, 5, 68],
    # Friday
    [4, 0, 58], [4, 1, 66], [4, 2, 74], [4, 3, 78], [4, 4, 72], [4, 5, 64],
]
