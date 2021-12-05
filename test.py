import unittest
from simplex import *


class SimplexSolverTestCase(unittest.TestCase):
    def test_exam(self):
        objective = ('minimize', '- 3x_1 - 2x_2')
        constraints = ['2x_1 + 1x_2 <= 18', '2x_1 + 3x_2 <= 42',
                       '3x_1 + 1x_2 <= 24']
        LP1 = Simplex(num_vars=3, constraints=constraints, objective_function=objective)
        print(LP1.solution)
        print(LP1.optimize_val)

    def test_exam_more(self):
        objective = ('minimize', '- 3x_1 - 2x_2')
        constraints = ['2x_1 + 1x_2 <= 18', '2x_1 + 3x_2 <= 42',
                       '3x_1 + 1x_2 <= 24']
        LP1 = Simplex(num_vars=3, constraints=constraints, objective_function=objective)
        print(LP1.solution)
        print(LP1.optimize_val)

    def test_maximize(self):
        objective = ('minimize', '- 3x_1 - 2x_2')
        constraints = ['2x_1 + 1x_2 <= 18', '2x_1 + 3x_2 <= 42',
                       '3x_1 + 1x_2 <= 24']
        LP1 = Simplex(num_vars=2, constraints=constraints, objective_function=objective)
        print(LP1.solution)
        print(LP1.optimize_val)

        objective = ('maximize', '3x_1 + 2x_2')
        constraints = ['2x_1 + 1x_2 <= 18', '2x_1 + 3x_2 <= 42',
                       '3x_1 + 1x_2 <= 24']
        LP2 = Simplex(num_vars=2, constraints=constraints, objective_function=objective)
        print(LP2.solution)
        print(LP2.optimize_val)
        self.assertEqual(LP1.optimize_val, -LP2.optimize_val)
        self.assertEqual(LP1.solution, LP2.solution)

    def test_complicated(self):
        objective = ('maximize', '1x_1 - 1x_2 + 1x_3')
        constraints = ['2x_1 - 1x_2 + 2x_3 <= 4', '- 2x_1 + 3x_2 - 1x_3 >= 5',
                       '1x_1 - 1x_2 + 2x_3 >= 1']
        LP1 = Simplex(num_vars=3, constraints=constraints, objective_function=objective)
        print(LP1.solution)
        print(LP1.optimize_val)
        self.assertEqual(Fraction(3, 5), LP1.optimize_val)

    def test_infeasible(self):
        objective = ('maximize', '1x_1 - 1x_2 + 1x_3')
        constraints = ['2x_1 - 1x_2 - 2x_3 <= 4', '- 2x_1 + 3x_2 + 1x_3 >= 5',
                       '1x_1 - 1x_2 - 1x_3 >= 1']
        try:
            LP1 = Simplex(num_vars=3, constraints=constraints, objective_function=objective, vars_non_negative=True)
            print(LP1.solution)
            print(LP1.optimize_val)
        except ValueError as e:
            self.assertEqual(str(e), "Infeasible solution")

    def test_unbounded(self):
        objective = ('minimize', '- 3/5x_1 - 1/3x_4 - 1/3')
        constraints = ['- 1/3x_1 + 1x_3 + 1/3x_4 = 5/3', '- 2/3x_1 + 1x_2 - 1/3x_4 = 1/3']
        try:
            LP = Simplex(num_vars=4, constraints=constraints, objective_function=objective)
            print(LP.solution)
            print(LP.optimize_val)
        except ValueError as e:
            self.assertEqual(str(e), "Unbounded solution")

    def test_more_basic(self):
        objective = ('minimize', '- 6x_1 - 4x_2 - 3x_3')
        constraints = ['4x_1 + 5x_2 + 3x_3 <= 12', '3x_1 + 4x_2 + 2x_3 <= 10', '4x_1 + 2x_2 + 1x_3 <= 8']
        LP = Simplex(num_vars=3, constraints=constraints, objective_function=objective, vars_non_negative=True)
        print(LP.solution)
        print(LP.optimize_val)
        self.assertEqual(LP.optimize_val, -15)

    def test_more(self):
        objective = ('minimize', '- 2x_1 + 3x_2 - 1x_3')
        constraints = ['3x_1 + 6x_2 + 1x_3 <= 6', '4x_1 + 2x_2 + 1x_3 <= 4', '1x_1 - 1x_2 + 1x_3 <= 3']
        LP = Simplex(num_vars=3, constraints=constraints, objective_function=objective, vars_non_negative=True)
        print(LP.solution)
        print(LP.optimize_val)
        self.assertEqual(LP.optimize_val*3, -10)

    def test_cycle(self):
        objective = ('minimize', '- 10x_1 + 57x_2 + 9x_3 + 24x_4')
        constraints = ['1/2x_1 - 11/2x_2 - 5/2x_3 + 9x_4 <= 0', '1/2x_1 - 3/2x_2 - 1/2x_3 + 1x_4 <= 0', '1x_1 <= 1']
        LP = Simplex(num_vars=4, constraints=constraints, objective_function=objective, vars_non_negative=True, avoid_cycle=True)
        print(LP.solution)
        print(LP.optimize_val)
        self.assertEqual(LP.optimize_val, -1)


if __name__ == '__main__':
    unittest.main()
