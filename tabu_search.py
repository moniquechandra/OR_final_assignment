import pandas as pd
import numpy as np
import logging
import time

from design.mathematical_model import MathModel
from scheduling import ProductAttributes
from greedy_constructive_heuristics import GreedyConstructiveHeuristics, objective_value

# Define the imported classes
gch = GreedyConstructiveHeuristics()
model = MathModel()
att = ProductAttributes()

# Choose any starting feasible solution x
# In this case, I use the feasible solution from the first solution method (Greedy Constructive Heuristics)
initial_solution = gch.construct_decision_variable()

class SimulatedAnnealing:

    # Set the initial objective value as the reference for improvement
    # If the penalty of the current algorithm becomes smaller than the initial total penalty, the model has improved!
    total_penalty = objective_value()
    
    # Initiate a tabu list
    temperature = 100

    # Functions for finding first improvement in the Discrete Improving Search algorithm

    def tabu_search(self):

        # Make a copy of the initial solution to avoid modifying it directly
        improving_solution = initial_solution.copy()

        for prod_index in range(model.num_prod - 1):        
            for line_index in range(model.num_prod_lines - 1):

                # While the new solution is improved,
                improved = True
                while improved:
                    improved = False
                
                    # Apply 2-opt to find the better solution in the neighbourhood
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
                    objective_value_list.append(current_penalty)
                else:
                    pass
        
            # If there are no better solution in the neighbourhood, the last improving solution is the best solution.
            improving_solution = best_solution.copy()

        end_algorithm = time.time()
        elapsed_algorithm = end_algorithm - start_algorithm

        # Log the time complexity of G.C.H algorithm
        logging.info(f"\nTime complexity of the algorithm for {model.num_prod} iterations = {elapsed_algorithm / model.num_prod} seconds")

        return best_solution


    
