import pandas as pd
import numpy as np

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

print(len(df.axes[1]-3), len(df.axes[0]))