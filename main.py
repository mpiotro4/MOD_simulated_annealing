# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import numpy as np


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def objective(a, b):
    return 40 * a + 30 * b


# Constraints
def constraints(a, b):
    return (a + b <= 12) and (2 * a + b <= 16) and (a >= 0) and (b >= 0)


def simulated_annealing(obj_func, constraint_func, a_bounds, b_bounds, max_iter, initial_temp, alpha):
    # Initialize solution within constraints
    a = np.random.uniform(*a_bounds)
    b = np.random.uniform(*b_bounds)

    while not constraint_func(a, b):
        a = np.random.uniform(*a_bounds)
        b = np.random.uniform(*b_bounds)

    best_solution = current_solution = np.array([a, b])
    best_obj = current_obj = obj_func(a, b)
    current_temp = initial_temp

    for i in range(max_iter):
        next_solution = np.array(current_solution) + np.random.uniform(-1, 1, 2)
        next_solution = np.maximum(next_solution, [a_bounds[0], b_bounds[0]])
        next_solution = np.minimum(next_solution, [a_bounds[1], b_bounds[1]])

        if constraint_func(*next_solution):
            next_obj = obj_func(*next_solution)

            # Decide if we should accept the new solution
            # Avoid large numbers in np.exp() computation
            delta_obj = current_obj - next_obj
            if delta_obj / current_temp < 100:  # adjust the number 100 as needed
                accept = np.exp(delta_obj / current_temp) > np.random.rand()
            else:
                accept = False

            if next_obj > current_obj or accept:
                current_solution = next_solution
                current_obj = next_obj

                if current_obj > best_obj:
                    best_solution = current_solution
                    best_obj = current_obj

        current_temp *= alpha

    return best_solution, best_obj


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    a_bounds = (0, 12)
    b_bounds = (0, 12)
    max_iter = 10000
    initial_temp = 100.0
    alpha = 0.999
    best_solution, best_obj = simulated_annealing(objective, constraints, a_bounds, b_bounds, max_iter, initial_temp,
                                                  alpha)

    print(
        f"The best solution found is a={best_solution[0]}, b={best_solution[1]} with an objective value of {best_obj}")

    print(constraints(best_solution[0], best_solution[1]))
