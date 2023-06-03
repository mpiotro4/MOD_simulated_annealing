import numpy as np
def simulated_annealing(obj_func, constraint_func, a_bounds, b_bounds, x_bounds, y_bounds, z_bounds, max_iter,
                        initial_temp, alpha):
    # Initialize solutions within constraints
    a = np.random.uniform(*a_bounds, size=(6,))
    b = np.random.uniform(*b_bounds, size=(5, 6))
    x = np.random.uniform(*x_bounds, size=(5, 6))
    y = np.random.uniform(*y_bounds, size=(5, 6))
    z = np.random.uniform(*z_bounds, size=(5, 7))

    while not constraint_func(a, b, x, y, z):
        a = np.random.uniform(*a_bounds, size=(6,))
        b = np.random.uniform(*b_bounds, size=(5, 6))
        x = np.random.uniform(*x_bounds, size=(5, 6))
        y = np.random.uniform(*y_bounds, size=(5, 6))
        z = np.random.uniform(*z_bounds, size=(5, 7))

    best_solution_a = current_solution_a = a
    best_solution_b = current_solution_b = b
    best_solution_x = current_solution_x = x
    best_solution_y = current_solution_y = y
    best_solution_z = current_solution_z = z

    best_obj = current_obj = obj_func(a, x, z)

    current_temp = initial_temp

    for i in range(max_iter):
        # Perturb the current solutions
        next_solution_a = current_solution_a + np.random.uniform(-1, 1, current_solution_a.shape)
        next_solution_b = current_solution_b + np.random.uniform(-1, 1, current_solution_b.shape)
        next_solution_x = current_solution_x + np.random.uniform(-1, 1, current_solution_x.shape)
        next_solution_y = current_solution_y + np.random.uniform(-1, 1, current_solution_y.shape)
        next_solution_z = current_solution_z + np.random.uniform(-1, 1, current_solution_z.shape)

        # Check constraints
        if constraint_func(next_solution_a, next_solution_b, next_solution_x, next_solution_y, next_solution_z):
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