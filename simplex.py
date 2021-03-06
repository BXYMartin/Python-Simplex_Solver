from fractions import Fraction
from warnings import warn


class Simplex(object):
    def __init__(self, num_vars, constraints, objective_function, vars_non_negative=True, avoid_cycle=False):
        """
        num_vars: Number of variables

        equations: A list of strings representing constraints
        each variable should be start with x followed by a underscore
        and a number
        eg of constraints
        ['1x_1 + 2x_2 >= 4', '2x_3 + 3x_1 <= 5', 'x_3 + 3x_2 = 6']
        Note that in x_num, num should not be more than num_vars.
        Also single spaces should be used in expressions.

        objective_function: should be a tuple with first element
        either 'min' or 'max', and second element be the equation
        eg
        ('min', '2x_1 + 4x_3 + 5x_2')

        For solution finding algorithm uses two-phase simplex method
        """
        self.num_vars = num_vars
        self.constraints = constraints
        self.objective = objective_function[0]
        self.objective_function = objective_function[1]
        self.vars_non_negative = vars_non_negative
        self.avoid_cycle = avoid_cycle
        self.coeff_matrix, self.r_rows, self.num_s_vars, self.num_r_vars = self.construct_matrix_from_constraints()
        del self.constraints
        self.basic_vars = [0 for i in range(len(self.coeff_matrix))]
        self.phase1()
        r_index = self.num_vars + self.num_s_vars

        for i in self.basic_vars:
            if i > r_index:
                raise ValueError("Infeasible solution")

        self.delete_r_vars()
        print("Phase 2")
        if 'min' in self.objective.lower():
            self.solution = self.objective_minimize()
        else:
            self.solution = self.objective_maximize()
        self.optimize_val = self.coeff_matrix[0][-1]

    def construct_matrix_from_constraints(self):
        num_s_vars = 0  # number of slack and surplus variables
        num_r_vars = 0  # number of additional variables to balance equality and less than equal to
        for expression in self.constraints:
            if '>=' in expression:
                num_s_vars += 1
                num_r_vars += 1

            elif '<=' in expression:
                num_s_vars += 1
                # num_r_vars += 1

            elif '=' in expression:
                num_r_vars += 1
        total_vars = self.num_vars + num_s_vars + num_r_vars

        coeff_matrix = [[Fraction("0/1") for i in range(total_vars+1)] for j in range(len(self.constraints)+1)]
        s_index = self.num_vars
        r_index = self.num_vars + num_s_vars
        r_rows = [] # stores the non -zero index of r
        for i in range(1, len(self.constraints)+1):
            constraint = self.constraints[i-1].split(' ')

            for j in range(len(constraint)):

                if '_' in constraint[j]:
                    coeff, index = constraint[j].split('_')
                    if constraint[j-1] == '-':
                        if '/' in coeff[:-1]:
                            coeff_matrix[i][int(index) - 1] = Fraction("-" + coeff[:-1])
                        else:
                            coeff_matrix[i][int(index)-1] = Fraction("-" + coeff[:-1] + "/1")
                    else:
                        if '/' in coeff[:-1]:
                            coeff_matrix[i][int(index) - 1] = Fraction(coeff[:-1])
                        else:
                            coeff_matrix[i][int(index)-1] = Fraction(coeff[:-1] + "/1")

                elif constraint[j] == '<=':
                    coeff_matrix[i][s_index] = Fraction("1/1")  # add surplus variable
                    s_index += 1

                elif constraint[j] == '>=':
                    coeff_matrix[i][s_index] = Fraction("-1/1")  # slack variable
                    coeff_matrix[i][r_index] = Fraction("1/1")   # r variable
                    s_index += 1
                    r_index += 1
                    r_rows.append(i)

                elif constraint[j] == '=':
                    coeff_matrix[i][r_index] = Fraction("1/1")  # r variable
                    r_index += 1
                    r_rows.append(i)
            if '/' in constraint[-1]:
                coeff_matrix[i][-1] = Fraction(constraint[-1])
            else:
                coeff_matrix[i][-1] = Fraction(constraint[-1] + "/1")

        return coeff_matrix, r_rows, num_s_vars, num_r_vars

    def print_tableau(self, key_column, key_row, finish=False, one=False):
        subscript = str.maketrans("0123456789", "??????????????????????????????")
        variables = [f"x{i+1}".translate(subscript) for i in range(self.num_vars)]
        variables += [f"s{i+1}".translate(subscript) for i in range(self.num_s_vars)]
        if one:
            variables += [f"??{i+1}".translate(subscript) for i in range(len(self.r_rows))]
        line = ""
        line += ("%-10s\t" + "%-10s\t"*len(variables) + "%-10s") % ("BV", *variables, "RHS")
        print(line)
        for row in range(len(self.coeff_matrix)):
            if row == 0:
                line = "%-10s\t" % "z"
            else:
                line = "%-10s\t" % variables[self.basic_vars[row]]
            for col in range(len(self.coeff_matrix[0])):
                line += "%-10s\t" % self.coeff_matrix[row][col]
            print(line)
        if not finish:
            print("> %s in, %s out" % (variables[key_column], variables[self.basic_vars[key_row]]))
        else:
            prefix = ""
            if one:
                prefix = "Phase 1 "
            solution = []
            for i in range(len(variables)):
                if i in self.basic_vars[1:]:
                    solution.append(str(self.coeff_matrix[self.basic_vars[1:].index(i) + 1][-1]))
                else:
                    solution.append("0")
            print(prefix + "Solution (" + ",".join(variables) + ") = (" + ",".join(solution) + ")")
            if one:
                if self.coeff_matrix[0][-1] != 0:
                    raise ValueError("Infeasible solution")
            if self.vars_non_negative:
                for i in solution:
                    if eval(i) < 0:
                        raise ValueError("Infeasible solution")

    def phase1(self):
        print("Phase 1")
        # Objective function here is minimize r1+ r2 + r3 + ... + rn
        r_index = self.num_vars + self.num_s_vars
        for i in range(r_index, len(self.coeff_matrix[0])-1):
            self.coeff_matrix[0][i] = Fraction("-1/1")
        coeff_0 = 0
        for i in self.r_rows:
            self.coeff_matrix[0] = add_row(self.coeff_matrix[0], self.coeff_matrix[i])
            self.basic_vars[i] = r_index
            r_index += 1
        s_index = self.num_vars
        for i in range(1, len(self.basic_vars)):
            if self.basic_vars[i] == 0:
                self.basic_vars[i] = s_index
                s_index += 1

        # Run the simplex iterations
        key_column = max_index(self.coeff_matrix[0])
        condition = self.coeff_matrix[0][key_column] > 0

        while condition is True:

            key_row = self.find_key_row(key_column = key_column)
            self.print_tableau(key_column, key_row, False, True)
            self.basic_vars[key_row] = key_column
            pivot = self.coeff_matrix[key_row][key_column]
            self.normalize_to_pivot(key_row, pivot)
            self.make_key_column_zero(key_column, key_row)

            key_column = max_index(self.coeff_matrix[0])
            condition = self.coeff_matrix[0][key_column] > 0

        self.print_tableau(0, 0, True, True)

    def find_key_row(self, key_column):
        min_val = float("inf")
        min_i = 0
        for i in range(1, len(self.coeff_matrix)):
            if self.coeff_matrix[i][key_column] > 0:
                val = self.coeff_matrix[i][-1] / self.coeff_matrix[i][key_column]
                if val < min_val:
                    min_val = val
                    min_i = i
        if min_val == float("inf"):
            self.print_tableau(key_column, 0, False, False)
            raise ValueError("Unbounded solution")
        if min_val == 0:
            warn("Dengeneracy")
        return min_i

    def normalize_to_pivot(self, key_row, pivot):
        for i in range(len(self.coeff_matrix[0])):
            self.coeff_matrix[key_row][i] /= pivot

    def make_key_column_zero(self, key_column, key_row):
        num_columns = len(self.coeff_matrix[0])
        for i in range(len(self.coeff_matrix)):
            if i != key_row:
                factor = self.coeff_matrix[i][key_column]
                for j in range(num_columns):
                    self.coeff_matrix[i][j] -= self.coeff_matrix[key_row][j] * factor

    def delete_r_vars(self):
        for i in range(len(self.coeff_matrix)):
            non_r_length = self.num_vars + self.num_s_vars + 1
            length = len(self.coeff_matrix[i])
            while length != non_r_length:
                del self.coeff_matrix[i][non_r_length-1]
                length -= 1

    def update_objective_function(self):
        objective_function_coeffs = self.objective_function.split()
        for i in range(len(objective_function_coeffs)):
            if '_' in objective_function_coeffs[i]:
                coeff, index = objective_function_coeffs[i].split('_')
                if objective_function_coeffs[i-1] == '-':
                    if '/' in coeff[:-1]:
                        self.coeff_matrix[0][int(index) - 1] = Fraction(coeff[:-1])
                    else:
                        self.coeff_matrix[0][int(index)-1] = Fraction(coeff[:-1] + "/1")
                else:
                    if '/' in coeff[:-1]:
                        self.coeff_matrix[0][int(index) - 1] = Fraction("-" + coeff[:-1])
                    else:
                        self.coeff_matrix[0][int(index)-1] = Fraction("-" + coeff[:-1] + "/1")

    def check_alternate_solution(self):
        for i in range(len(self.coeff_matrix[0])):
            if self.coeff_matrix[0][i] and i not in self.basic_vars[1:]:
                warn("Alternate Solution exists")
                break

    def objective_minimize(self):
        self.update_objective_function()

        for row, column in enumerate(self.basic_vars[1:]):
            if self.coeff_matrix[0][column] != 0:
                self.coeff_matrix[0] = add_row(self.coeff_matrix[0], multiply_const_row(-self.coeff_matrix[0][column], self.coeff_matrix[row+1]))

        key_column = max_index(self.coeff_matrix[0], self.avoid_cycle)
        condition = self.coeff_matrix[0][key_column] > 0

        while condition is True:

            key_row = self.find_key_row(key_column = key_column)
            self.print_tableau(key_column, key_row, False, False)
            self.basic_vars[key_row] = key_column
            pivot = self.coeff_matrix[key_row][key_column]
            self.normalize_to_pivot(key_row, pivot)
            self.make_key_column_zero(key_column, key_row)

            key_column = max_index(self.coeff_matrix[0], self.avoid_cycle)
            condition = self.coeff_matrix[0][key_column] > 0
        self.print_tableau(0, 0, True, False)
        solution = {}
        for i, var in enumerate(self.basic_vars[1:]):
            if var < self.num_vars:
                solution['x_'+str(var+1)] = self.coeff_matrix[i+1][-1]

        for i in range(0, self.num_vars):
            if i not in self.basic_vars[1:]:
                solution['x_'+str(i+1)] = Fraction("0/1")
        self.check_alternate_solution()
        return solution

    def objective_maximize(self):
        self.update_objective_function()

        for row, column in enumerate(self.basic_vars[1:]):
            if self.coeff_matrix[0][column] != 0:
                self.coeff_matrix[0] = add_row(self.coeff_matrix[0], multiply_const_row(-self.coeff_matrix[0][column], self.coeff_matrix[row+1]))

        key_column = min_index(self.coeff_matrix[0], self.avoid_cycle)
        condition = self.coeff_matrix[0][key_column] < 0

        while condition is True:

            key_row = self.find_key_row(key_column = key_column)
            self.print_tableau(key_column, key_row, False, False)
            self.basic_vars[key_row] = key_column
            pivot = self.coeff_matrix[key_row][key_column]
            self.normalize_to_pivot(key_row, pivot)
            self.make_key_column_zero(key_column, key_row)

            key_column = min_index(self.coeff_matrix[0], self.avoid_cycle)
            condition = self.coeff_matrix[0][key_column] < 0
        self.print_tableau(0, 0, True, False)
        solution = {}
        for i, var in enumerate(self.basic_vars[1:]):
            if var < self.num_vars:
                solution['x_'+str(var+1)] = self.coeff_matrix[i+1][-1]

        for i in range(0, self.num_vars):
            if i not in self.basic_vars[1:]:
                solution['x_'+str(i+1)] = Fraction("0/1")

        self.check_alternate_solution()

        return solution


def add_row(row1, row2):
    row_sum = [0 for i in range(len(row1))]
    for i in range(len(row1)):
        row_sum[i] = row1[i] + row2[i]
    return row_sum


def max_index(row, avoid_cycle=False):
    max_i = 0
    if avoid_cycle:
        for i in range(0, len(row) - 1):
            if row[i] > 0:
                return i

    for i in range(0, len(row)-1):
        if row[i] > row[max_i]:
            max_i = i

    return max_i


def multiply_const_row(const, row):
    mul_row = []
    for i in row:
        mul_row.append(const*i)
    return mul_row


def min_index(row, avoid_cycle=False):
    min_i = 0
    if avoid_cycle:
        for i in range(0, len(row) - 1):
            if row[i] < 0:
                return i

    for i in range(0, len(row)-1):
        if row[min_i] > row[i]:
            min_i = i

    return min_i
