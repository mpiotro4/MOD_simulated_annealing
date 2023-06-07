from model import *
from functions import *

if __name__ == '__main__':
    # print(objective(a_optimal, x_optimal, z_optimal))
    # print(constraints(a=a_optimal, x=x_optimal, y=y_optimal, z=z_optimal, b=b_optimal))

    a = np.zeros((6,))
    b = np.zeros((5, 6))
    x = np.zeros((5, 6))
    y = np.zeros((5, 6))
    z = np.full((5, 7), 500)
    for i in range(0, 100):
        a, b, x, y, z = find_neighbours(a=a, b=b, x=x, y=y, z=z)
        while not constraints(a, x, y, z, b):
            print(f"iteration: {i}")

    # while not constraints(a, x, y, z, b):
    #     a, b, x, y, z = find_neighbours(a=a, b=b, x=x, y=y, z=z)
    #
    # best_solution_a = current_solution_a = a
    # best_solution_b = current_solution_b = b
    # best_solution_x = current_solution_x = x
    # best_solution_y = current_solution_y = y
    # best_solution_z = current_solution_z = z

    # best_solution_a, best_solution_b, best_solution_x, best_solution_y, best_solution_z, best_obj = simulated_annealing(
    #     objective,
    #     constraints,
    #     max_iter=50000,
    #     initial_temp=100.0,
    #     alpha=0.999
    # )
    # print(constraints(best_solution_a, best_solution_x, best_solution_y, best_solution_z, best_solution_b))
    # print(best_obj)
