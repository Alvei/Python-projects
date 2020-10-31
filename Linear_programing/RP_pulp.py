""" Linear programing in Python. Inspired by RealPython. """
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable


def simple():
    # Create the model
    model = LpProblem(name="small-problem", sense=LpMaximize)

    # Initialize the decision variables
    x = LpVariable(name="x", lowBound=0)
    y = LpVariable(name="y", lowBound=0)

    # expression = 2 * x + 4 * y
    # constraint = 2 * x + 4 * y >= 8
    # print(f"{type(expression)}\n{type(constraint)}")

    # Add the constraints to the model
    model += (2 * x + y <= 20, "red_constraint")
    model += (4 * x - 5 * y >= -10, "blue_constraint")
    model += (-x + 2 * y >= -2, "yellow_constraint")
    model += (-x + 5 * y == 15, "green_constraint")

    # Add the objective function to the model
    obj_func = x + 2 * y
    model += obj_func

    # print(model)
    status = model.solve()
    return model


def simple2():
    # Define the model
    model = LpProblem(name="resource-allocation", sense=LpMaximize)

    # Define the decision variables
    x = {i: LpVariable(name=f"x{i}", lowBound=0) for i in range(1, 5)}

    # Add constraints
    model += (lpSum(x.values()) <= 50, "manpower")
    model += (3 * x[1] + 2 * x[2] + x[3] <= 100, "material_a")
    model += (x[2] + 2 * x[3] + 3 * x[4] <= 90, "material_b")

    # Set the objective
    model += 20 * x[1] + 12 * x[2] + 40 * x[3] + 25 * x[4]

    # Solve the optimization problem
    status = model.solve()
    return model


def main():
    # model = simple()
    model = simple2()

    print(f"status: {model.status}, {LpStatus[model.status]}")
    print(f"objective: {model.objective.value():.2e}")

    for var in model.variables():
        print(f"{var.name}:\t{var.value():.2e}")

    for name, constraint in model.constraints.items():
        print(f"{name}:\t{constraint.value():.2e}")


if __name__ == "__main__":
    main()
