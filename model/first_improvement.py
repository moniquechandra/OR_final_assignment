import pandas as pd
import numpy as np
import logging
import time

from greedy_constructive_heuristics import GreedyConstructiveHeuristics

logging.basicConfig(filename='discrete_improving.txt', level=logging.INFO, filemode='w')

# Read the excel file
df = pd.read_excel("Line Production September 2023.xlsx")

# Step 1: Choose any starting feasible solution x
gch = GreedyConstructiveHeuristics()
initial_solution = gch.greedy_constructive_heuristics()

class SecondSolutionMethod:

    # Parameterization for second solution method, Discrete Improving Search:
    def get_line_end_time(self, line_end_time):
        self.line_end_time = line_end_time

    def get_list_end_time(self, list_end_time):
        self.list_end_time = list_end_time

    def get_late_list(self, late_list):
        self.late_list = late_list

    def get_task_list(self, task_list):
        self.task_list = task_list

    def lateness(self):
        # Define which variable that can be improved by checking which products that are late.
        initial_schedule = model.scheduling_constructive_heuristics()
        late = initial_schedule["Tardiness"] > 0
        products_late = initial_schedule[late]
        late_list = (products_late["Product"]).tolist()

        late_indices = []
        for prod_name in late_list:
            late_indices.append(model.product_list.index(prod_name))

        late_prod_times = []
        for late_prod_index in late_indices:       
            line_index = np.where(initial_solution[late_prod_index] == 1)[0][0]
            task_in_line = model.line_headers[line_index]
            task_prod = df["Product"] == model.product_list[late_prod_index]
            process_time = df.loc[task_prod, task_in_line].values[0]
            late_prod_times.append(process_time)
        
        print(model.get_line_end_time(model.list_end_time))
        print(late_prod_times)


def process_time_for_late(self):
        # Define which variable that can be improved by checking which products that are late.
        initial_schedule = model.scheduling_constructive_heuristics()
        late = initial_schedule["Tardiness"] > 0
        products_late = initial_schedule[late]
        late_list = (products_late["Product"]).tolist()
        
        late_indices = []
        for prod_name in late_list:
            late_indices.append(product_list.index(prod_name))

        # Define the process time for each late products
        late_prod_times = []
        swapped_time = []
        for late_prod_index in late_indices:       
            line_index = np.where(x[late_prod_index] == 1)[0][0]
            task_in_line = line_headers[line_index]
            task_prod = df["Product"] == product_list[late_prod_index]
            process_time = df.loc[task_prod, task_in_line].values[0]
            late_prod_times.append([process_time, line_index])

        # Coba reverse! Calculationnya masi salah:
        # Harusnya 69, 85, 55, 83, 127, 149 -> late_prod_times = late_prod_times.reverse()
        print(late_prod_times)
        print(self.line_end_time)
            # In this code, line is still undefined/wrong. harus nyocokin end time per line sama nama linenya!!
            # sekarang malah ngiranya produknya per line, padahal harus dicek dulu product itu di line mana!!
        for [process_time, line_index] in late_prod_times:
            swapped_time.append(self.line_end_time[line_index] - process_time) 

        # print(swapped_time)

mode.lateness()

    # M = np.zeros((model.num_prod, model.num_prod_lines))