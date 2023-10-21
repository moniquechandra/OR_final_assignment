import pandas as pd

def read_data_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df

# WILR: based on chatgpt
# question: i would like to program a greedy constructive heuristic for the knapsack problem in python. give me code for this, please.

# chatgpt's remark:
# In this code, we first sort the items by their value-to-weight ratio in descending order, 
# which means we prioritize items with a higher value-to-weight ratio. 
# Then, we iterate through the sorted items and add them to the knapsack if they can fit without exceeding the capacity.

def knapsack_greedy(items, capacity):
    # Sort items by value-to-weight ratio in descending order
    items.sort(key=lambda x: x[1] / x[0], reverse=True)
    
    # WILR: initialize (empty knapsack, no decisions made)
    knapsack = []
    knapsack_value = 0
    knapsack_weight = 0
    
    for item in items:
        # WILR: consider the next item (not yet in knapsack), according to descending value-to-weigth
        if knapsack_weight + item[0] <= capacity:
            # WILR: the item can be added to the knapsack (fits), so: add item to knapsack
            knapsack.append(item)
            knapsack_weight += item[0]
            knapsack_value += item[1]
    
    return knapsack, knapsack_value

# Example usage:
# WILR: for each item i, we are given two numbers (w_i, v_i), representing the item weight and item value
if __name__ == "__main__":
    filePathInstance = "simple instance.xlsx"

    dfInstance = read_data_from_excel(filePathInstance)

    items = []
    for index, row in dfInstance.iterrows():
        item = row["item"]
        weight = row["weight"]
        value = row["value"]
        item = (weight,value)
        items.append(item)
        if index == 0:
            capacity = row["capacity"]


    result, total_value = knapsack_greedy(items, capacity)

    print("Selected items:", result)
    print("Total value:", total_value)