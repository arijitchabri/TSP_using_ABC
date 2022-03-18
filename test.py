import csv
from math import sqrt
import random
from tabulate import tabulate

# initilizing the global variables

length = 0  # the node number
trail = []  # this is the trail counter
table = []  # this is the table matrix where the distance from each co-ordinate is stored
food_source = []  # this is the path list
node_list = [] # just to take the list variables


# taking the input from file and making it a distance matrix

def read_data_from_csv(file_name):
    data_list = []
    with open(file_name) as f:
        reader = csv.reader(f)
        data_list = [[int(s) for s in row.split(',')] for row in f]
    return data_list


def get_distance_between_nodes(n1, n2):
    dist = sqrt(((n1[0] - n2[0]) ** 2) + ((n1[1] - n2[1]) ** 2))
    return round(dist, 3)


# making the distance table

def make_distance_table(data_list):
    global length
    global table
    length = len(data_list)

    table = [[get_distance_between_nodes(
        data_list[i], data_list[j])
        for i in range(0, length)] for j in range(0, length)]
    return table

def init():
    make_distance_table(read_data_from_csv("data_12.csv"))
    global food_source, trail, node_list

def objective_value_calculation(*, path):
    i = path
    objective_val = 0
    for j in range(len(i)):
        if j == 0:
            pass
        else:
            objective_val = objective_val + table[i[j - 1]][i[j]]
        objective_val = objective_val + table[i[- 1]][i[0]]
    return objective_val

init()
print(table)
a = sqrt(((3-4) ** 2) + ((3-1) ** 2))
print(read_data_from_csv("data_12.csv"))
print(a)
print(objective_value_calculation(path = [9, 1, 11, 4, 10, 6, 7, 2, 5, 8, 3, 0, 9]))