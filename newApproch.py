import csv
from math import sqrt
import random
from tabulate import tabulate
from time import perf_counter
import sys

# initializing the global variables

length = 0  # the total nodes.
trail = []  # this is the trail counter.
table = []  # this is the table matrix where the distance from each co-ordinate is stored.
food_source = []  # this is the path list.
node_list = []  # just to take the list variables.
limit = 1000 # this is the limit constant.
trail_limit = 4  # this is the trail limit.
change = []  # keeping track of the changed values
best_path = [] # keeping track of the best path
best_f = 9999


# taking the input from file and making it a distance matrix

def read_data_from_csv(file_name):
    """
    Reads from the csv converts it to a data list returns it.
    :param file_name: The csv file where our co-ordinates are stored.
    :return: Returning a data list after reading the csv file.
    """
    data_list = []
    with open(file_name) as f:
        reader = csv.reader(f)
        data_list = [[int(s) for s in row.split(',')] for row in f]
    return data_list


def get_distance_between_nodes(n1, n2):
    """
    Calculating the distance between two nodes or cities.
    :param n1: Co-ordinate of point 1.
    :param n2: Co-ordinate of point 2.
    :return: The distance between two point.
    """
    dist = sqrt(((n1[0] - n2[0]) ** 2) + ((n1[1] - n2[1]) ** 2))
    return round(dist, 3)


# making the distance table

def make_distance_table(data_list):
    """
    Creating the path cose table from one node to other nodes.
    :param data_list: Converted data list from the csv
    :return: Each point traveling cost form every point.
    """
    global length
    global table
    length = len(data_list)

    table = [[get_distance_between_nodes(
        data_list[i], data_list[j])
        for i in range(0, length)] for j in range(0, length)]
    return table


# Generate new solution
def sol_generator(lis):
    """ This shuffles the list and return us the food path and as
    the journey starts from the depo zero is the starting node.
    """
    random.shuffle(lis)
    nlis = [0, *lis]
    return nlis


# objective value calculation
def objective_value_calculation(*, path):
    """
    Objective value is calculated by adding up the travel cost.
    :param path: is the path who's objective value is to be calculated.
    :return: returns the calculated objective value.
    """
    i = path
    objective_val = 0
    for j in range(len(i)):
        if j == 0:
            pass
        else:
            objective_val = objective_val + table [ i [j - 1] ] [i [j] ]
    objective_val = objective_val + table[i[- 1]][i[0]]
    return objective_val


# fitness value calculation
def fitness_value_calculation(*, objective_value):
    """
    Calculating the fitness value of a path.
    :param objective_value: any objective value for whom we are calculating the fitness value.
    :return:
    """
    i = objective_value
    fit = 0
    if i > 0:
        fit = (round(1 / (1 + i), 3))
    if i < 0:
        fit = (1 - i)
    return fit


# probability value calculation
def probability_value_calculation(*, objective_value, min_f):
    """
    Calculating the probability of the food source it determine whether an onlooker bee will choose this or not.
    :param objective_value: The objective of the current path.
    :param min_f: min objective value of all the food source.
    :return:
    """
    try:
        prob = (((0.9 * (min_f / objective_value)) + 0.1))
    except ZeroDivisionError:
        prob = .0000000001
    return prob


# initializing the input

def init(food_source1 = None):
    """
    Some stuff are going on here like :
    1. Creating the food sources, or we may say the paths.
    2. Storing the paths, calculating and storing of objective,  fitness, probability, trail counter, min fitness
    :return: fitness, objective, probability, min fitness
    """
    make_distance_table(read_data_from_csv("data_12.csv"))
    print("The distance table is : \n")
    for i in table:
        print(i, "\n")
    print("\n\n")
    global food_source, trail, node_list
    node_list = [i for i in range(1, length)]
    if food_source1:
        food_source = food_source1
    else:
        for i in range(0, length):
            food_source.append(sol_generator(node_list)[:])
            trail.append(0)
            change.append("None")
        print("The initial food source list is :- ")
    for i in food_source:
        print(i)
    f = []  # objective value
    for i in food_source:
        f.append(objective_value_calculation(path=i))
    fit = []  # fitness value

    for i in f:
        fit.append(fitness_value_calculation(objective_value=i))
    min_f = min(*f)

    prob = []  # probability value calculation
    for i in f:
        prob.append(probability_value_calculation(objective_value=i, min_f=min_f))

    return fit, f, prob, min_f


