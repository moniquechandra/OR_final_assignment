import pandas as pd
import numpy as np

# Read the excel file
df = pd.read_excel("Line Production September 2023.xlsx")

# temporary variables: how many lines, how many products in the file
num_prod_lines = 7
num_prod = 27

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
for p in product_list:
    product_line = df[df['Product'] == p] # the overview of the data for the current product
    best_line_for_product = product_line[line_headers].idxmin(axis=1).values[0]
    which_line = line_headers.index(best_line_for_product)
    which_product = product_list.index(p)
    x[which_product][which_line] = 1 # for index p = product and l = prod. line

    # for line in line_headers:
    #     which_product = (df[df[line] == minimal_lead_time_per_line]["Product"]).index[0]
    #     which_line = line_headers.index(line)
    #     x[which_product][which_line] = 1
    #     product_list.pop(which_product)

    # Check whether there are double copies for each product!

# Formulating a feasible schedule with Greedy Constructive Heuristics
transposed_x = x.transpose()
tasks_list = [] # list for products that each line has to process
penalty = 0

for task_line in range(len(transposed_x)):
    tasks = sum(transposed_x[task_line])
    # if tasks > 1:
    tasks_list.append([line_headers[task_line], (np.where(transposed_x[task_line] == 1)[0])])
    
# Determine the sequence of tasks based on its deadline (using EDD method)
for i in range(len(tasks_list)):
    attribute_prod = []
    task_sequence = []
    for product_type in list(tasks_list[i][1]):
        attribute_prod.append([deadlines[product_type], penalty_costs[product_type], product_type])
    attribute_prod = sorted(attribute_prod)
    task_sequence = [product_list[attribute_prod[i][2]] for i in range(len(attribute_prod))]    
    print(tasks_list[i][0], task_sequence) 

    # Calculate the penalty costs (objective value) with the current solution
    lead_time = 0
    for p in range(len(attribute_prod)):
        lead_time += df.loc[df['Product'] == product_list[attribute_prod[p][2]], tasks_list[i][0]].values[0]
        if lead_time > attribute_prod[p][0]:
            penalty += (lead_time - attribute_prod[p][0]) * attribute_prod[p][1]

print(penalty)     
# The feasible schedule is:
# L1 ['P26', 'P6', 'P24', 'P9']
# L2 ['P10', 'P7', 'P27', 'P16', 'P15']
# L3 ['P13', 'P25']
# L4 ['P4', 'P8']
# L5 ['P18', 'P21', 'P3']
# L6 ['P2', 'P11', 'P14', 'P23', 'P5', 'P19', 'P20']
# L7 ['P22', 'P17', 'P1', 'P12']

# the total penalty costs is 6096.