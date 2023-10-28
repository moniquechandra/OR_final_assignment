import pandas as pd
import numpy as np
import logging
import time

logging.basicConfig(filename='g_c_h.txt', level=logging.INFO, filemode='w')

# Read the excel file
df = pd.read_excel("Line Production September 2023.xlsx")


class Model:

    # Define number of products and number of production lines
    # (-3 because there are column of deadlines, penalty costs, and prod. names)
    num_prod = len(df.axes[0])
    num_prod_lines = (len(df.axes[1])-3)

    # Step 0: Initialize x as an array of zeros (all-free decision variables)
    x = np.zeros((num_prod, num_prod_lines))

    # Put the production lines (l) and products (p) in lists as indices of the model
    line_headers = df.columns.tolist()[1:num_prod_lines+1]
    product_list = df["Product"].tolist()

    # Define the parameters of deadlines (d_p) & penalty costs (c_p)
    deadlines = df["deadline"]
    penalty_costs = df["penalty cost"]


def greedy_constructive_heuristics(product_list):
    # Step 2 & 3: Step and iterate for each product:
    # Decide the production line greedily for each product based on the lead time (the lesser, the better)
    model = Model()
    start_g = time.time()
    for prod in product_list:
        product_data = df[df["Product"] == prod]
        best_line_for_product = product_data[model.line_headers].idxmin(axis=1).values[0]
        which_line = model.line_headers.index(best_line_for_product)
        which_product = product_list.index(prod)
        model.x[which_product][which_line] = 1 # for index p = product and l = prod. line
        logging.info(f"Assigned product = {which_product} | Production line = {which_line}")

    end_g = time.time()
    elapsed_g = end_g - start_g
    logging.info("\nTime complexity of the algorithm = %s seconds", elapsed_g)
    return model.x


def schedule_row(x):
    # Define attributes for each product: "Line", "Start", "Process Time", "End", "Deadline", "Tardiness", "Total Penalty Cost"
    model = Model()
    transposed_x = x.transpose()
    attributes_prod = [] # attributes for each row in Excel file
    tasks_list = [] # list for products that each line has to process
    total_penalty = 0 # count the total penalty

    for task_row in range(len(transposed_x)):
        tasks_list.append([model.line_headers[task_row], (np.where(transposed_x[task_row] == 1)[0])])
        
    for task_index in range(len(tasks_list)):
        task_sequence = [] # sequence of tasks for each prod. line
        deadline_penalty = [] # deadline and penalty for each product
        task_in_line = tasks_list[task_index][0]

        # Sort the tasks for each line based on the EDD method
        for product_type in list(tasks_list[task_index][1]):
            deadline_penalty.append([model.deadlines[product_type], model.penalty_costs[product_type], product_type])
        deadline_penalty = sorted(deadline_penalty)
        # Calculate the lead time and penalty costs (objective value) with the current solution
        tardiness = 0
        start_times = [0]
        for product in range(len(deadline_penalty)):
            penalty = 0
            product_index = deadline_penalty[product][2]
            deadline_prod = deadline_penalty[product][0]
            penalty_prod = deadline_penalty[product][1]
            product_num = model.product_list[product_index]
            process_time = df.loc[df["Product"] == product_num, task_in_line].values[0]

            # Create the sequence of products for each line based on the EDD method
            task_sequence.append(product_num)

            if product == 0:
                start_time = start_times[product]  
            elif product > 0:
                start_times.append(end_time)
                start_time = start_times[product]
            end_time = start_time + process_time
            if end_time > deadline_prod:
                tardiness = end_time - deadline_prod
                penalty = tardiness * penalty_prod
                total_penalty += penalty
            attributes_prod.append([product_num, task_in_line, start_time, process_time, end_time, deadline_prod, tardiness, penalty])
            
            
            columns = ["Product", "Line", "Start", "Process Time", "End", "Deadline", "Tardiness", "Total Penalty Cost"]
            schedule = pd.DataFrame(attributes_prod, columns=columns)

    logging.info(f"\nObjective value: {total_penalty}")
    return schedule
            
# The total penalty costs is 6096.

def main():
    model = Model()
    start_schedule = time.time()
    schedule_row(greedy_constructive_heuristics(model.product_list)).to_excel("schedule1.xlsx", index=False)
    end_schedule = time.time()
    elapsed_time = end_schedule - start_schedule
    logging.info("\nTime complexity of the scheduling: %s seconds", elapsed_time)

main()