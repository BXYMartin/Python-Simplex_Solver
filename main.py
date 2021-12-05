from simplex import *


if __name__ == '__main__':
    objective = ('minimize', '1 - 1x_4 - 2x_5 - 1x_6')
    constraints = ['1x_1 + 1x_4 + 1x_5 - 1x_6 = 5', '1x_2 + 2x_4 - 3x_5 + 1x_6 = 3', '1x_3 - 1x_4 + 2x_5 - 1x_6 = -1']
    LP = Simplex(num_vars=6, constraints=constraints, objective_function=objective)
    print(LP.solution)
    print(LP.optimize_val)
    pass
    objective = ('maximize', '5x_1 + 6x_2')
    constraints = ['1x_1 + 1x_2 <= 6', '5x_1 + 9x_2 <= 45']
    LP = Simplex(num_vars=2, constraints=constraints, objective_function=objective)
    print(LP.solution)
    print(LP.optimize_val)
    pass
    objective = ('maximize', '1x_1 + 1x_2')
    constraints = ['- 1x_1 + 1x_2 <= 2', '- 2x_1 + 3x_2 >= 1']
    LP = Simplex(num_vars=2, constraints=constraints, objective_function=objective)
    print(LP.solution)
    print(LP.optimize_val)
    pass
    objective = ('minimize', '- 3/5x_1 - 1/3x_4 - 1/3')
    constraints = ['- 1/3x_1 + 1x_3 + 1/3x_4 = 5/3', '- 2/3x_1 + 1x_2 - 1/3x_4 = 1/3']
    LP = Simplex(num_vars=4, constraints=constraints, objective_function=objective)
    print(LP.solution)
    print(LP.optimize_val)

