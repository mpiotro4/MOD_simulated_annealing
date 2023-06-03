import numpy as np

price = np.array([
    [110, 130, 110, 120, 100, 90],
    [120, 130, 140, 110, 120, 100],
    [130, 110, 130, 120, 150, 140],
    [110, 90, 100, 120, 110, 80],
    [115, 115, 95, 125, 105, 135]
], dtype=np.float64)

T = np.array([8.8, 6.1, 2.0, 4.2, 5.0], dtype=np.float64)

area = np.array([
    [0, 500],  # a
    [0, 1000],  # x
    [0, 300],  # y
    [0, 800],  # z
    [0, 1]  # b
])

months = 6
oils = 5

# a - ilość produktu wyprodukowana w i-tym miesiącu
a = np.zeros(months, dtype=float)

# x - ilość kupionego i-tego oleju w j-tym miesiącu
x = np.zeros((oils, months), dtype=float)

# y - ilość użytego i-tego oleju w j-tym miesiącu
y = np.zeros((oils, months), dtype=float)

# z - ilość przechowanego i-tego oleju w j-tym miesiącu
z = np.zeros((oils, months + 1), dtype=float)

# b - zmienna binarna mówiąca czy i-ty olej jest wykorzystywany w j-tym miesiącu
b = np.zeros((oils, months), dtype=bool)

debug = True


def objective(a, x, z):
    return np.sum(a * 150) - np.sum(x * price) - np.sum(z[:, 1:] * 5)


def constraints(a, x, y, z, b):
    # Define constraints
    constraints = []
    # Constraint: zmiennaA
    for j in range(months):
        constraint = abs(np.sum(y[:, j]) - a[j]) <= 0.11
        if not constraint:
            if debug:
                print(f"Constraint zmiennaA violated {np.sum(y[:, j])} == {a[j]}")
        constraints.append(constraint)

    # Constraint: MaksymalnaIloscOlejuRoslinnegoNaMiesiac
    for j in range(months):
        constraint = np.sum(y[0:2, j]) <= 200
        if not constraint:
            if debug:
                print(f"Constraint MaksymalnaIloscOlejuRoslinnegoNaMiesiac violated")
        constraints.append(constraint)

    # Constraint: MaksymalnaIloscOlejuNormalnegoNaMiesiac
    for j in range(months):
        constraint = np.sum(y[2:5, j]) <= 250
        if not constraint:
            if debug:
                print(f"Constraint MaksymalnaIloscOlejuNormalnegoNaMiesiac violated")
        constraints.append(constraint)

    # Constraint: MaksymalnaTwardosc
    for j in range(months):
        constraint = np.sum(y[:, j] * T) <= 6 * a[j]
        if not constraint:
            if debug:
                print(f"Constraint MaksymalnaTwardosc violated {np.sum(y[:, j] * T)} <= {6 * a[j]}")
        constraints.append(constraint)

    # Constraint: MinimalnaTwardosc
    for j in range(months):
        constraint = np.sum(y[:, j] * T) >= 3 * a[j]
        if not constraint:
            if debug:
                print(f"Constraint MinimalnaTwardosc violated {np.sum(y[:, j] * T)} >= {3 * a[j]}")
        constraints.append(constraint)

    # Constraint: StanPoczatkowy
    for i in range(oils):
        constraint = z[i, 0] == 500
        if not constraint:
            if debug:
                print(f"Constraint StanPoczatkowy violated")
        constraints.append(constraint)

    # Constraint: StanKoncowy
    for i in range(oils):
        constraint = z[i, months] == 500
        if not constraint:
            if debug:
                print(f"Constraint StanKoncowy violated")
        constraints.append(constraint)

    # Constraint: relacje
    for i in range(oils):
        for j in range(1, months + 1):
            constraint = abs(z[i, j - 1] + x[i, j - 1] - y[i, j - 1] - z[i, j]) <= 20
            if not constraint:
                if debug:
                    print(f"Constraint relacje violated {z[i, j - 1]} + {x[i, j - 1]} == {y[i, j - 1]} + {z[i, j]}")
            constraints.append(constraint)

    # Constraint: MaksymalnePojemnosciMagazynow
    for i in range(oils):
        for j in range(months + 1):
            constraint = z[i, j] <= 1000
            if not constraint:
                if debug:
                    print(f"Constraint MaksymalnePojemnosciMagazynow violated")
            constraints.append(constraint)

    # Constraint: Maks3Oleje
    for j in range(months):
        constraint = np.sum(b[:, j]) <= 3
        if not constraint:
            if debug:
                print(f"Constraint Maks3Oleje violated")
        constraints.append(constraint)

    # Constraint: Min20Ton
    for i in range(oils):
        for j in range(months):
            constraint = y[i, j] >= 20 * b[i, j]
            if not constraint:
                if debug:
                    print(f"Constraint Min20Ton violated {y[i, j]} >= {20 * b[i, j]}")
            constraints.append(constraint)

    # Constraint: zmiennaBinarna
    for i in range(oils):
        for j in range(months):
            constraint = y[i, j] <= 200 * b[i, j]
            if not constraint:
                if debug:
                    print(f"Constraint zmiennaBinarna violated")
            constraints.append(constraint)

    # Constraint: zmiennaBinarna2
    for i in range(2, oils):
        for j in range(months):
            constraint = y[i, j] <= 250 * b[i, j]
            if not constraint:
                if debug:
                    print(f"Constraint zmiennaBinarna2 violated")
            constraints.append(constraint)

    # Constraint: JesliVEG1toOIL3
    for j in range(months):
        constraint = b[0, j] - b[4, j] <= 0
        if not constraint:
            if debug:
                print(f"Constraint JesliVEG1toOIL3 violated")
        constraints.append(constraint)

    return np.all(constraints)


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


b_optimal = np.array([
    [0, 1, 0, 0, 1, 0],
    [1, 0, 1, 1, 0, 1],
    [0, 1, 0, 0, 1, 0],
    [1, 0, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1]
], dtype=np.float64)

a_optimal = np.array([450, 450, 450, 450, 450, 450], dtype=np.float64)

x_optimal = np.array([
    [0, 0, 0, 0, 0, 400],
    [0, 0, 0, 100, 0, 700],
    [0, 0, 0, 206.6, 0, 0],
    [0, 0, 0, 0, 0, 700],
    [0, 0, 0, 0, 593.3, 0]
], dtype=np.float64)

y_optimal = np.array([
    [0, 200, 0, 0, 200, 0],
    [200, 0, 200, 200, 0, 200],
    [0, 103.3, 0, 0, 103.3, 0],
    [200, 0, 200, 100, 0, 200],
    [50, 146.6, 50, 150, 146.6, 50]
], dtype=np.float64)

z_optimal = np.array([
    [500, 500, 300, 300, 300, 100, 500],
    [500, 300, 300, 100, 0, 0, 500],
    [500, 500, 396.7, 396.7, 603.3, 500, 500],
    [500, 300, 300, 100, 0, 0, 500],
    [500, 450, 303.3, 253.3, 103.3, 550, 500]
], dtype=np.float64)
