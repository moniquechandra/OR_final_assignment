import pandas as pd
import numpy as np
import logging
import time
from mathematical_model import MathModel
from greedy_constructive_heuristics import GreedyConstructiveHeuristics, greedy_constructive_heuristics

logging.basicConfig(filename='discrete_improving.txt', level=logging.INFO, filemode='w')

# Read the excel file
df = pd.read_excel("Line Production September 2023.xlsx")

# Step 0: Choose any starting feasible solution x
gch = GreedyConstructiveHeuristics()
model = MathModel()
initial_solution = gch.greedy_algorithm()
# initial_solution = np.array([[1, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 1]])

# task_list = gch.sorted_tasks(initial_solution)

class SecondSolutionMethod:

    # Define its total penalty cost (the objective value) as the parameter for improvement
    total_penalty = greedy_constructive_heuristics()

    # Parameterization for second solution method, Discrete Improving Search:
    def get_late_list(self, late_list):
        self.late_list = late_list

    # Functions for finding first improvement in the Discrete Improving Search algorithm

    def first_two_opt(self):
        # 2-opt swapping to find improving solution(s) based on the First Improvement approach
        improve = True
        improving_solution = initial_solution.copy()
        prod_line = model.line_headers.copy()
        # for line in range(model.num_prod_lines -1):
        #     for prod in range(model.num_prod - 35):

                
            # # Swap product1 and product2 and see whether there are improvements
        if improving_solution[0][0] == 1:
            improving_solution[0][0] = 0
            improving_solution[0][0 + 1] = 1 # has to be zero again if not improving

            attributes_prod = []
            new_task_list = gch.sorted_tasks(improving_solution)
            current_sol_total_penalty = 0
            # Determine the attributes for each product to put it in each product's row
            for line, products in new_task_list:

                # Determine the attributes for each product to put it in each product's row
                self.sorted_products = sorted(products, key=lambda product_index: (model.deadlines[product_index], -model.penalty_costs[product_index]))

                # Calculate the start, process, and end time
                current_time = 0

                for product in self.sorted_products:
                    process_time = model.df.iloc[product][line]
                    deadline_prod = model.deadlines[product]
                    penalty_prod = model.penalty_costs[product]

                    start_time = current_time
                    end_time = start_time + process_time
                    tardiness = max(0, end_time - deadline_prod)
                    
                    # Calculate penalty, if applicable 
                    penalty = gch.calculate_penalty(tardiness, penalty_prod)
                    current_sol_total_penalty += penalty
                    current_time = end_time

                    # if current_sol_total_penalty < self.total_penalty:
                    #     print("yay", current_sol_total_penalty)

                    # else:
                    #     print("current sol not improving", {current_sol_total_penalty}, {prod}, {line})
        if current_sol_total_penalty < self.total_penalty:
            improve = True
            



    # def lateness(self):
    #     # Define which variable that can be improved by checking which products that are late.
    #     initial_schedule = gch.scheduling_constructive_heuristics()
    #     late = initial_schedule["Tardiness"] > 0
    #     products_late = initial_schedule[late]
    #     late_list = (products_late["Product"]).tolist()

    #     late_indices = []
    #     for prod_name in late_list:
    #         late_indices.append(model.product_list.index(prod_name))

    #     late_prod_times = []
    #     for late_prod_index in late_indices:       
    #         line_index = np.where(initial_solution[late_prod_index] == 1)[0][0]
    #         task_in_line = model.line_headers[line_index]
    #         task_prod = df["Product"] == model.product_list[late_prod_index]
    #         process_time = df.loc[task_prod, task_in_line].values[0]
    #         late_prod_times.append(process_time)
        
    #     print(model.get_line_end_time(model.list_end_time))
    #     print(late_prod_times)


def process_time_for_late(self):
        # Define which variable that can be improved by checking which products that are late.
        initial_schedule = model.scheduling_constructive_heuristics()
        late = initial_schedule["Tardiness"] > 0
        products_late = initial_schedule[late]
        late_list = (products_late["Product"]).tolist()
        
        late_indices = []
        for prod_name in late_list:
            late_indices.append(model.product_list.index(prod_name))

        # Define the process time for each late products
        late_prod_times = []
        swapped_time = []
        for late_prod_index in late_indices:       
            line_index = np.where(gch.x[late_prod_index] == 1)[0][0]
            task_in_line = model.line_headers[line_index]
            task_prod = df["Product"] == model.product_list[late_prod_index]
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

ss = SecondSolutionMethod()
ss.first_two_opt()

    # M = np.zeros((model.num_prod, model.num_prod_lines))