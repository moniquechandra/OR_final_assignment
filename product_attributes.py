import pandas as pd
import numpy as np
import logging
import time

from design.mathematical_model import MathModel

model = MathModel()

class Attributes:

    # Define the objective value
    total_penalty = 0

    def get_total_penalty(self, total_penalty):
        # Assign the derived total penalty to the class  
        self.total_penalty = total_penalty

    def sorted_tasks(self, solution):
        # Schedule products based on the EDD method and littlest damage to the objective value.

        # Append tasks_list with the production line and the indices of product that will be produced on that line
        task_list = []
        trans_sol = solution.transpose()
        for task_row in range(len(trans_sol)):
            line = model.line_headers[task_row]
            assigned_products = np.where(trans_sol[task_row] == 1)[0]
            task_list.append([line, assigned_products])

        return task_list

    def calculate_penalty(self, tardiness, penalty_prod):
        # Calculate the penalty costs (objective value) with the current solution    
        penalty = tardiness * penalty_prod
        return penalty
    
    def calculate_total_penalty(self, attributes_prod):
        # Calculate the total penalty from the attributes list
        total_penalty = sum(attr[-1] for attr in attributes_prod)
        return total_penalty

    def get_product_attributes(self, solution):
        # Determine the attributes for each product for the first solution method's schedule
        attributes_prod = []
        self.total_penalty = 0
        task_list = self.sorted_tasks(solution)

        for line, products in task_list:
            # Derive products from the task list to simplify the iteration process
            self.sorted_products = sorted(products, key=lambda product_index: (model.deadlines[product_index], -model.penalty_costs[product_index]))

            # Define the necessary parameter
            current_time = 0
            for product in self.sorted_products:
                product_name = model.df.iloc[product]["Product"]
                process_time = model.df.iloc[product][line]
                deadline_prod = model.deadlines[product]
                penalty_prod = model.penalty_costs[product]

                # Calculate the start, process, and end time to find tardiness
                start_time = current_time
                end_time = start_time + process_time
                tardiness = max(0, end_time - deadline_prod)
                current_time = end_time
                
                # Calculate penalty, if applicable 
                penalty = self.calculate_penalty(tardiness, penalty_prod)

                # Append the attributes into the list
                attributes_prod.append([product_name, line, start_time, process_time, end_time, deadline_prod, tardiness, penalty])
                
        # Update the parameters
        self.total_penalty = self.calculate_total_penalty(attributes_prod)
        self.get_total_penalty(self.total_penalty)
        self.get_sorted_products(self.sorted_products)

        return attributes_prod

