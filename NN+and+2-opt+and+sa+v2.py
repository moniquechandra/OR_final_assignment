# Solving Traveling Salesman Problem by applying Discrete Improving Search (local search)
# Neighborhood structure/Move: 2-exchange
# - remove two arcs, not sharing a node -> three paths
# - reconnect the three paths and form a new dicycle, by inserting two arcs

import copy
import csv                          # for exporting instances
import logging
import math
import matplotlib.pyplot as plt     # for visualization of the tours
import random
import time

random.seed(42)
logger = logging.getLogger(name='nn-2opt-sa-v2-logger')
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(message)s',
                    handlers=[logging.FileHandler("nn-2opt-sa-ga-v2.log")])

MYVERYBIGNUMBER = 424242424242
MYVERYSMALLNUMBER = 1e-4

# INSTANCE CONSTANTS
NUMPOINTS = 50

# SIMULATED ANNEALING CONSTANTS
COOLINGRATE = 0.995
INITIALTEMPERATURE = 1500.0
MAXITERATIONS = 50000
NUMITERATIONSATTEMP = 500
MYSASEED = 84

# GENETIC ALGORITHM CONSTANTS
GENERATIONS = 100
MAXNUMIMPROVEMENTS = 100
MUTATIONRATE = 0.2
POPULATIONSIZE = 50

class Instance:
    def __init__(self, locations, distance):
        # locations is a list of (x,y) coordinates, representing the n locations 
        # distance is an dictionary mapping a (fromLocation,toLocation) pair onto a decimal value
        self.locations = locations
        self.distance = distance

    def getNumLocations(self):
        return len(self.locations)

    def getLocations(self):
        return self.locations

    def getDistance(self, fromLocation, toLocation):
        keyToRetrieve = (fromLocation,toLocation)
        return self.distance[keyToRetrieve]
    
    def exportToTsv(self, filename):
        data = self.locations

        tsv_file_path = f'{filename}.tsv'

        # Open the TSV file in write mode
        with open(tsv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file, delimiter='\t')  # Use '\t' as the delimiter


            # Write the header row if needed
            # writer.writerow(['X', 'Y'])  # Uncomment this line if you want a header row

            # Write the data
            for x, y in data:
                writer.writerow([x, y])

class Solution:
    def __init__(self, instance, tour):
        self.instance = instance
        self.tour = copy.deepcopy(tour)

        # calculate total distance of tour
        self.totalDistance = 0
        for i in range(len(self.tour)):
            fromLocation = self.instance.locations[self.tour[i]]
            toLocation = self.instance.locations[self.tour[(i + 1) % len(self.tour)]]
            self.totalDistance += self.instance.distance[fromLocation, toLocation]

    def getTour(self):
        return self.tour

    def getTotalDistance(self):
        return self.totalDistance

def euclidean_distance(point1, point2):
    # to calculate the euclidean distance between two given points
    x1, y1 = point1
    x2, y2 = point2
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

def nearest_neighbor(instance):
    # constructive heuristic for generating a tour for a given traveling salesman problem instance
    # algorithm runs in O(n^2) time
    # input: a traveling salesman problem instance (locations, distances)
    # returns  
    #   - a (feasible) tour visiting all locations in the instance
    #   - the total distance of the tour
    points = instance.locations
    distance = instance.distance

    logger.debug(msg=f"Apply Nearest Neighbor (NN)")        
    startTime = time.time()
    nnTour = []
    inTour = [False]*len(points)

    # initialize the nn-tour: 0 is only location in tour
    nnTour.append(0) 
    inTour[0] = True
    lastAdded = 0
    logger.debug(msg=f"Initialize NN tour: start with location 0")    

    # next, assign all remaining locations
    for i in range(len(points)-1):
        # determine location not yet in tour closest to last added location
        minDistance = MYVERYBIGNUMBER # very big number
        for j in (range(len(points))):
            if not(inTour[j]) and (distance[points[lastAdded],points[j]] < minDistance):
                    candidate = j
                    minDistance = distance[points[lastAdded],points[j]]
        nnTour.append(candidate)
        inTour[candidate] = True
        lastAdded = candidate
        logger.debug(msg=f"Add location {candidate} and arc ({lastAdded},{candidate}) with distance {minDistance:.2f} to tour")    
    endTime = time.time()

    nnSolution = Solution(instance,nnTour)
    totalDistanceNNSolution = nnSolution.getTotalDistance()
    logger.info(msg=f"NN tour has distance {totalDistanceNNSolution:.2f}; time: {endTime-startTime:.2f}")    

    return nnSolution, totalDistanceNNSolution

