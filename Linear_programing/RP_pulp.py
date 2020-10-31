""" Linear programing in Python. Inspired by RealPython tutorial and blog from Ben Alex Keen. """
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


def simple3():
    """Facility location problem using mixed integer variable. The objective is to choose the best among potential sites,
    subject to constraints requiring that demands at several points mut be serviced by the established facilities.
    The company has 3 potential sites for installing its facilities/warehouses and five demand points.
    Each site j has a yearly activation cost fj, i.e., an annual leasing expense that is incurred for using it, independnt of volume.
    Volume is limited to a maximum yearly amount Mj.
    There are transportation cost Cij per unit service from facility j to the demand point i.
    Objective is to minimize the sum of facility activation costs and transportation costs.
        min sum(f_j * y_j) + sum(sum(c_ij*x_ij))
    where x_ij is the ammount service  from facility j to point i and y_j is facility j
    https://scipbook.readthedocs.io/en/latest/flp.html  inspired by youtube Caylie Cincera.
    answer:
    objective is 5610$
    should be keep Facility 2 and 3 open while closing Facility 1
    Volume transported to Facility 2 is 80, 270 and 150 from customer 1, 2, and 3
    Volume transported to Facility 3 is 100, 160, 180  from customer 3, 4, and 5
    """
    CUSTOMERS = [1, 2, 3, 4, 5]  # C_i
    FACILITY = ["FAC_1", "FAC_2", "FAC_3"]  # Facility_j

    demand = {1: 80, 2: 270, 3: 250, 4: 160, 5: 180}  # Annual demand d_i

    actcost = {"FAC_1": 1000, "FAC_2": 1000, "FAC_3": 1000}  # Activation cost  f_j
    maxam = {"FAC_1": 500, "FAC_2": 500, "FAC_3": 500}  # Max volume M_j

    transp = {
        "FAC_1": {1: 4, 2: 5, 3: 6, 4: 8, 5: 10},
        "FAC_2": {1: 6, 2: 4, 3: 3, 4: 5, 5: 8},
        "FAC_3": {1: 9, 2: 7, 3: 4, 4: 3, 5: 4},
    }

    # Initialize the model
    prob = LpProblem("FacilityLocation")

    # Set decision variables
    # Binary decision variables, x_ij
    use_vars = LpVariable.dicts("UseLocation", FACILITY, 0, 1, "Binary")
    serv_vars = LpVariable.dicts(
        "Service", [(i, j) for i in CUSTOMERS for j in FACILITY], lowBound=0
    )

    # Set objective function
    prob += lpSum(actcost[j] * use_vars[j] for j in FACILITY) + lpSum(
        transp[j][i] * serv_vars[(i, j)] for j in FACILITY for i in CUSTOMERS
    )

    # Set constraints
    for i in CUSTOMERS:
        prob += lpSum(serv_vars[(i, j)] for j in FACILITY) == demand[i]

    for j in FACILITY:
        prob += lpSum(serv_vars[(i, j)] for i in CUSTOMERS) <= maxam[j] * use_vars[j]

    for i in CUSTOMERS:
        for j in FACILITY:
            prob += serv_vars[(i, j)] <= demand[i] * use_vars[j]

    status = prob.solve()
    return prob


def print_model_basic(model):
    print(f"status: {model.status}, {LpStatus[model.status]}")
    print(f"objective: {model.objective.value()}")

    for var in model.variables():
        print(f"{var.name}:\t{var.value()}")

    for name, constraint in model.constraints.items():
        print(f"{name}:\t{constraint.value()}")


def print_model_scientifc(model):
    print(f"status: {model.status}, {LpStatus[model.status]}")
    print(f"objective: {model.objective.value():.2e}")

    for var in model.variables():
        print(f"{var.name}:\t{var.value():.2e}")

    for name, constraint in model.constraints.items():
        print(f"{name}:\t{constraint.value():.2e}")


def main():
    # model = simple()
    model = simple3()

    print_model_basic(model)


if __name__ == "__main__":
    main()
