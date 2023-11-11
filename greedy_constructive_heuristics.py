import pandas as pd
import numpy as np
import logging
import time
import sys
import os
sys.path.append(os.chdir('../OR PROGRAMMING ASSIGNMENT'))

from mathematical_model import MathModel
from scheduling import ProductAttributes

# Initiate a logger to log necessary information
log_format = "%(asctime)s - %(module)s - %(message)s"
logging.basicConfig(filename='log_file.log', level=logging.INFO, format=log_format, filemode='w')

# Declare classes
model = MathModel()
att = ProductAttributes()

class GreedyConstructiveHeuristics:
    
    # Define the decision variable (all-free binary variable)
    x = np.zeros((model.num_prod, model.num_prod_lines))
    
    def greedy_algorithm(self):
        # Decide the production line greedily for each product based on the lead time (the lesser, the better)
        
        for product in model.product_list:
            product_data = model.df[model.df["Product"] == product]
            best_line = product_data[model.line_headers].idxmin(axis=1).values[0]
            which_line = model.line_headers.index(best_line)
            which_product = model.product_list.index(product)
            self.x[which_product][which_line] = 1 # for index p = product and l = prod. line
            
            # Log the production line that is assigned for each product
            logging.info(f"Product {product} has been assigned to Line {best_line}")

        return self.x
    
    def scheduling_constructive_heuristics(self):
        # Insert the built schedule in a dataframe
        
        # Determine the time complexity of the Greedy Constructive Heuristics algorithm
        start_algorithm = time.time()
        x = self.greedy_algorithm()
        end_algorithm = time.time()
        elapsed_algorithm = end_algorithm - start_algorithm

    	# Log the time complexity
        logging.info(f"\nTime complexity of the algorithm for {model.num_prod} iterations = {elapsed_algorithm / model.num_prod} seconds")

        # Construct the schedule as a DataFrame
        rows = att.get_product_attributes(x)
        columns = ["Product", "Line", "Start", "Process Time", "End", "Deadline", "Tardiness", "Total Penalty Cost"]
        schedule = pd.DataFrame(rows, columns=columns)
        
        return schedule

def objective_value():
    # Return the objective value for parametrization
    return att.total_penalty        

def main():
    # Log the computation time of the scheduling and export the Excel schedule
    gch = GreedyConstructiveHeuristics()
    start_schedule = time.time()
    gch.scheduling_constructive_heuristics().to_excel("g_c_h_schedule.xlsx",index=False)
    end_schedule = time.time()
    elapsed_time = end_schedule - start_schedule

    logging.info("\nComputation time of the scheduling: %s seconds", elapsed_time)
    logging.info(f"Objective value: {objective_value()}")
    print(f"Objective value: {objective_value()}")
    

main()

# # First solution method execution
# def greedy_constructive_heuristics():
#     gch = GreedyConstructiveHeuristics()
#     start_schedule = time.time()
#     gch.scheduling_constructive_heuristics().to_excel("g_c_h_schedule.xlsx",index=False)
#     end_schedule = time.time()
#     elapsed_time = end_schedule - start_schedule
#     logging.info("\nComputation time of the scheduling: %s seconds", elapsed_time)

#     # Log the final objective value of the current solution and print it as an output
#     logging.info(f"\nObjective value: {att.total_penalty}")
#     print(f"Objective value: {att.total_penalty}")

#     return att.total_penalty

# greedy_constructive_heuristics()