def two_opt(instance,currentSolution,type):
    # improving search heuristic for improving a given tour (currentSolution) for a given traveling salesman problem instance
    # algorithm runs in exponential time
    # input: a traveling salesman problem instance (locations, distances), a tour currentSolution, 
    #       and type: a description how the currentSolution was computed (randomly, nearest neighbor, ...)  
    # returns  
    #       - a (feasible) 2-optimal tour visiting all locations in the instance
    #       - the total distance of the 2-optimal tour (say: l)
    #       any other tour which differs two edges from the 2-optimal tour has length >= l     
    startTime = time.time()
    improved = True
    while improved:
        improved = False
        tour = currentSolution.getTour()
        totDistCurrentSolution = currentSolution.getTotalDistance()
        logger.debug(msg=f"Initial tour of type {type} has total distance: {totDistCurrentSolution}")
        i = 1
        while ((i <= len(tour)-2) and not(improved)):
            j = i+1
            while((j <= len(tour)) and not(improved)): 
                if j - i == 1:
                    j += 1
                    continue  # No need to reverse two consecutive edges
                newTour =  tour[:]
                newTour[i:j] = reversed(tour[i:j])
                neighborSolution = Solution(instance,newTour) 
                totDistNeighborSolution = neighborSolution.getTotalDistance()
                if totDistNeighborSolution < totDistCurrentSolution:
                    logger.debug(msg=f"neighbor tour has total distance: {totDistNeighborSolution}, so: Improvement for i,j={i},{j}")
                    tour = newTour
                    currentSolution = Solution(instance,tour)
                    print(f"2-opt: New current solution has value {totDistNeighborSolution:.2f}",end='\r')
                    improved = True
                else:
                    logger.debug(msg=f"neighbor tour has total distance: {totDistNeighborSolution}, so:No improvement for i,j={i},{j}")
                j += 1
            i += 1
    endTime = time.time()

    twoOptSolution = Solution(instance,tour)
    totalDistanceTwoOptSolution = twoOptSolution.getTotalDistance()
    logger.info(msg=f"2-opt tour of type {type} has total distance: {totalDistanceTwoOptSolution}; time: {endTime-startTime:.6f}")
    print("\n")

    return twoOptSolution, totalDistanceTwoOptSolution