def calculation(*, f, path, pos):
    """
    This is not the typical way of ABC cause that calculate the new path in fraction but as we can not make our path '
    a fraction that's why we are using this approach.
    The approach is to generate two random numbers and swapping the nodes.
    :param f: Objective value of the current path.
    :param path: The current path.
    :param pos: The position of the current path in the food source list.
    :return: If better solution is generated then true is returned else false.
    """
    global best_f, best_path
    rand_pos = random.randint(1, length - 2)
    rand_pos2 = random.randint(1, length - 2)
    while rand_pos2 == rand_pos:
        rand_pos2 = random.randint(1, length - 2)
    # path[rand_pos], path[rand_pos2] = path[rand_pos2], path[rand_pos]
    new_path = [*path]
    new_path[rand_pos], new_path[rand_pos2] = path[rand_pos2], path[rand_pos]

    cng = (path[rand_pos], path[rand_pos2])
    new_f = objective_value_calculation(path=new_path)
    if best_f > new_f:
        best_path = new_path
        best_f = new_f
    if new_f < f[pos]:
        food_source[pos] = new_path
        return True, cng
    return False, None


def result_formatter(f, fit, trial=None, prob=None):
    """
    Printing the values in a tabular way by using the "Tabulate" module.
    :param f: Objective value list.
    :param fit: Fitness value list.
    :param trial: Trial counter list.
    :param prob: Probability value list.
    :return: NONE
    """
    data = []
    global food_source, length
    np = length
    if not trial:
        for i in range(0, np):
            data.append([i, food_source[i], f[i], fit[i], change[i]])
        print(tabulate(data, headers=["NO", "Food Source", "f", "fit", "Change"]))
    else:
        for i in range(0, np):
            data.append([i, food_source[i], f[i], fit[i], prob[i], trial[i], change[i]])
        print(tabulate(data, headers=["NO", "Food Source", "f", "fit", "Probability", "Trail", "Change"]))
    print("\n")
    return


# ##---------Main Phases---------## #


# perform the employee bee phase
def employee_bees(fit, f, prob):
    """
    The employee bee phase is calculated here. We are directing each path to the calculation function then
    trying to make it a better solution.
    In success, we are resetting the trail to zero if not then increasing the trial.
    :param fit: Fitness value list.
    :param f: Objective value list.
    :param prob: Probability value list.
    :return: None.
    """
    global food_source
    print("\n\n:--- We are in employee bee phase ---:\n\n ")
    print("The initial food source list and other parameters are  :- \n")
    result_formatter(f, fit, trail, prob)
    for c in range(0, limit):  # here will be the limit register

        for pos in range(len(food_source)):
            path = food_source[pos]
            flag, cng = calculation(f=f, path=food_source[pos], pos=pos)

            if flag:
                trail[pos] = 0
                new_f = objective_value_calculation(path=food_source[pos])
                new_fit = fitness_value_calculation(objective_value=new_f)
                f[pos] = new_f
                fit[pos] = new_fit
                min_f = min(*f)
                change[pos] = cng
                for i in range(len(food_source)):
                    prob[i] = probability_value_calculation(objective_value=f[i], min_f=min_f)

            else:
                trail[pos] = trail[pos] + 1
                food_source[pos] = path
                change[pos] = "None"
        print(f"""Cycle {c + 1}""")
        result_formatter(f, fit, trail, prob)

    print("After completing the employee bee phase the results are : ")
    result_formatter(f, fit, trail, prob)
    return


