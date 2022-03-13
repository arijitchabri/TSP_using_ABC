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


# Generate new solution
def sol_generator(lis):
    random.shuffle(lis)
    return lis


# objective value calculation
def objective_value_calculation(*, path):
    i = path
    objective_val = 0
    for j in range(len(i)):
        if j == 0:
            objective_val = objective_val + table[0][i[j]]
        elif j == len(i) - 1:
            objective_val = objective_val + table[i[j]][0]
        else:
            objective_val = objective_val + table[i[j - 1]][i[j]]
    return objective_val


# fitness value calculation
def fitness_value_calculation(*, objective_value):
    i = objective_value
    fit = 0
    if i > 0:
        fit = (round(1 / (1 + i), 5))
    if i < 0:
        fit = (1 - i)
    return fit


# probability value calculation
def probaility_value_calculation(*, fitness_value, max_fit):
    i = fitness_value
    prob = (round(((0.9 * (i / max_fit)) + 0.1), 10))
    return prob


# initilizing the input

def init():
    make_distance_table(read_data_from_csv("data_12.csv"))
    global food_source, trail, node_list
    node_list = [i for i in range(1, length)]
    i = 0
    for i in range(length):
        food_source.append(sol_generator(node_list)[:])
        trail.append(0)

    f = []  # objective value
    for i in food_source:
        f.append(objective_value_calculation(path=i))
    fit = []  # fitness value

    for i in f:
        fit.append(fitness_value_calculation(objective_value=i))
    max_fit = max(*fit)

    prob = []  # probability value calculation
    for i in fit:
        prob.append(probaility_value_calculation(fitness_value=i, max_fit=max_fit))

    return fit, f, prob, max_fit


def calculation(*, rand_pos, constant, partner, fit, d, emp_bee, pos):
    rand_pos = random.randint(0, length - 2)
    rand_pos2 = random.randint(0, length - 2)
    while rand_pos2 == rand_pos:
        rand_pos2 = random.randint(0, length - 2)
    emp_bee[rand_pos], emp_bee[rand_pos2] = emp_bee[rand_pos2], emp_bee[rand_pos]

    new_f = objective_value_calculation(path=emp_bee)
    new_fit = fitness_value_calculation(objective_value=new_f)
    if new_fit > fit[pos]:
        food_source[pos] = emp_bee
        return True
    return False


def result_formatter(f, fit, trial=None, prob=None):
    data = []
    global food_source, length
    np = length - 1
    if not trial:
        for i in range(0, np):
            data.append([i, food_source[i], f[i], fit[i]])
        print(tabulate(data, headers=["NO", "Food Source", "f", "fit"]))
    else:
        for i in range(0, np):
            data.append([i, food_source[i], f[i], fit[i], prob[i], trial[i]])
        print(tabulate(data, headers=["NO", "Food Source", "f", "fit", "Probability", "Trail"]))
    print("\n")


# ##---------Main Phases---------## #


# perform the employee bee phase
def employee_bees(fit, f, prob):
    global food_source
    print("\n\n:--- We are is employee bee phase ---:\n\n ")
    for i in range(0, 1000):  # here will be the limit register

        for emp_bee in range(len(food_source)):
            partner = random.randint(0, length - 2)
            while partner == emp_bee:
                partner = random.randint(0, length - 2)
            constant = random.randint(-1000, 1000) / 1000
            rand_pos = random.randint(0, length - 2)
            flag = calculation(rand_pos=rand_pos, constant=constant,
                                                        partner=partner,
                                                        fit=fit, d=length,
                                                        emp_bee=food_source[emp_bee], pos=emp_bee)

            if flag:
                trail[emp_bee] = 0
                new_f = objective_value_calculation(path=food_source[emp_bee])
                new_fit = fitness_value_calculation(objective_value=new_f)
                f[emp_bee] = new_f
                fit[emp_bee] = new_fit
                max_fit = max(*fit)
                prob[emp_bee] = ((0.9 * (fit[emp_bee] / max_fit)) + 0.1)

            else:
                trail[emp_bee] = trail[emp_bee] + 1
        print(f"""Cycle {i + 1}""")
        result_formatter(f, fit, trail, prob)

    print("After completing the employee bee phase the results are : ")
    result_formatter(f, fit, trail, prob)
    return


# preform the onlooker_bee phase
def onlooker_bees(fit, f, prob):
    print("\n\n:--- We are is onlooker bee phase ---:\n\n ")

    for i in range(0, 1000):  # here will be the limit register

        for onlooker_bee in range(len(food_source)):
            partner = onlooker_bee
            partner2 = random.randint(0, length - 2)
            bee_prob = random.randint(0, 1000) / 1000
            while bee_prob > prob[partner]:
                partner = partner + 1
                if partner > length - 2:
                    partner = 0
                bee_prob = random.randint(0, 1000) / 1000

            constant = random.randint(-1000, 1000) / 1000
            rand_pos = random.randint(0, length - 2)

            flag = calculation(rand_pos=rand_pos, constant=constant,
                                                        partner=partner2,
                                                        fit=fit, d=length,
                                                        emp_bee=food_source[partner], pos=partner)

            if flag:
                trail[partner] = 0
                new_f = objective_value_calculation(path=food_source[partner])
                new_fit = fitness_value_calculation(objective_value=new_f)
                f[partner] = new_f
                fit[partner] = new_fit
                max_fit = max(*fit)
                prob[partner] = ((0.9 * (fit[partner] / max_fit)) + 0.1)
            else:
                trail[partner] = trail[partner] + 1
        print(f"""Cycle {i + 1}""")
        result_formatter(f, fit, trail, prob)


def scout_bees(fit, f, prob):
    global food_source, trail, length
    print("\n\n:--- We are is onlooker bee phase ---:\n\n ")
    max_trial = max(*trail)
    if max_trial < 4:
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
    employee_bees(fit, f, prob)
    onlooker_bees(fit, f, prob)
    max_trial = max(*trail)

    if max_trial > previous_fit:
        print("New sol is accepted")
        result_formatter(f, fit)

    else:
        print("Previous sol was good")
        food_source[rand_selector] = previous_solution
        result_formatter(f, fit)
    min_f = min(*f)
    print("The solution is : ", min_f)
    for i in range(length - 2):
        if f[i] == min_f:
            path = food_source[i]
    else:
        path = food_source[rand_selector]
    print("The path is : ", path)


class ABC:
    global food_source, trail
    fit, f, prob, max_fit = init()
    employee_bees(fit, f, prob)
    onlooker_bees(fit, f, prob)
    scout_bees(fit, f, prob)