def simulated_annealing_two_exchange(instance,currentSolution,type,rngSeed):
    # meta heuristic for improving a given tour (currentSolution) for a given traveling salesman problem instance
    # algorithm runs in exponential time
    # input: a traveling salesman problem instance (locations, distances), a tour currentSolution, 
    #       type: a description how the currentSolution was computed (randomly, nearest neighbor, ...) 
    #       rngSeed: the seed for initializing the random number generator 
    # function produces a graph showing the progress of the current solution's objective value when plotted against the iteration counter
    # returns  
    #       - a (feasible) 2-optimal tour visiting all locations in the instance
    #       - the total distance of the 2-optimal tour (say: l)
    #       any other tour which differs two edges from the 2-optimal tour has length >= l         
    random.seed(rngSeed)
    iterationLog = []
   
    tour = currentSolution.getTour()
    totDistCurrentSolution = currentSolution.getTotalDistance()
    logger.debug(msg=f"Initial tour of type {type} has total distance: {totDistCurrentSolution}")

    bestSolution = currentSolution
    totDistBestSolution = totDistCurrentSolution

    startTime = time.time()
    temperature = INITIALTEMPERATURE
    iteration = 0

    logToInsert = (iteration,totDistCurrentSolution,totDistBestSolution,temperature)
    iterationLog.append(logToInsert)

    while iteration < MAXITERATIONS:
        iterationsAtTemp = 0
        while iterationsAtTemp < NUMITERATIONSATTEMP:
            tour = currentSolution.getTour()
            totDistCurrentSolution = currentSolution.getTotalDistance()
            logger.debug(msg=f"Initial tour of type {type} has total distance: {totDistCurrentSolution}")

            # draw random pair i,j
            while True:
                i,j = random.sample(range(len(tour)),2) # two random numbers
                if (i>0) and (j>i+1):
                    break

            # j>i+1, so the 2-exchange based on i and j is relevant
            newTour =  tour[:]
            newTour[i:j] = reversed(tour[i:j])
            neighborSolution = Solution(instance,newTour) 
            totDistNeighborSolution = neighborSolution.getTotalDistance()
            deltaDist = totDistNeighborSolution-totDistCurrentSolution
            if deltaDist < 0 or random.random() < math.exp(-deltaDist/temperature):
                # accept neighbor solution
                logger.debug(msg=f"neighbor tour has total distance: {totDistNeighborSolution}, so: Improvement for i,j={i},{j}")
                tour = newTour
                currentSolution = Solution(instance,tour)
                totDistCurrentSolution = totDistNeighborSolution

                if totDistCurrentSolution < totDistBestSolution:
                    # update best solution
                    bestSolution = Solution(instance,tour)
                    totDistBestSolution = totDistCurrentSolution
            else:
                logger.debug(msg=f"neighbor tour has total distance: {totDistNeighborSolution}, so:No improvement for i,j={i},{j}")

            # to visualize the solution method's progress at the end,
            # record the iteration counter, objective value (current and best solution) and temperature 
            logToInsert = (iteration,totDistCurrentSolution,totDistBestSolution,temperature)
            iterationLog.append(logToInsert)
            if iteration%10 == 0:
                print(f"Iteration {iteration:8}, temp {temperature:.4f} current {totDistCurrentSolution:.2f} best {totDistBestSolution:.2f}", end='\r')

            logger.debug(msg=f"Iteration {iteration+1:3n}, temp: {temperature:.2f}, distance (curr): {totDistCurrentSolution:.2f}, (best): {totDistBestSolution:.2f}")

            iteration += 1
            iterationsAtTemp += 1
        temperature *= COOLINGRATE

    # finalize by running 2-opt -> this will guarantee a 2-opt solution
    simulatedAnnealingSolution, totDistSimulatedAnnealing = two_opt(instance, bestSolution,"SA")    
    endTime = time.time()

    logger.info(msg=f"Simulated annealing tour of type {type} has total distance: {totDistSimulatedAnnealing}; time: {endTime-startTime:.2f}")

    # visualize iteration log
    plt.figure(0)
    x = [ilog[0] for ilog in iterationLog]
    y1 = [ilog[1] for ilog in iterationLog]
    y2 = [ilog[2] for ilog in iterationLog]
    y3 = [ilog[3] for ilog in iterationLog]

    plt.plot(x, y1)
    plt.plot(x, y2)
    plt.plot(x, y3)
    plt.xlabel('Iteration')
    plt.ylabel('Distance')
    plt.title(f'Progress of SA heuristic applied to {len(tour)} nodes')

    return simulatedAnnealingSolution, totDistSimulatedAnnealing

