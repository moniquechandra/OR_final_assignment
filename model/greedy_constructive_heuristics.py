import pandas as pd
import numpy as np
import logging
import time

logging.basicConfig(filename='g_c_h.txt', level=logging.INFO, filemode='w')

### Dataframe

# Read the excel file
df = pd.read_excel("Line Production December 2023.xlsx")

# Define number of products and number of production lines
# (-3 because there are column of deadlines, penalty costs, and prod. names)
num_prod = len(df.axes[0])
num_prod_lines = (len(df.axes[1])-3)

### Mathematical Model

# Initialize x as an array of zeros (all-free decision variables)
x = np.zeros((num_prod, num_prod_lines))

# Put the production lines (l) and products (p) in lists as indices of the model
line_headers = df.columns.tolist()[1:num_prod_lines+1]
product_list = df["Product"].tolist()

# Define the parameters of deadlines (d_p) & penalty costs (c_p)
deadlines = df["deadline"]
penalty_costs = df["penalty cost"]

class GreedyConstructiveHeuristics:
    
    # Define parameters for parametrization
    total_penalty = 0
    line_end_time = {f'L{i}': 0 for i in range(1, num_prod_lines+1)} # end time for each line

    # Function for parametrization
    def get_line_end_time(self, line_end_time):
        self.line_end_time = line_end_time

    def get_total_penalty(self, total_penalty):
        self.total_penalty = total_penalty


    ### Function for greedy constructive heuristics:
    
    def greedy_algorithm(self):
        # Step 2 & 3: Step and iterate for each product:
        # Decide the production line greedily for each product based on the lead time (the lesser, the bette
        start_algorithm = time.time()
        for product in product_list:
            product_data = df[df["Product"] == product]
            best_line = product_data[line_headers].idxmin(axis=1).values[0]
            which_line = line_headers.index(best_line)
            which_product = product_list.index(product)
            x[which_product][which_line] = 1 # for index p = product and l = prod. line
            logging.info(f"Production line = {best_line} | Assigned product = {product}")

        end_algorithm = time.time()
        elapsed_algorithm = end_algorithm - start_algorithm

        # Log the time complexity of G.C.H algorithm
        logging.info("\nTime complexity of the algorithm = %s seconds", elapsed_algorithm)

        return x

    def create_task_list(self, x):
        # Append tasks_list with the production line and the indices of product that will be produced on that line
        
        task_list = []
        trans_x = x.transpose()
        for task_row in range(len(trans_x)):
            line = line_headers[task_row]
            assigned_products = np.where(trans_x[task_row] == 1)[0]
            task_list.append([line, assigned_products])

        return task_list
    
    def gch_attributes(self, task_list):
        # Append attributes for the G.C.H schedule

        attributes_prod = [] # attributes for each row in Excel file
        self.line_end_time = []
        self.total_penalty = 0

        # Determine the attributes for each product to put it in each product's row
        for line, products in task_list:
            
            # Schedule products based on the EDD method and littlest damage to the objective value.
            sorted_products = sorted(products, key=lambda product_index: (deadlines[product_index], -penalty_costs[product_index]))

            # Calculate the lead time and penalty costs (objective value) with the current solution
            current_time = 0

            for product in sorted_products:
                product_name = df.iloc[product]["Product"]
                process_time = df.iloc[product][line]
                deadline_prod = deadlines[product]
                penalty_prod = penalty_costs[product]

                # Calculate the start, process, and end time. Also the tardiness and penalty costs (if applicable)
                start_time = current_time
                end_time = start_time + process_time
                tardiness = max(0, end_time - deadline_prod)
                penalty = tardiness * penalty_prod
                self.total_penalty += penalty

                attributes_prod.append([product_name, line, start_time, process_time, end_time, deadline_prod, tardiness, penalty])
                current_time = end_time

                self.line_end_time.append(end_time)

        # Update the parameters
        self.get_total_penalty(self.total_penalty)
        self.get_line_end_time(self.line_end_time)

        return attributes_prod
    
    def scheduling_constructive_heuristics(self):
        # Insert the built schedule in a dataframe
        task_list = self.create_task_list(self.greedy_algorithm())
        att = self.gch_attributes(task_list)
        
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

    logging.info("\nTime complexity of the scheduling: %s seconds", elapsed_time)

    # Log the final objective value of the current solution
    logging.info(f"\nObjective value: {model.total_penalty}")

greedy_constructive_heuristics()