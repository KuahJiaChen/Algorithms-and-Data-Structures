########################
#####  Question 2  #####
########################


import math
import numpy as np
import sys


def linear_programming(num_decision, num_constraint, objective, constraints_LHS_matrix, constraints_RHS_vector):
    """
    Description: Aims to address linear programming problems, which entail the optimization of a linear objective
                 function while considering linear inequality constraints.
    Written by: Kuah Jia Chen
    Input: num_decision is an integer, num_constraint is an integer, objective is a list of integers,
           constraints_LHS_matrix is list of list that contains all integer element, constraints_RHS_vector is a list of integers
    Return: the optimal decisions for the decision variables and the optimal objective value
    Time complexity (Worst case): O(N^2+NM), where N is the value num_constraint and M is the value of num_decision
    Space complexity:
        Input: O(N^2 +NM)), where N is the value num_constraint and M is the value of num_decision
        Aux: O(N+M), where N is the value num_constraint and M is the value of num_decision
    """
    # construct the C_j list
    C_j = objective.copy()
    for i in range(num_constraint + 1):  # + 1 due to the RHS value
        C_j.append(0)
    C_j = np.array(C_j)

    # construct the constraint table
    constraint_table = np.zeros((num_constraint, num_decision + num_constraint + 1))
    for i in range(num_constraint):
        constraint_table[i, :num_decision] = constraints_LHS_matrix[i].copy()
        constraint_table[i, num_decision:] = [0] * (num_constraint + 1)  # + 1 due to the RHS value
        constraint_table[i, i + num_decision] = 1
        constraint_table[i, num_decision + num_constraint] = constraints_RHS_vector[i]

    # create a list to stores the index of basic variables
    basic_variables_index = [i for i in range(num_decision, num_decision + num_constraint)]
    # create a list to store the boolean values to indicate if a variable is basic or not
    is_basic = ([False] * num_decision) + ([True] * num_constraint)

    while True:

        # get the coefficient of the basic variables
        temp = []
        for i in range(len(basic_variables_index)):
            current_basic_index = basic_variables_index[i]
            current_coefficient = C_j[current_basic_index]
            temp.append(current_coefficient)
        temp = np.array(temp)

        # compute Z_j
        Z_j = temp.dot(constraint_table)

        # computer C_j - Z_j
        C_j_Z_j = C_j - Z_j

        # make the last element in C_j_Z_j which represents the z as positive
        C_j_Z_j[-1] = abs(C_j_Z_j[-1])

        # find the value and the index of the non-basic variable with the highest coefficient
        max_value = -1
        max_variable_index = None

        # exclude the last element in C_i_Z_j, which is z
        for i in range(len(C_j_Z_j) - 1):
            current_value = C_j_Z_j[i]
            if current_value > max_value and current_value > 0:
                max_value = current_value
                max_variable_index = i

        # no more improvement can be made as there is no non-basic variable with max positive coefficient
        if max_variable_index is None:
            break

        theta = []
        for i in range(len(constraint_table)):
            RHS_value = constraint_table[i][-1]
            if constraint_table[i][max_variable_index] != 0:
                current_theta_value = RHS_value / constraint_table[i][max_variable_index]
            else:
                current_theta_value = math.inf
            theta.append(current_theta_value)

        # find the minimum theta value
        min_theta_value = math.inf
        min_theta_index = 0
        for i in range(len(theta)):
            current_theta = theta[i]
            if 0 < current_theta < min_theta_value:
                min_theta_value = current_theta
                min_theta_index = i

        intersection_point = constraint_table[min_theta_index][max_variable_index]

        # change the boolean variable for the non-basic variable with the highest value
        is_basic[max_variable_index] = True

        # get the index of the basic variable with the lowest index
        min_basic_variable_index = basic_variables_index[min_theta_index]
        is_basic[min_basic_variable_index] = False

        # replace the basic variable with the lowest value with the non-basic variable with the highest value
        basic_variables_index[min_theta_index] = max_variable_index

        # divide the (min_theta_index)th row with the intersection point
        n = len(constraint_table[min_theta_index])
        for i in range(n):
            constraint_table[min_theta_index][i] /= intersection_point

        # update the values in all constraint in the constraint table
        for i in range(len(constraint_table)):
            if i != min_theta_index:
                current_constraint = constraint_table[i]
                for j in range(len(constraint_table[i])):
                    if j != max_variable_index:
                        current_constraint[j] -= \
                            (constraint_table[min_theta_index][j] * current_constraint[max_variable_index])
                current_constraint[max_variable_index] = 0

    # get the value for decision variables
    ans = [0] * num_decision

    for i in range(len(basic_variables_index)):
        current_index = basic_variables_index[i]
        if 0 <= current_index <= num_decision - 1:
            current_constraint_index = i
            # print(current_constraint_index)
            current_decision_value = constraint_table[current_constraint_index][-1]
            ans[current_index] = current_decision_value

    return ans, C_j_Z_j[-1]


