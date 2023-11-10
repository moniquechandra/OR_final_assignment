import pandas as pd
import numpy as np
import logging
import time
from mathematical_model import MathModel
from scheduling import ProductAttributes
from greedy_constructive_heuristics import GreedyConstructiveHeuristics, greedy_constructive_heuristics

logging.basicConfig(filename='discrete_improving.txt', level=logging.INFO, filemode='w')

# Define the imported classes
gch = GreedyConstructiveHeuristics()
model = MathModel()
att = ProductAttributes()

# Choose any starting feasible solution x
# In this case, I use the feasible solution from the first solution method
initial_solution = gch.greedy_algorithm()

class DiscreteImprovingSearch:

    # Set the initial total penalty cost as the reference for improvement
    # If the total penalty becomes smaller than the initial total penalty, the model has improved!
    total_penalty = greedy_constructive_heuristics()

    # Functions for finding first improvement in the Discrete Improving Search algorithm

    def best_improvement(self):
        # 2-opt swapping to find the local optimal based on the Best Improvement approach
        start_algorithm = time.time()

        # Make a copy of the initial solution to avoid modifying it directly
        improving_solution = initial_solution.copy()

        for prod_index in range(model.num_prod - 1):        
            for line_index in range(model.num_prod_lines - 1):
                improved = True
                while improved:
                    improved = False
                    where_one = np.where(improving_solution[prod_index] == 1)[0][0]
                    improving_solution[prod_index][where_one] = 0
                    improving_solution[prod_index][line_index + 1] = 1

                    # Calculate the penalty of the current solution
                    attributes = att.get_product_attributes(improving_solution)
                    current_penalty = att.calculate_total_penalty(attributes)
             
                # Check if the current solution is better
                if current_penalty < self.total_penalty:
                    self.total_penalty = current_penalty
                    best_solution = improving_solution.copy()
                else:
                    pass
            
            # If there are no better solution in the neighbourhood, the last improving solution is the best solution.
            improving_solution = best_solution.copy()

        end_algorithm = time.time()
        elapsed_algorithm = end_algorithm - start_algorithm

        # Log the time complexity of G.C.H algorithm
        logging.info(f"\nTime complexity of the algorithm for {model.num_prod} iterations = {elapsed_algorithm / model.num_prod} seconds")

        return best_solution

    def scheduling_discrete_improving(self):
        # Insert the built schedule in a dataframe
        x = self.best_improvement()
        rows = att.get_product_attributes(x)
        
        columns = ["Product", "Line", "Start", "Process Time", "End", "Deadline", "Tardiness", "Total Penalty Cost"]
        schedule = pd.DataFrame(rows, columns=columns)
        
        return schedule

# First solution method execution
def discrete_improving_search():
    gch = DiscreteImprovingSearch()
    start_schedule = time.time()
    gch.scheduling_constructive_heuristics().to_excel("d_i_s_schedule.xlsx",index=False)
    end_schedule = time.time()
    elapsed_time = end_schedule - start_schedule
    logging.info("\nComputation time of the scheduling: %s seconds", elapsed_time)

    # Log the final objective value of the current solution and print it as an output
    logging.info(f"\nObjective value: {att.total_penalty}")
    print(f"Objective value: {att.total_penalty}")

    return att.total_penalty

greedy_constructive_heuristics()

ss = DiscreteImproving()
ss.best_improvement()