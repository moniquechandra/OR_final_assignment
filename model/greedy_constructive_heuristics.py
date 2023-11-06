import pandas as pd
import numpy as np
import logging
import time
from mathematical_model import MathModel

# Provide a txt file to log necessary information
logging.basicConfig(filename='g_c_h.txt', level=logging.INFO, filemode='w')

# Define the decision variable (all-free binary variable) and parameters
model = MathModel()
x = np.zeros((model.num_prod, model.num_prod_lines))

class GreedyConstructiveHeuristics:
    
    # Define parameters for parametrization
    total_penalty = 0

    # Functions for parametrization
    def sort_product(self, sorted_products):
        self.sorted_products = sorted_products

    def get_total_penalty(self, total_penalty):
        self.total_penalty = total_penalty

    # Functions to implement greedy constructive heuristics:
    
    def greedy_algorithm(self):
        # Step 2 & 3: Step and iterate for each product:
        # Decide the production line greedily for each product based on the lead time (the lesser, the better)

        start_algorithm = time.time()
        for product in model.product_list:
            product_data = model.df[model.df["Product"] == product]
            best_line = product_data[model.line_headers].idxmin(axis=1).values[0]
            which_line = model.line_headers.index(best_line)
            which_product = model.product_list.index(product)
            x[which_product][which_line] = 1 # for index p = product and l = prod. line
            logging.info(f"Production line = {best_line} | Assigned product = {product}")

        end_algorithm = time.time()
        elapsed_algorithm = end_algorithm - start_algorithm

        # Log the time complexity of G.C.H algorithm
        logging.info(f"\nTime complexity of the algorithm for {model.num_prod} iterations = {elapsed_algorithm / model.num_prod} seconds")

        return x

    def sorted_tasks(self, x):
        # Schedule products based on the EDD method and littlest damage to the objective value.

        # Append tasks_list with the production line and the indices of product that will be produced on that line
        task_list = []
        trans_x = x.transpose()
        for task_row in range(len(trans_x)):
            line = model.line_headers[task_row]
            assigned_products = np.where(trans_x[task_row] == 1)[0]
            task_list.append([line, assigned_products])

        return task_list
    
    def calculate_penalty(self, tardiness, penalty_prod):
        # Calculate the penalty costs (objective value) with the current solution    
        penalty = tardiness * penalty_prod
        return penalty

    def gch_attributes(self, task_list):
        # Append attributes for the G.C.H schedule

        attributes_prod = [] # attributes for each row in Excel file
        self.total_penalty = 0
        self.sorted_products = []

        # Determine the attributes for each product to put it in each product's row
        for line, products in task_list:

            # Determine the attributes for each product to put it in each product's row
            self.sorted_products = sorted(products, key=lambda product_index: (model.deadlines[product_index], -model.penalty_costs[product_index]))

            # Calculate the start, process, and end time
            current_time = 0

            for product in self.sorted_products:
                product_name = model.df.iloc[product]["Product"]
                process_time = model.df.iloc[product][line]
                deadline_prod = model.deadlines[product]
                penalty_prod = model.penalty_costs[product]

                start_time = current_time
                end_time = start_time + process_time
                tardiness = max(0, end_time - deadline_prod)
                
                # Calculate penalty, if applicable 
                penalty = self.calculate_penalty(tardiness, penalty_prod)
                self.total_penalty += penalty

                attributes_prod.append([product_name, line, start_time, process_time, end_time, deadline_prod, tardiness, penalty])
                current_time = end_time

        # Update the parameters
        self.get_total_penalty(self.total_penalty)
        self.sort_product(self.sorted_products)

        return attributes_prod
    
    def scheduling_constructive_heuristics(self):
        # Insert the built schedule in a dataframe
        sort_task_list = self.sorted_tasks(self.greedy_algorithm())
        att = self.gch_attributes(sort_task_list)
        
        columns = ["Product", "Line", "Start", "Process Time", "End", "Deadline", "Tardiness", "Total Penalty Cost"]
        schedule = pd.DataFrame(att, columns=columns)
        
        return schedule

# First solution method execution

def greedy_constructive_heuristics():
    model = GreedyConstructiveHeuristics()
    start_schedule = time.time()
    model.scheduling_constructive_heuristics().to_excel("g_c_h_schedule.xlsx",index=False)
    end_schedule = time.time()
    elapsed_time = end_schedule - start_schedule
    logging.info("\nComputation time of the scheduling: %s seconds", elapsed_time)

    # Log the final objective value of the current solution and print it as an output
    logging.info(f"\nObjective value: {model.total_penalty}")
    print(f"Objective value: {model.total_penalty}")

    return model.total_penalty

greedy_constructive_heuristics()
