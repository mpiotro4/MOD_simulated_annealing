from model import *
from functions import *

if __name__ == '__main__':
    print(objective(a_optimal, x_optimal, z_optimal))
    print(constraints(a=a_optimal, x=x_optimal, y=y_optimal, z=z_optimal, b=b_optimal))

    # a_bounds = (0, 100)
    # b_bounds = (0, 1)
    # x_bounds = (0, 100)
    # y_bounds = (0, 100)
    # z_bounds = (0, 500)
    #
    # a = np.zeros((6,))
    # b = np.zeros((5, 6))
    # x = np.zeros((5, 6))
    # y = np.zeros((5, 6))
    # z = np.full((5, 7), 500)
    # a[np.random.randint(0, len(a))] = np.random.rand()

    # while True:
    #     # while not constraints(a=a, x=x, y=y, z=z, b=b):
    #     a = np.zeros((6,))
    #     x = np.zeros((5, 6))
    #     y = np.zeros((5, 6))
    #     z = np.full((5, 7), 500)
    #     b = np.zeros((5, 6))
    #
    #     row_index, col_index = np.random.randint(0, 5), np.random.randint(1, 6)
    #     if col_index - 1 == 0:
    #         rand_z2 = 500
    #     else:
    #         rand_z2 = np.random.uniform(500, 510)
    #     rand_x = np.random.uniform(0, 10)
    #     rand_y = np.random.uniform(rand_z2, rand_z2 + 10)
    #     rand_z1 = rand_y - rand_z2 - rand_x
    #     # z2[i, j - 1] + x[i, j - 1]) - (y[i, j - 1] + z1[i, j] == 0
    #     # z2 = y - z1 - x
    #     z[row_index, col_index] = rand_z1
    #     z[row_index, col_index - 1] = rand_z2
    #     x[row_index, col_index - 1] = rand_x
    #     y[row_index, col_index - 1] = rand_y
    #     b[row_index, col_index - 1] = 1
    #     for j in range(months):
    #         a[j] = np.sum(y[:, j])
    #     print(constraints(a=a, x=x, y=y, z=z, b=b))

    # while not constraints(a, b, x, y, z):
    #     a = np.random.uniform(*a_bounds, size=(6,))
    #     b = np.random.uniform(*b_bounds, size=(5, 6))
    #     x = np.random.uniform(*x_bounds, size=(5, 6))
    #     y = np.random.uniform(*y_bounds, size=(5, 6))
    #     z = np.random.uniform(*z_bounds, size=(5, 7))
    #     print(constraints(a=a, x=x, y=y, z=z, b=b))

    # best_solution_a, best_solution_b, best_solution_x, best_solution_y, best_solution_z, best_obj = simulated_annealing(
    #     objective,
    #     constraints,
    #     a_bounds,
    #     b_bounds,
    #     x_bounds,
    #     y_bounds,
    #     z_bounds,
    #     max_iter=10000,
    #     initial_temp=100.0,
    #     alpha=0.999
    # )
