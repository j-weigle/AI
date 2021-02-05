#-------------------------------------------#
#       Author: Justin Weigle               #
#       Edited: 20 Sept 2019                #
#-------------------------------------------#
#           A* Search Algorithm             #
#-------------------------------------------#

import csv
import math
from collections import defaultdict

def reconstruct_path(came_from, current):
    """
    path reconstruction for A* algorithm
    """
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.insert(0, current)
    return total_path

def astar(edgeweights, start, goal, h):
    """
    A* search algorithm
    """
    # Create needed structures
    open_set = set()
    closed_set = set()
    came_from = {}
    g_score = {}
    f_score = {}

    # initialize all g and f scores to infinity
    for node in edgeweights:
        g_score[node] = math.inf
    for node in edgeweights:
        f_score[node] = math.inf

    open_set.add(start)
    g_score[start] = 0
    if(int(start) < int(goal)):
        f_score[start] = h[start][0][int(goal)-1]
    else:
        f_score[start] = h[goal][0][int(start)-1]

    # find the best path or exhaust the open set
    while open_set:
        # set current as node in open set with lowest f score
        min_score = math.inf
        for node in open_set:
            if float(f_score[node]) < min_score:
                min_score = f_score[node]
                current = node
        if(current == goal):
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        closed_set.add(current)

        for neighbor in edgeweights[current]:
            if neighbor[0] in closed_set:
                continue

            # tentative_g_score is the cost from start to neighbor
            # through current
            tentative_g_score = float(g_score[current]) + float(neighbor[1])
            if tentative_g_score < g_score[neighbor[0]]:
                # this path is better than any previous, remember it
                came_from[neighbor[0]] = current
                g_score[neighbor[0]] = tentative_g_score
                if(int(neighbor[0]) < int(goal)):
                    f_score[neighbor[0]] = (g_score[neighbor[0]] +
                                        float(h[neighbor[0]][0][int(goal)-1]))
                else:
                    f_score[neighbor[0]] = (g_score[neighbor[0]] +
                                        float(h[goal][0][int(neighbor[0])-1]))
                if(neighbor[0] not in open_set):
                    open_set.add(neighbor[0])

    return False

def calc_cost(edgeweights, path, goal):
    """
    calculate the cost of the path found by A*
    """
    cost = 0
    for i in range(0, len(path)):
        if path[i] != goal:
            nn_i = next_node_i(edgeweights, path[i], path[i+1])
            cost += float(edgeweights[path[i]][nn_i][1])

    return cost

def next_node_i(edgeweights, node, next_node):
    """
    find the next node's index in the edgeweights
    file so the cost can be calculated
    """
    for i in range(len(edgeweights[node])):
        if edgeweights[node][i][0] == next_node:
            return i

def get_edgeweights(file_name):
    """
    load in the edgeweights file
    store in defaultdict
    """
    f = open(file_name, 'r')
    reader = csv.reader(f)
    edgeweights = defaultdict(list)
    for row in reader:
        if row:
            edgeweights[row[0]].append([row[1], row[2]])
    f.close()

    return edgeweights

def get_heuristics(file_name):
    """
    load in the heuristics file
    store in defaultdict
    """
    f = open(file_name, 'r')
    reader = csv.reader(f)
    heuristics = defaultdict(list)
    for row in reader:
        if row:
            heuristics[row[0]].append(row[1:])
    f.close()

    return heuristics

def print_results(cost, path):
    """
    print out the results of A* search in a nice formatted way
    """
    print("A* minimum cost path")
    print('[' + str(cost) + ']', end='')
    pretty_path = ''
    for node in path:
        pretty_path += (str(node) + ' - ')
    pretty_path = pretty_path.rstrip("- ")
    print(pretty_path)


if __name__=="__main__":
    file_name = input("Please enter the edgeweight file name:\n")
    file_name += ".csv"
    edgeweights = get_edgeweights(file_name)


    file_name = input("Please enter the heuristics file name:\n")
    file_name += ".csv"
    heuristics = get_heuristics(file_name)

    start = int(input("Please enter the starting node (1-200): "))
    while(start < 1 or 200 < start or type(start) != int):
        print("Starting node not integer from 1-200")
        start = int(input("Please enter the starting node (1-200): "))
    start = str(start)

    goal = int(input("Please enter the goal node (1-200): "))
    while(goal < 1 or 200 < goal or type(goal) != int):
        print("Goal node not integer from 1-200")
        goal = int(input("Please enter the goal node (1-200): "))
    goal = str(goal)

    path = astar(edgeweights, start, goal, heuristics)
    if path:
        cost = calc_cost(edgeweights, path, goal)

    if path:
        print_results(cost, path)
    else:
        print("Failed to find path")
