import pandas as pd
import numpy as np

# Read the excel file
df = pd.read_excel("Line Production September 2023.xlsx")

# Define number of products and number of production lines
# (-3 because there are column of deadlines, penalty costs, and prod. names)
num_prod = len(df.axes[0])
num_prod_lines = (len(df.axes[1])-3)

# Step 1: Initialize x as an array of zeros (all-free decision variables)
x = np.zeros((num_prod, num_prod_lines))

# Put the production lines (l) and products (p) in lists as indices of the model
line_headers = df.columns.tolist()[1:num_prod_lines+1]
product_list = df["Product"].tolist()

# Also define the parameters of deadlines (d_p) & penalty costs (c_p)
deadlines = df["deadline"]
penalty_costs = df["penalty cost"]

# Step 2 & 3: Step and iterate for each product;
# determine the quality of solution based on the lead time (the lesser, the better)
for prod in product_list:
    product_data = df[df["Product"] == prod]
    best_line_for_product = product_data[line_headers].idxmin(axis=1).values[0]
    which_line = line_headers.index(best_line_for_product)
    which_product = product_list.index(prod)
    x[which_product][which_line] = 1 # for index p = product and l = prod. line

# Formulate list of tasks for each production line
transposed_x = x.transpose()
attributes_prod = [] # attributes for each row in Excel file
tasks_list = [] # list for products that each line has to process

for task_row in range(len(transposed_x)):
    tasks = sum(transposed_x[task_row])
    tasks_list.append([line_headers[task_row], (np.where(transposed_x[task_row] == 1)[0])])
    
for task_index in range(len(tasks_list)):
    task_sequence = [] # sequence of tasks for each prod. line
    deadline_penalty = [] # deadline and penalty for each product
    task_in_line = tasks_list[task_index][0]

    for product_type in list(tasks_list[task_index][1]):
        deadline_penalty.append([deadlines[product_type], penalty_costs[product_type], product_type])
    deadline_penalty = sorted(deadline_penalty)

    # Calculate the lead time and penalty costs (objective value) with the current solution
    tardiness = 0
    start_times = [0]
    for product in range(len(deadline_penalty)):
        penalty = 0
        product_index = deadline_penalty[product][2]
        deadline_prod = deadline_penalty[product][0]
        penalty_prod = deadline_penalty[product][1]
        product_num = product_list[product_index]
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

        attributes_prod.append([product_num, task_in_line, start_time, process_time, end_time, deadline_prod, tardiness, penalty])

columns = ["Product", "Line", "Start", "Process Time", "End", "Deadline", "Tardiness", "Total Penalty Cost"]
schedule = pd.DataFrame(attributes_prod, columns=columns)
# schedule.sort_values(by="Product")
schedule.to_excel("schedule1.xlsx", index=False)

# The total penalty costs is 6096.