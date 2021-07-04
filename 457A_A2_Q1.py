# Assignment 2 - 1
# Author: Aish Srinivas
# Date: 17 June 2021
# Spring 2021

from decimal import Decimal
from random import randrange
from random import randint
from random import uniform
from random import random
from numpy import asarray
from numpy import exp
from numpy.random import randn
from numpy.random import rand
from numpy.random import seed
from math import cos
from math import exp
from math import pi
import matplotlib.pyplot as plt
import time

# Plot the results
def plot_my_graph(graph_title, legend_title):
    plt.xlabel('Time (s)')
    plt.ylabel('Cost')
    plt.legend(title = legend_title, bbox_to_anchor = (1.05, 1.0), loc='upper left')
    plt.savefig(graph_title, bbox_inches='tight')
    plt.close()

# cost cost
def cost(x):
    return -cos(x[0]) * cos(x[1]) * exp(-(x[0] - pi) ** 2 - (x[1] - pi) ** 2)


def randrange_float(start, stop, step):
    return randint(0, int((stop - start) / step)) * step + start


# simulated annealing algorithm
def simulated_annealing(iteration, temp, alpha, initial, start_time):

    best_point = initial
    best_f = cost(best_point)
    curr, curr_eval = best_point, best_f

    start_of_experiment = time.perf_counter()

    timestamps = []
    best_points_found = []

    count = 0

    # run the algorithm
    while temp > 0.001:
        for i in range(iteration):

            count+=1

            # Get random neighbour and get value
            next_point = [randrange_float(max(curr[0] - 5, -100), min(curr[0] + 5, 100), 0.1),
                          randrange_float(max(curr[1] - 5, -100), min(curr[1] + 5, 100), 0.1)]
            next_point_f = cost(next_point)

            # get acceptance probability
            try:
                if temp > 0:
                    probability_cost = exp(-(next_point_f - curr_eval) / (alpha*temp))
                else:
                    probability_cost = 0
            except OverflowError:
                probability_cost = 0

            # check if solution is better
            if (next_point_f - curr_eval) < 0:
                best_point, best_f = next_point, next_point_f
                curr, curr_eval = next_point, next_point_f

                # record the timestamp and optimal cost found so far
                timestamps.append(time.perf_counter() - start_of_experiment)
                best_points_found.append(next_point_f)
            else:
                if rand() < probability_cost:
                    curr, curr_eval = next_point, next_point_f

                    # record the timestamp and optimal cost found so far
                    timestamps.append(time.perf_counter() - start_of_experiment)
                    best_points_found.append(next_point_f)
        temp = alpha * temp

    best_point = [round(best_point[0],4), round(best_point[1], 4)]
    return timestamps, best_points_found, best_point, round(best_f, 4)


##############################################################################################################



def main():



    seed(1)
    start_time = time.perf_counter()

    # main bounds and data arys
    bounds = asarray([[-100, 100], [-100, 100]])
    inital_points = []
    inital_temperatures = []
    inital_alpha = []

    # parameter to be changed
    initial = [-100, 100]
    temp = 50
    alpha = 0.95

    # initialise parameters (initial point, initial temperature, annealing rate)
    for i in range(10):
        inital_points.append([round(randrange_float(bounds[0][0], bounds[0][1], 0.01), 2),
                          round(randrange_float(bounds[1][0], bounds[1][1], 0.01), 2)])
        inital_temperatures.append(round(temp, 2))
        inital_alpha.append(round(alpha, 2))

        temp = temp + 100
        alpha -= 0.1

    inital_alpha.sort()

    ##############################################################################################################

    temp = 500
    alpha = 0.95
    iteration = 1000

    # Experiment 1
    print ("Varying initial points ...")
    print("T = " + str(temp))
    print("Annealing Rate = "+ str(alpha))
    for i in inital_points:
        solution_x, solution_y, best_point, best_f = simulated_annealing(iteration, temp, alpha, i, start_time)
        print('Initial Point = %s, f(%s) = %f' % (i, best_point, best_f))

        plt.plot(solution_x, solution_y, label=i)
    print(" ")

    plot_my_graph('Experiment 1', 'Initial Points')

    # Experiment 2
    print ("Varying initial temperatures ...")
    print("Annealing Rate = " + str(alpha))
    print("Initial Point = " + str(initial))
    for i in inital_temperatures:
        solution_x, solution_y, best_point, best_f = simulated_annealing(iteration, i, alpha, initial, start_time)
        print('Initial Temperature = %s, f(%s) = %f' % (i, best_point, best_f))

        plt.plot(solution_x, solution_y, label=i)
    print(" ")

    plot_my_graph('Experiment 2', 'Initial Temperature')


    # Experiment 3
    print ("Varying initial annealing parameter ...")
    print("T = " + str(temp))
    print("Initial Point = " + str(initial))
    for i in inital_alpha:
        solution_x, solution_y, best_point, best_f = simulated_annealing(iteration, temp, i, initial, start_time)
        print('Annealing Rate = %s, f(%s) = %f' % (i, best_point, best_f))

        plt.plot(solution_x, solution_y, label=i)
    print(" ")

    plot_my_graph('Experiment 3', 'Annealing Rate')


if __name__ == "__main__":
    main()