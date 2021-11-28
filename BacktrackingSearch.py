"""
Date: 10/19/21
Author: Tate Toussaint
Description: runs backtracking search on constraint satisfaction problems using various heuristics and inference methods
"""

import math
import copy


class BacktrackingSearch:
    def __init__(self, ac3=True, mrv=True, degree=True, lcv=True):
        self.recursive_calls = 0  # keep track of recursive calls run runtime analysis
        self.ac3 = ac3
        self.mrv = mrv
        self.degree = degree
        self.lcv = lcv

    def backtracking_search(self, csp):
        empty_assignment = [None] * csp.num_variables  # use array of integers to hold variable assignment
        domain = csp.domain  # a dictionary starting with keys = variables and values = all possible values
        return self.backtrack(empty_assignment, csp, domain)

    def backtrack(self, assignment, csp, domain):
        self.recursive_calls += 1  # increment recursive calls variable for my writeup analysis

        if self.is_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment, csp.constraints, domain)  # uses combo of mrv + degree or first unassigned

        for value in self.order_domain_values(var, assignment, csp, domain):  # list of values variable can take
            # check if assigning variable to value breaks constraints
            if self.is_consistent(var, value, assignment, csp.constraints):
                # add {var = value} to assignment
                assignment[var] = value

                # create a copy and update domain based off new variable assignment
                new_domain = copy.deepcopy(domain)
                self.update_domain(new_domain, csp.constraints, var, value)

                # get inferences made by this new assignment
                inferences = self.inference(csp, var, value, domain, assignment)

                if inferences is True:
                    # recurse into backtrack
                    result = self.backtrack(assignment, csp, new_domain)

                    # check if result is a success
                    if result is not None:
                        return result
            assignment[var] = None

        return None  # return failure

    # returns True if a variable assignment is complete; False if not
    def is_complete(self, assignment):
        for i in range(0, len(assignment)):
            if assignment[i] is None:  # not complete
                return False
        return True

    # get rid of assignment when implementing heuristic
    def select_unassigned_variable(self, assignment, constraints, domain):
        if self.mrv:
            return self.select_minimum_remaining_values(assignment, constraints, domain)
        elif self.degree:
            unassigned_list = []
            for i in range(0, len(assignment)):
                if assignment[i] is None:
                    unassigned_list.append(i)
            return self.degree_heuristic(unassigned_list, constraints, assignment)
        else:
            return self.select_first_unassigned_variable(assignment)  # select first unassigned variable

    # returns the first unassigned variable
    def select_first_unassigned_variable(self, assignment):
        for i in range(0, len(assignment)):
            if assignment[i] is None:
                return i

    # selects the variable with the minimum remaining values
    def select_minimum_remaining_values(self, assignment, constraints, domain):
        # use degree heuristic as tie breaker
        min_list = []
        num_min_values = math.inf

        # go through all variables and check the size of their domain
        for var in domain:
            # if variable unassigned
            if assignment[var] is None:
                var_domain = domain[var]  # list of legal values left for var
                if len(var_domain) < num_min_values:
                    min_list = [var]
                    num_min_values = len(var_domain)  # update number of minimum values
                elif len(var_domain) == num_min_values:
                    min_list.append(var)

        if self.degree:
            return self.degree_heuristic(min_list, constraints, assignment)
        else:
            return min_list[0]

    # returns the variable involved in the largest number of constraints
    def degree_heuristic(self, min_list, constraints, assignment):
        num_constraints_involved = {}  # keys: variables, value: number of neighbors

        # loop through constraints and increment variable degrees if involved in constraints and in min_list
        for x1, x2 in constraints:
            if x2 is not None:  # if x2 unassigned
                if x1 in num_constraints_involved:
                    num_constraints_involved[x1] += 1
                else:
                    if x1 in min_list:
                        num_constraints_involved[x1] = 1

            if x1 is not None:  # if x1 unassigned
                if x2 in num_constraints_involved:
                    num_constraints_involved[x2] += 1
                else:
                    if x2 in min_list:
                        num_constraints_involved[x2] = 1

        # add variables without constraints to list
        for x in min_list:
            if x not in num_constraints_involved:
                num_constraints_involved[x] = 0

        # find maximum degree variable from dictionary
        max_degree = -1
        max_var = None
        for x in num_constraints_involved:
            if num_constraints_involved[x] > max_degree:
                max_var = x
                max_degree = num_constraints_involved[x]

        return max_var

    # returns the list of domain values according to the heuristic called
    def order_domain_values(self, var, assignment, csp, domain):
        if self.lcv:
            return self.order_least_constraining_values(var, assignment, csp, domain)
        else:
            return domain[var]  # return values in basic order with no heuristic

    # returns the value that constrains the least values in neighbors
    def order_least_constraining_values(self, var, assignment, csp, domain):
        value_constraint_map = {}  # keys = variable values, values = total constraints
        var_domain = domain[var]
        # iterate over legal values for variable
        for val in var_domain:
            neighbors_with_val = 0
            # iterate over neighbors of variable
            for neighbor in csp.neighbor_map[var]:
                # increment neighbors_with_val if neighbor has val as legal value
                if val in domain[neighbor]:
                    neighbors_with_val += 1
            value_constraint_map[val] = neighbors_with_val

        # sort by min in var domain
        sorted_value_map = dict(sorted(value_constraint_map.items(), key=lambda item: item[1]))
        # return keys in sorted order
        return sorted_value_map.keys()

    def is_consistent(self, var, value, assignment, constraints):
        # loop over binary constraints
        for x1, x2 in constraints:
            # check every binary constraint involving variable
            if x1 == var:
                if assignment[x2] is not None:
                    x1_x2_constraint = constraints[(x1, x2)]
                    # check if value is legal for x1
                    if (value, assignment[x2]) not in x1_x2_constraint:
                        return False

            elif x2 == var:
                if assignment[x1] is not None:
                    x1_x2_constraint = constraints[(x1, x2)]
                    # check if value is legal for x2
                    if (assignment[x1], value) not in x1_x2_constraint:
                        return False

        return True

    # go through neighbors and remove value from domain based off assignment
    def update_domain(self, new_domain, constraints, var, value):
        for x1, x2 in constraints:
            if x1 == var:
                neighbor_domain = new_domain[x2]
                new_neighbor_domain = set()
                for neighbor_val in neighbor_domain:
                    if neighbor_val != value:
                        new_neighbor_domain.add(neighbor_val)
                new_domain[x1] = new_neighbor_domain
            elif x2 == var:
                neighbor_domain = new_domain[x1]
                new_neighbor_domain = set()
                for neighbor_val in neighbor_domain:
                    if neighbor_val != value:
                        new_neighbor_domain.add(neighbor_val)
                new_domain[x1] = new_neighbor_domain

        # reduce variable's domain to value
        new_domain[var] = {value}

    def inference(self, csp, var, value, domain, assignment):
        if self.ac3:
            return self.arc_consistency(csp, csp.constraints, domain, assignment)
        else:
            return True

    def arc_consistency(self, csp, constraints, domain, assignment):
        queue = []
        # add all initial arcs of csp to queue
        for neighbor_pair in constraints:
            queue.append(neighbor_pair)

        # iterate while queue is not empty
        while len(queue) > 0:
            x1, x2 = queue.pop(0)

            if self.remove_inconsistent_values(x1, x2, constraints, domain, assignment):
                for neighbor in csp.neighbor_map[x1]:
                    queue.append((neighbor, x1))

        # make automatic assignments and detect early failure
        for var in range(0, len(assignment)):
            var_domain = domain[var]
            if len(var_domain) == 1 and assignment[var] is None:
                # automatically make assignments if only one spot left in unassigned domain
                assignment[var] = next(iter(var_domain))
            elif len(var_domain) == 0:
                # return False if complete assignment impossible
                return False

        return True

    def remove_inconsistent_values(self, x1, x2, constraints, domain, assignment):
        removed = False
        # loop over values in domain of x1
        for val1 in domain[x1]:
            # check if value exists in domain of x2 that satisfies constraint (x1, x2)
            x1_x2_constraint = constraints[(x1, x2)]
            satisfied = False
            for val2 in domain[x2]:
                if (val1, val2) in x1_x2_constraint:
                    satisfied = True

            # if no value satisfies constraint
            if not satisfied:
                # remove value from domain of x1
                # adds all other values to new_domain and then setting domain to new_domain
                neighbor_domain = domain[x1]
                new_neighbor_domain = set()
                for neighbor_val in neighbor_domain:
                    if neighbor_val != val1:
                        new_neighbor_domain.add(neighbor_val)
                domain[x1] = new_neighbor_domain

                removed = True

        return removed
