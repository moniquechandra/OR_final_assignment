import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math as m
import logging
import time

from design.mathematical_model import MathModel
from scheduling import ProductAttributes
from greedy_constructive_heuristics import GreedyConstructiveHeuristics, objective_value

# Define the imported classes
gch = GreedyConstructiveHeuristics()
model = MathModel()
att = ProductAttributes()



# If you need to apply the code, copy from here to the end:

def get_sorted_products(self, sorted_products):
    # Assign the derived sorted products to the class  
    self.sorted_products = sorted_products

def best_improvement(self):
    # Find the local optima based on the Best Improvement approach
    start_algorithm = time.time()

    # Make a copy of the initial solution to avoid modifying it directly
    improving_solution = initial_solution.copy()
    best_solution = initial_solution.copy()

    task_list = att.sorted_tasks(improving_solution)

    # Initiate an objective value list to keep track of the obj. value improvement (for plotting)
    objective_value_list = [self.total_penalty]
    i = 0
    
    # Get the sorted products (the same as G.C.H's)
    for line, products in task_list:
        if i < 1:
            # Derive products from the task list to simplify the iteration process
            self.sorted_products = sorted(products, key=lambda product_index: (model.deadlines[product_index], -model.penalty_costs[product_index]))
            self.get_sorted_products(self.sorted_products)
            i += 1
        else:
            break

    # Check for all neighbouring solutions and selects the best one
    for prod_index in self.sorted_products:       
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
    
    end_algorithm = time.time()
    elapsed_algorithm = end_algorithm - start_algorithm

    # Log the time complexity of G.C.H algorithm
    logging.info(f"\nTime complexity of the algorithm for {model.num_prod} iterations = {elapsed_algorithm / model.num_prod} seconds")

    # Plot the improvements of the objective value (each dot represent each product)
    plt.plot(objective_value_list, '-o')
    plt.title(f"Discrete Improving Search using Best Improvement on {model.num_prod} products")
    plt.show()
    return best_solution