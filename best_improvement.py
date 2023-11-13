import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import logging
import time

from design.mathematical_model import MathModel
from product_attributes import Attributes
from greedy_constructive_heuristics import GreedyConstructiveHeuristics, objective_value

# Initiate a logger to log necessary information
log_format = "%(asctime)s - %(module)s - %(message)s"
logging.basicConfig(filename='log_file.log', level=logging.INFO, format=log_format, filemode='w')

# Define the imported classes
gch = GreedyConstructiveHeuristics()
model = MathModel()
att = Attributes()

# Choose any starting feasible solution x
# In this case, I use the feasible solution from the first solution method
initial_solution = gch.construct_decision_variable()


class DiscreteImprovingSearch:

    # Set the initial objective value as the reference for improvement
    total_penalty = objective_value()
    
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

    def schedule_discrete_improving(self):
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
    dis.schedule_discrete_improving().to_excel("d_i_s_schedule.xlsx",index=False)

    # Log the final objective value of the current solution and print it as an output
    logging.info(f"D.I.S' objective value: {att.total_penalty}")
    print(f"The total penalty costs when using the best improvement approach in Discrete Improving Search = {att.total_penalty}")

    return att.total_penalty

main()