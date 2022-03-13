import random



def calculation(*, rand_pos, constant, partner, fit, d, emp_bee, pos):
    new_sol = round(emp_bee[rand_pos] + (constant * (emp_bee[rand_pos] - food_source[partner][rand_pos])))
    while new_sol == emp_bee[rand_pos]:
        constant = random.randint(-1000, 1000) / 1000
        new_sol = round(emp_bee[rand_pos] + (constant * (emp_bee[rand_pos] - food_source[partner][rand_pos])))
    ub, lb = d, 1
    if new_sol > ub:
        new_sol = ub
    if new_sol < lb:
        new_sol = lb

    j = 0
    for i in emp_bee:
        if new_sol == i:
            # swapping the position of the variables
            emp_bee[j], emp_bee[rand_pos] = emp_bee[rand_pos], new_sol
            break
        j += 1
    new_f = objective_value_calculation(path=emp_bee)

    new_fit = fitness_value_calculation(objective_value=new_f)
    if new_fit > fit[pos]:
        return True, new_sol, new_f, round(new_fit, 5)
    return False, 0, 0, 0



def employee_bees(fit, f, prob):
    print("\n\n:--- We are is employee bee phase ---:\n\n ")
    global food_source
    for i in range(0, 4):  # here will be the limit register

        for emp_bee in range(len(food_source)):
            partner = random.randint(0, length - 2)
            while partner == emp_bee:
                partner = random.randint(0, length - 2)
            constant = random.randint(-1000, 1000) / 1000
            rand_pos = random.randint(0, length - 2)
            flag, new_sol, new_f, new_fit = calculation(rand_pos=rand_pos, constant=constant,
                                                        partner=partner,
                                                        fit=fit, d=length,
                                                        emp_bee=food_source[emp_bee], pos=emp_bee)

            if flag:
                food_source[emp_bee][rand_pos] = new_sol
                trail[emp_bee] = 0
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