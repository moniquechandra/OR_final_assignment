import pandas as pd

# Consists of the applied dataset in Excel format and the parameters for the mathematical model.

class MathModel:
    
    # Read the excel file
    df = pd.read_excel("Line Production December 2023.xlsx")

    # Number of products and number of production lines
    # (-3 because there are column of deadlines, penalty costs, and prod. names)
    num_prod = len(df.axes[0])
    num_prod_lines = (len(df.axes[1])-3)

    # Indices:
    # Production lines (l) and products (p)
    line_headers = df.columns.tolist()[1:num_prod_lines+1]
    product_list = df["Product"].tolist()

    # Parameters:
    # Deadlines (d_p) & penalty costs (c_p)
    deadlines = df["deadline"]
    penalty_costs = df["penalty cost"]