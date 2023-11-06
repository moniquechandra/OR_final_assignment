import pandas as pd
import numpy as np

# Consists of the applied dataset in Excel format and the parameters for the mathematical model.

class MathModel:
    # Read the excel file
    df = pd.read_excel("Line Production December 2023.xlsx")

    # Define number of products and number of production lines
    # (-3 because there are column of deadlines, penalty costs, and prod. names)
    num_prod = len(df.axes[0])
    num_prod_lines = (len(df.axes[1])-3)

    # Put the production lines (l) and products (p) in lists as indices of the model
    line_headers = df.columns.tolist()[1:num_prod_lines+1]
    product_list = df["Product"].tolist()

    # Define the parameters of deadlines (d_p) & penalty costs (c_p)
    deadlines = df["deadline"]
    penalty_costs = df["penalty cost"]