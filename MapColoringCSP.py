"""
Date: 10/18/21
Author: Tate Toussaint
Description: builds a model for the map coloring problem that can be solved using backtracking search
"""


class MapColoringCSP:
    def __init__(self, neighbor_set, region_dictionary, color_dictionary):
        self.num_variables = len(region_dictionary)
        self.values = set(color_dictionary.keys())  # color options
        self.domain = self.build_domain()

        self.region_dictionary = region_dictionary
        self.color_dictionary = color_dictionary

        neighbors = set()
        for pair in neighbor_set:
            neighbors.add((pair[0], pair[1]))  # original pair
            neighbors.add((pair[1], pair[0]))   # reversed pair; ensures constraints go both ways

        self.constraints = self.build_constraints(neighbors)
        self.neighbor_map = self.build_neighbor_map()

    # builds set of possible color values for each pair of regions
    def build_constraints(self, neighbor_list):
        constraints = {}     # constraint dictionary mapping keys of region
        for x1 in range(0, self.num_variables):
            for x2 in range(0, self.num_variables):
                pair = (x1, x2)
                if pair in neighbor_list:
                    pair_constraints = set()
                    for c1 in self.values:
                        for c2 in self.values:
                            if c1 != c2:
                                pair_constraints.add((c1, c2))

                    constraints[pair] = pair_constraints

        return constraints

    # builds a domain of the variables and all their starting values
    def build_domain(self):
        domain_map = {}  # keys = variables, values = list of possible values
        for i in range(0, self.num_variables):
            domain_map[i] = self.values  # set each variable's original domain to starting domain
        return domain_map

    # builds a map of the neighbors for each variable
    def build_neighbor_map(self):
        neighbor_map = {}  # key = variable, value = list of neighbor variables
        for x1, x2 in self.constraints:
            if x1 in neighbor_map:  # key already exists
                neighbor_set = neighbor_map[x1]
                if x2 not in neighbor_set:
                    neighbor_set.add(x2)
                neighbor_map[x1] = neighbor_set
            else:
                neighbor_map[x1] = {x2}

            if x2 in neighbor_map:  # key already exists
                neighbor_set = neighbor_map[x2]
                if x1 not in neighbor_set:
                    neighbor_set.add(x1)
                neighbor_map[x2] = neighbor_set
            else:
                neighbor_map[x2] = {x1}

        # add keys for variables with no neighbors
        for i in range(0, self.num_variables):
            if i not in neighbor_map:
                neighbor_map[i] = []

        return neighbor_map

    # prints the regions and corresponding colors
    def print_assignment(self, assignment):
        if assignment is None:
            print("Failure")
        else:
            s = ""
            for i in range(0, len(assignment)):
                region = self.region_dictionary[i]
                color = self.color_dictionary[assignment[i]]
                s += region + ": " + color + "\n"

            s += "\nAssignment: " + str(assignment)
            print(s)
