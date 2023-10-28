import pandas as pd
import numpy as np
import logging
import time
from constructive_heuristics.greedy_constructive_heuristics import Model, greedy_constructive_heuristics, schedule_row
logging.basicConfig(filename='discrete_improving.txt', level=logging.INFO, filemode='w')

# Read the excel file
df = pd.read_excel("Line Production September 2023.xlsx")

# Import the class Model() for parameters, dec. variable, etc.
model = Model()

# Step 1: Choose any starting feasible solution x
initial_solution = greedy_constructive_heuristics(model.product_list)
print(initial_solution)
trans_solution = initial_solution.transpose()

# Define which variable that can be improved by checking which products that are late.
initial_schedule = schedule_row(initial_solution)
late = initial_schedule["Tardiness"] > 0
products_late = initial_schedule[late]
late_list = (products_late["Product"]).tolist()
print(late_list)

late_indices = []
for prod_name in late_list:
    late_indices.append(model.product_list.index(prod_name))

# for row in initial_solution:
#     for element in row:
#         if element == 1:

M = []