def plotSATSPSolutions(instance, initialSolution, bestSolution, type):
    numPoints = instance.getNumLocations()
    points = instance.getLocations()

    initialTour = initialSolution.getTour()
    bestTour = bestSolution.getTour()

    if numPoints<500:
        # If the instance is not too complex (big): Plot the instance and the solutions
        # ---

        # Separate the x and y values into separate lists
        x = [coord[0] for coord in points]
        y = [coord[1] for coord in points]

        # In Figure 1, we show both the random solution and the NN solution
        plt.figure(1)
        plt.scatter(x, y)
        plt.xlabel('X-axis Label')
        plt.ylabel('Y-axis Label')
        for i in range(1, len(points)):
            x1, y1 = points[initialTour[i - 1]]
            x2, y2 = points[initialTour[i]]
            plt.plot([x1, x2], [y1, y2], 'g--',linewidth=0.1)  
        x1, y1 = points[initialTour[len(points)-1]]
        x2, y2 = points[initialTour[0]]
        plt.plot([x1, x2], [y1, y2], 'g--',linewidth=0.1)        
        for i in range(1, len(points)):
            x1, y1 = points[bestTour[i - 1]]
            x2, y2 = points[bestTour[i]]
            plt.plot([x1, x2], [y1, y2], 'b-',linewidth=1)  
        x1, y1 = points[bestTour[len(points)-1]]
        x2, y2 = points[bestTour[0]]
        plt.plot([x1, x2], [y1, y2], 'b-',linewidth=1)  
        plt.title(f'SA: Solutions on {numPoints} nodes; Initial: {initialSolution.getTotalDistance():.2f}, Best: {bestSolution.getTotalDistance():.2f} , {type}')

def main():
    # Solution method will create an instance of the traveling salesman problem
    # Generate two initial solutions for the instance (randomly generated, and constructed via nearest neighbor)
    # Improves the initial solution by just 2-opt
    # or by simulated annealing (followed by 2-opt)
    # So: four ways to create a good feasible tour
    # - Random / 2-opt
    # - Random / SA (+2-opt)
    # - Nearest Neighbor / 2-opt
    # - Nearest Neighbor / SA (+2-opt)
    # Method will compare these four solutions 

    #
    # Instance: Define a random instance
    # ---
    numPoints = NUMPOINTS
    points = []
    distance = {}
    for i in range(numPoints):
        x = random.uniform(0,100)
        y = random.uniform(0,100)
        points.append((x,y))

    # Calculate the distance matrix, given the points' (x,y)-coordinates
    for p1 in range(len(points)):
        for p2 in range(len(points)):
            point1 = points[p1]
            point2 = points[p2]
            dist = euclidean_distance(point1,point2)
            keyToRetrieve = (point1,point2)
            distance[keyToRetrieve] = dist
    
    # create the instance
    instance = Instance(points,distance)
    instance.exportToTsv(f"TSP-R-{numPoints}")      # store the traveling salesman problem instance as a tab-separated value file
    logger.info(msg=f"Random instance with {numPoints} locations")    

    # Option 1: Initial solution is randomly generated tour
    # ---
    startTime = time.time()
    randomTour = list(range(len(points)))
    random.shuffle(randomTour)
    endTime = time.time()

    randomSolution = Solution(instance,randomTour) 
    totalDistanceRandomSolution = randomSolution.getTotalDistance()
    logger.info(msg=f"Random tour has distance {totalDistanceRandomSolution:.2f}; time: {endTime-startTime:.2f}")    

    # Improve the randomly generated tour by applying 2-opt
    twoOptSolutionRnd, totDistTwoOptRnd = two_opt(instance, randomSolution,"RND")
    twoOptRndtour = twoOptSolutionRnd.getTour()

    # Improve the randomly generated tour by applying simulated Annealing 
    saSolutionRnd, totDistSARnd = simulated_annealing_two_exchange(instance,randomSolution,"RND",MYSASEED)
    saRndtour = saSolutionRnd.getTour()

    """
    # Option 2: Initial tour is tour constructed by Nearest Neighbor
    # ---
    nnSolution, totalDistanceNNSolution = nearest_neighbor(instance)
    nnTour = nnSolution.getTour()

    # Apply 2-opt to NN tour
    twoOptSolutionNN, totDistTwoOptNN = two_opt(instance, nnSolution,"NN")
    twoOptNNtour = twoOptSolutionNN.getTour()

    # Simulated Annealing on NN tour
    saSolutionNN , totDistSANN = simulated_annealing_two_exchange(instance,nnSolution,"NN",MYSASEED)
    saNNtour = saSolutionNN.getTour()
    """

    plotSATSPSolutions(instance,randomSolution,saSolutionRnd,"RND")
    #plotSATSPSolutions(instance,nnSolution,saSolutionNN,"NN")
    plt.show()

if __name__ == "__main__":
    main()
