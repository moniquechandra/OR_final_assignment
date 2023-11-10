import pandas as pd
import numpy as np
import logging
import time
import sys
import os
sys.path.append(os.chdir('../OR PROGRAMMING ASSIGNMENT'))

from mathematical_model import MathModel
from scheduling import ProductAttributes

# Provide a txt file to log necessary information
logging.basicConfig(filename='g_c_h.log', level=logging.INFO, filemode='w')

# Declare classes
model = MathModel()
att = ProductAttributes()

# Define the decision variable (all-free binary variable) and parameters
x = np.zeros((model.num_prod, model.num_prod_lines))

class GreedyConstructiveHeuristics:
    
    def greedy_algorithm(self):
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

    def scheduling_constructive_heuristics(self):
        # Insert the built schedule in a dataframe
        x = self.greedy_algorithm()
        rows = att.get_product_attributes(x)
        
        columns = ["Product", "Line", "Start", "Process Time", "End", "Deadline", "Tardiness", "Total Penalty Cost"]
        schedule = pd.DataFrame(rows, columns=columns)
        
        return schedule

# First solution method execution
def greedy_constructive_heuristics():
    gch = GreedyConstructiveHeuristics()
    start_schedule = time.time()
    gch.scheduling_constructive_heuristics().to_excel("g_c_h_schedule.xlsx",index=False)
    end_schedule = time.time()
    elapsed_time = end_schedule - start_schedule
    logging.info("\nComputation time of the scheduling: %s seconds", elapsed_time)

    # Log the final objective value of the current solution and print it as an output
    logging.info(f"\nObjective value: {att.total_penalty}")
    print(f"Objective value: {att.total_penalty}")

    return att.total_penalty

greedy_constructive_heuristics()