def read_file(file_path):
    """
    Description: read the num_of_decision, num_of_constraint, objective, constraints_LHS_matrix, constraints_RHS_vector
                 from the input file
    Written by: Kuah Jia Chen
    Input: file_path is the file path to access the file
    Return: return the num_of_decision, num_of_constraint, objective, constraints_LHS_matrix, constraints_RHS_vector
            in the file
    """

    f = open(file_path, 'r')
    lines = f.readlines()

    # get the value of num_of_decision and num_of_constraint
    num_of_decision, num_of_constraint = int(lines[1]), int(lines[3])

    # get the values of objective
    objective = [float(num.strip()) for num in lines[5].split(",")]

    # get the values in constraints_LHS_matrix
    constraints_LHS_matrix = []
    current_index = 7
    for _ in range(num_of_constraint):
        current_constraint = [float(num.strip()) for num in lines[current_index].split(",")]
        constraints_LHS_matrix.append(current_constraint)
        current_index += 1
    # skip the header of RHSVector
    current_index += 1

    # get the values in constraints_RHS_vector
    constraints_RHS_vector = []
    for _ in range(num_of_constraint):
        current_vector = float(lines[current_index])
        constraints_RHS_vector.append(current_vector)
        current_index += 1

    f.close()
    return num_of_decision, num_of_constraint, objective, constraints_LHS_matrix, constraints_RHS_vector


def write_output(optimal_decisions, optimal_objective):
    """
    Description: write the answer to the output file
    Written by: Kuah Jia Chen
    Input: the value of p, q, modulus and exponent
    Return: None
    """
    output_file = open("lpsolution.txt", "w")
    output_file.write("# optimalDecisions")
    output_file.write("\n")
    n = len(optimal_decisions)
    for i in range(n):
        if i == n - 1:
            output_file.write(str(optimal_decisions[i]))
        else:
            output_file.write(str(optimal_decisions[i]) + ", ")
    output_file.write("\n")
    output_file.write("# optimalObjective")
    output_file.write("\n")
    output_file.write(str(optimal_objective))
    # Close output file
    output_file.close()


if __name__ == '__main__':
    # retrieve the file paths from the commandline arguments
    _, file_name = sys.argv
    print("Number of arguments passed : ", len(sys.argv))
    # since we know the program takes one argument
    print("First argument : ", file_name)

    input_num_of_decision, input_num_of_constraint, input_objective, input_constraints_LHS_matrix, \
                                                           input_constraints_RHS_vector = read_file(file_name)

    output_optimal_decisions, output_optimal_objective = linear_programming(input_num_of_decision,
                                                          input_num_of_constraint, input_objective,
                                                          input_constraints_LHS_matrix, input_constraints_RHS_vector)

    write_output(output_optimal_decisions, output_optimal_objective)