# preform the onlooker_bee phase
def onlooker_bees(fit, f, prob):
    """
    Onlooker bee phase is calculated here.
    First we are generating a bee probability to exploit the food source, and looping the process until we get a
    food source to be exploited. Then we are directing each path to the calculation function then
    trying to make it a better solution.
    In success, we are resetting the trail to zero if not then increasing the trial.
    :param fit: Fitness value list.
    :param f: Objective value list.
    :param prob: Probability value list.
    :return: None.
    """
    print("\n\n:--- We are is onlooker bee phase ---:\n\n ")

    for c in range(0, limit):  # here will be the limit register
        for onlooker_bee in range(len(food_source)):
            path = onlooker_bee
            bee_prob = random.randint(0, 1000) / 1000
            while bee_prob > prob[path]:
                path = path + 1
                if path > length - 2:
                    path = 0
                bee_prob = random.randint(0, 1000) / 1000
            pre_path = food_source[path]
            flag, cng = calculation(f=f, path=food_source[path], pos=path)

            if flag:
                trail[path] = 0
                new_f = objective_value_calculation(path=food_source[path])
                new_fit = fitness_value_calculation(objective_value=new_f)
                f[path] = new_f
                fit[path] = new_fit
                min_f = min(*f)
                change[path] = cng
                for i in range(len(food_source)):
                    prob[i] = probability_value_calculation(objective_value=f[i], min_f=min_f)
            else:
                trail[path] = trail[path] + 1
                change[path] = "None"
                food_source[path] = pre_path
        print(f"""Cycle {c + 1}""")
        result_formatter(f, fit, trail, prob)


def scout_bees(fit, f, prob):
    """
    Scout bee phase is done here.
    We are comparing the min allowed trail limit and min trail from the food source if the food source trail is
    greater than the trail then it is a good solution as we failed to generate a better solution than it.
    So we are soting it in a variable and  generating a new solution and running the process again from the start
    if new better solution can be produce then population is accepting it else the previous was best.
    So we are keeping the old best solution.
    :param fit: Fitness value list.
    :param f: Objective value list.
    :param prob: Probability value list.
    :return: None.
    """
    global food_source, trail, length
    print("\n\n:--- We are in scout bee phase ---:\n\n ")
    print("The initial food source list and other parameters are  :- \n")
    result_formatter(f, fit, trail, prob)
    max_trial = max(*trail)
    if max_trial < trail_limit:
        print("The sol is : ", best_f)
        print("The best path is : ", best_path)
        return
    max_trial_list = []
    for i in range(len(trail)):
        if trail[i] == max_trial:
            max_trial_list.append(i)
    rand_selector = random.choice(max_trial_list)
    previous_solution = food_source[rand_selector]
    previous_f = f[rand_selector]
    previous_fit = fit[rand_selector]
    food_source[rand_selector] = sol_generator(node_list)
    # f[rand_selector] = objective_value_calculation(path=food_source[rand_selector])
    # fit[rand_selector] = fitness_value_calculation(objective_value=f[rand_selector])
    # min_f = min(*f)
    # for i in range(len(food_source)):
    #     prob[i] = probability_value_calculation(objective_value=f[i], min_f=min_f)
    trail[rand_selector] = 0
    fit, f, prob, min_fit = init(food_source1 = food_source)
    employee_bees(fit, f, prob)
    onlooker_bees(fit, f, prob)
    new_f = min(*f)

    if new_f < previous_f:
        print(f"New sol is accepted\n"
              f"Previous sol was : ", previous_f)

        result_formatter(f, fit)

    else:
        print("Previous sol was good")
        food_source[rand_selector] = previous_solution
        fit[rand_selector] = previous_fit
        f[rand_selector] = previous_f
        result_formatter(f, fit)
    min_f = min(*f)
    print("The solution is : ", min_f)
    print("The path is : ", best_path)



start = perf_counter()
fit, f, prob, min_fit = init()
employee_bees(fit, f, prob)
onlooker_bees(fit, f, prob)
scout_bees(fit, f, prob)
end = perf_counter()
print("Total time taken = ", end - start, " sec")

