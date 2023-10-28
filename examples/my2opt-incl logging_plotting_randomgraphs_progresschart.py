# Solving Traveling Salesman Problem by applying Discrete Improving Search (local search)
# Neighborhood structure/Move: 2-exchange
# - remove two arcs, not sharing a node -> three paths
# - reconnect the three paths and form a new dicycle, by inserting two arcs

import random
import logging
import matplotlib.pyplot as plt
import time

logger = logging.getLogger(name='2opt-logger')
logging.basicConfig(level=logging.DEBUG,
                    format='[%(asctime)s] %(message)s',
                    handlers=[logging.FileHandler("2-opt_debug-my.log")])

def euclidean_distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def total_distance(tour, points):
    distance = 0
    for i in range(len(tour)):
        distance += euclidean_distance(points[tour[i]], points[tour[(i + 1) % len(tour)]])
    return distance

def two_opt(tour, points, iteration_log):
    improved = True
    iteration = 0
    iteration_log.append((iteration,total_distance(tour, points)))
    while improved:
        improved = False
        total_distance_tour = total_distance(tour, points)
        logger.debug(msg=f"tour has total distance: {total_distance_tour}")
        i = 1
        while ((i <= len(tour)-2) and not(improved)):
            j = i+1
            while((j <= len(tour)) and not(improved)): 
                if j - i == 1:
                    j += 1
                    continue  # No need to reverse two consecutive edges
                new_tour = tour[:]
                new_tour[i:j] = reversed(tour[i:j])
                total_distance_new_tour = total_distance(new_tour, points)
                if total_distance(new_tour, points) < total_distance(tour, points):
                    logger.debug(msg=f"new tour has total distance: {total_distance_new_tour}, so: Improvement for i,j={i},{j}")
                    tour = new_tour
                    logger.debug(msg=f"tour updated: tour={tour}")
                    improved = True
                    iteration_log.append((iteration+1,total_distance_new_tour))
                    iteration += 1
                else:
                    logger.debug(msg=f"new tour has total distance: {total_distance_new_tour}, so:No improvement for i,j={i},{j}")
                j += 1
            i += 1
    return tour, iteration_log

def main():
    # Define a list of points (coordinates) for the TSP
    number_of_points = 100
    points = []
    for i in range(number_of_points):
        x = random.uniform(0,100)
        y = random.uniform(0,100)
        points.append((x,y))

    # Apply Nearest Neighbor (greedy constructive heuristic)
    # ---
    nn_tour = []
    in_tour = [False]*len(points)

    nn_tour.append(0) # initialize the nn-tour: 0 is only location in tour
    in_tour[0] = True
    last_added = 0
    for i in range(len(points)-1):
        # determine location not yet in tour closest to last added location
        minimal_distance = 424242424242424 # very big number
        for j in (range(len(points))):
            if not(in_tour[j]) and (euclidean_distance(points[last_added],points[j]) < minimal_distance):
                    candidate = j
                    minimal_distance = euclidean_distance(points[last_added],points[j])
        nn_tour.append(candidate)
        in_tour[candidate] = True
        last_added = candidate

    # Create an initial tour (random permutation of points)
    # ---
    tour = list(range(len(points)))
    random.shuffle(tour) 
 
    olddistance = total_distance(tour, points)
    oldtour = tour[:]
    logger.debug(msg=f"Initial solution: Tour={tour}")

    # Apply the 2-opt heuristic to improve the tour
    # ---
    iteration_log = []
    start_time = time.time()
    tour, iteration_log = two_opt(tour, points, iteration_log)
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Calculate and print the total distance of the optimized tour
    distance = total_distance(tour, points)
    logger.info(msg=f"Optimized tour: {tour}")
    logger.info(msg=f"Total distance: {distance}")

    # Plot two figures: one with the optimized route and one with the progress of the heuristic
    # ===

    # Figure 1: Optimized route
    # ---
    # Separate the x and y values into separate lists
    x = [coord[0] for coord in points]
    y = [coord[1] for coord in points]

    # Create a scatter plot
    plt.figure(1)
    plt.scatter(x, y)
    plt.xlabel('X-axis Label')
    plt.ylabel('Y-axis Label')

    # Add lines between consecutive points based on the route
    for i in range(1, len(points)):
        x1, y1 = points[tour[i - 1]]
        x2, y2 = points[tour[i]]
        plt.plot([x1, x2], [y1, y2], 'b-')  # 'b-' specifies blue solid line
    x1, y1 = points[tour[len(points)-1]]
    x2, y2 = points[tour[0]]
    plt.plot([x1, x2], [y1, y2], 'b-')  # 'b-' specifies blue solid line

    for i in range(1, len(points)):
        x1, y1 = points[nn_tour[i - 1]]
        x2, y2 = points[nn_tour[i]]
        plt.plot([x1, x2], [y1, y2], 'r-',linewidth=1)  
    x1, y1 = points[nn_tour[len(points)-1]]
    x2, y2 = points[nn_tour[0]]
    plt.plot([x1, x2], [y1, y2], 'r-',linewidth=1)  

    for i in range(1, len(points)):
        x1, y1 = points[oldtour[i - 1]]
        x2, y2 = points[oldtour[i]]
        plt.plot([x1, x2], [y1, y2], 'g--',linewidth=0.25)  # 'b-' specifies blue solid line
    x1, y1 = points[oldtour[len(points)-1]]
    x2, y2 = points[oldtour[0]]
    plt.plot([x1, x2], [y1, y2], 'g--', linewidth=0.25)  # 'b-' specifies blue solid line


    plt.title(f'Tour with {len(tour)} nodes improved by 2-opt from {olddistance:.2f} to {distance:.2f} in {elapsed_time:.3f} seconds')

    # Figure 2: Heuristic progress
    plt.figure(2)
    x = [ilog[0] for ilog in iteration_log]
    y = [ilog[1] for ilog in iteration_log]
    plt.plot(x, y)

    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.title(f'Progress of 2-opt heuristic applied to {len(tour)} nodes')

    # Show both figures
    plt.show()

if __name__ == "__main__":
    main()
