import numpy as np
from model import *


def find_neighbours(a, b, x, y, z):
    b = np.zeros((5, 6))
    row_index, col_index = np.random.randint(0, 5), np.random.randint(1, 6)
    print(f"row index: {row_index}")
    print(f"col index: {col_index}")
    z_prev = z[row_index, col_index]
    if col_index == 6:
        rand_z = 500
    else:
        rand_z = z[row_index, col_index + 1] + np.random.uniform(0, 100)
    if rand_z >= z_prev:
        rand_x = x[row_index, col_index] + np.random.uniform(abs(rand_z - z_prev), z_prev)
    else:
        rand_x = x[row_index, col_index] + np.random.uniform(0, 100)
    rand_y = z_prev - rand_z + rand_x
    print(f"prev z = {z_prev}")
    print(f"rand z = {rand_z}")
    print(f"rand x = {rand_x}")
    print(f"rand y = {rand_y}")
    print(f"{z_prev + rand_x} == {rand_y + rand_z}")

    x[row_index, col_index] = rand_x
    y[row_index, col_index] = rand_y
    z[row_index, col_index + 1] = rand_z
    for j in range(months):
        a[j] = np.sum(y[:, j])
    b[row_index, col_index] = 1

    return a, b, x, y, z


def simulated_annealing(obj_func, constraint_func, max_iter, initial_temp, alpha):
    # Initialize solutions within constraints
    a = np.zeros((6,))
    b = np.zeros((5, 6))
    x = np.zeros((5, 6))
    y = np.zeros((5, 6))
    z = np.full((5, 7), 500)

    while not constraint_func(a, x, y, z, b):
        a, b, x, y, z = find_neighbours(a=a, b=b, x=x, y=y, z=z)

    best_solution_a = current_solution_a = a
    best_solution_b = current_solution_b = b
    best_solution_x = current_solution_x = x
    best_solution_y = current_solution_y = y
    best_solution_z = current_solution_z = z

    best_obj = current_obj = obj_func(a, x, z)

    current_temp = initial_temp

    for i in range(max_iter):
        # Perturb the current solutions
        next_solution_a, next_solution_b, next_solution_x, next_solution_y, next_solution_z = find_neighbours(
            a=current_solution_a, b=current_solution_b, x=current_solution_x, y=current_solution_y,
            z=current_solution_z)
        # next_solution_a = current_solution_a + np.random.uniform(-1, 1, current_solution_a.shape)
        # next_solution_b = current_solution_b + np.random.uniform(-1, 1, current_solution_b.shape)
        # next_solution_x = current_solution_x + np.random.uniform(-1, 1, current_solution_x.shape)
        # next_solution_y = current_solution_y + np.random.uniform(-1, 1, current_solution_y.shape)
        # next_solution_z = current_solution_z + np.random.uniform(-1, 1, current_solution_z.shape)

        # Check constraints
        if constraint_func(next_solution_a, next_solution_x, next_solution_y, next_solution_z, next_solution_b):
            next_obj = obj_func(next_solution_a, next_solution_x, next_solution_z)

            # Avoid large numbers in np.exp() computation
            delta_obj = current_obj - next_obj
            if delta_obj / current_temp < 100:  # adjust the number 100 as needed
                accept = np.exp(delta_obj / current_temp) > np.random.rand()
            else:
                accept = False

            if next_obj > current_obj or accept:
                current_solution_a = next_solution_a
                current_solution_b = next_solution_b
                current_solution_x = next_solution_x
                current_solution_y = next_solution_y
                current_solution_z = next_solution_z

                current_obj = next_obj

                if current_obj > best_obj:
                    best_solution_a = current_solution_a
                    best_solution_b = current_solution_b
                    best_solution_x = current_solution_x
                    best_solution_y = current_solution_y
                    best_solution_z = current_solution_z

                    best_obj = current_obj

        current_temp *= alpha

    return best_solution_a, best_solution_b, best_solution_x, best_solution_y, best_solution_z, best_obj
