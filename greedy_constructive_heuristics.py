import pandas as pd
import numpy as np
import logging
import time

from design.mathematical_model import MathModel
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
    
    def construct_decision_variable(self):
        # Decide the production line greedily for each product based on the lead time (the lesser, the better)
        for product in model.product_list:
            product_data = model.df[model.df["Product"] == product]
            best_line = product_data[model.line_headers].idxmin(axis=1).values[0]
            which_line = model.line_headers.index(best_line)
            which_product = model.product_list.index(product)
            self.x[which_product][which_line] = 1 # for index p = product and l = prod. line
        
        return self.x
    
    def log_greedy_algorithm(self):
        # Log the time complexity of the Greedy Constructive Heuristics algorithm and info. regarding solution
        start_algorithm = time.time()
        solution = self.construct_decision_variable()
        end_algorithm = time.time()
        elapsed_algorithm = end_algorithm - start_algorithm

    	# Log the time complexity
        logging.info(f"\nTime complexity of the algorithm for {model.num_prod} iterations = {elapsed_algorithm / model.num_prod} seconds")
        
        # Log the production line that is assigned for each product
        product_index, line_index = np.where(solution == 1)
        for p, l in zip(product_index, line_index):
            product = model.product_list[p]
            line = model.line_headers[l]
            logging.info(f"Product {product} has been assigned to Line {line}")

    def scheduling_constructive_heuristics(self, x):
        # Insert the built schedule in a dataframe and log the information regarding the scheduling time.

        start_schedule = time.time()
        rows = att.get_product_attributes(x)
        columns = ["Product", "Line", "Start", "Process Time", "End", "Deadline", "Tardiness", "Total Penalty Cost"]
        schedule = pd.DataFrame(rows, columns=columns)
        
        end_schedule = time.time()
        elapsed_time = end_schedule - start_schedule

        # Log scheduling time to the log file
        logging.info("Scheduling time: %s seconds", elapsed_time)

        return schedule

def objective_value():
    # Return the objective value for future reuse/reference
    return att.total_penalty        

def main():
    # Log the final objective value and export the Excel schedule
    gch = GreedyConstructiveHeuristics()
    gch.log_greedy_algorithm()

    x = gch.construct_decision_variable()
    gch.scheduling_constructive_heuristics(x).to_excel("g_c_h_schedule.xlsx",index=False)
    
    logging.info(f"Objective value: {att.total_penalty}")
    print(f"G.C.H's objective value: {att.total_penalty}")

main()
objective_value()