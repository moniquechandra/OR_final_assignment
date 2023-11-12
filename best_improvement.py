import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import time

from design.mathematical_model import MathModel
from scheduling import ProductAttributes
from greedy_constructive_heuristics import GreedyConstructiveHeuristics, objective_value

# Initiate a logger to log necessary information
log_format = "%(asctime)s - %(module)s - %(message)s"
logging.basicConfig(filename='log_file.log', level=logging.INFO, format=log_format, filemode='w')

# Define the imported classes
gch = GreedyConstructiveHeuristics()
model = MathModel()
att = ProductAttributes()

# Choose any starting feasible solution x
# In this case, I use the feasible solution from the first solution method
initial_solution = gch.construct_decision_variable()

# sorted_prod = att.get_sorted_products

class DiscreteImprovingSearch:

    # Set the initial objective value as the reference for improvement
    # If the penalty of the current algorithm becomes smaller than the initial total penalty, the model has improved!
    total_penalty = objective_value()
    objective_value_list = []

    # Functions for finding first improvement in the Discrete Improving Search algorithm

    def best_improvement(self):
        # Find the local optima based on the Best Improvement approach
        start_algorithm = time.time()

        # Make a copy of the initial solution to avoid modifying it directly
        improving_solution = initial_solution.copy()
        best_solution = initial_solution.copy()
        
        # Initiate an objective value list to keep track of the obj. value improvement (for plotting)
        objective_value_list = [self.total_penalty]

        # Check for all neighbouring solutions and selects the best one
        for prod_index in range(model.num_prod - 1):       
            for line_index in range(model.num_prod_lines - 1):
                # While the new solution is improved,
                improved = True
                while improved:
                    improved = False
                
                    # Identify which line the product assigned to, then assign it to the next line (l + 1)
                    where_one = np.where(improving_solution[prod_index] == 1)[0][0]
                    improving_solution[prod_index][where_one] = 0
                    improving_solution[prod_index][line_index + 1] = 1

                    # Calculate the penalty of the current solution
                    attributes = att.get_product_attributes(improving_solution)
                    current_penalty = att.calculate_total_penalty(attributes)
                
                # Evaluate the current solution
                if current_penalty < self.total_penalty:
                    self.total_penalty = current_penalty
                    best_solution = improving_solution.copy()
                    chosen_solution_penalty = current_penalty
                else:
                    pass
        
            # If there are no better solution in the neighbourhood,
            # the last improving solution is the locally optimal move.
            objective_value_list.append(chosen_solution_penalty)
            improving_solution = best_solution.copy()
        
        # Calculate the algorithm time
        end_algorithm = time.time()
        elapsed_algorithm = end_algorithm - start_algorithm

        # Log the time complexity of G.C.H algorithm
        logging.info(f"\nTime complexity of the algorithm for {model.num_prod} iterations = {elapsed_algorithm / model.num_prod} seconds")

        # Plot the improvements of the objective value (each dot represent each product)
        plt.plot(objective_value_list, '-o')
        plt.title(f"Discrete Improving Search using Best Improvement on {model.num_prod} products")
        plt.show()

        return best_solution

    def scheduling_discrete_improving(self):
        # Insert the built schedule in a dataframe and log the scheduling time + assigned line for each product
        x = self.best_improvement()
        
        # Log the production line that is assigned for each product
        product_index, line_index = np.where(x == 1)
        for p, l in zip(product_index, line_index):
            product = model.product_list[p]
            line = model.line_headers[l]
            logging.info(f"Product {product} has been reassigned to Line {line}")

        start_schedule = time.time()
        # Insert the built schedule in a dataframe
        rows = att.get_product_attributes(x)
        columns = ["Product", "Line", "Start", "Process Time", "End", "Deadline", "Tardiness", "Total Penalty Cost"]
        schedule = pd.DataFrame(rows, columns=columns)

        # Calculate the elapsed time and log the scheduling time to the log file
        end_schedule = time.time()
        elapsed_time = end_schedule - start_schedule
        logging.info("Scheduling time: %s seconds", elapsed_time)
        
        return schedule

# Second solution method execution
def main():
    dis = DiscreteImprovingSearch()
    dis.scheduling_discrete_improving().to_excel("d_i_s_schedule.xlsx",index=False)

    # Log the final objective value of the current solution and print it as an output
    logging.info(f"D.I.S' objective value: {att.total_penalty}")
    print(f"D.I.S' objective value: {att.total_penalty}")

    return att.total_penalty

main()