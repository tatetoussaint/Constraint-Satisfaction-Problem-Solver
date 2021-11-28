"""
Date: 10/20/21
Author: Tate Toussaint
Description: builds a model for the circuit board problem that can be solved using backtracking search
"""


class CircuitBoardCSP:
    def __init__(self, components, board_width, board_height):
        self.num_variables = len(components)
        self.board_width = board_width
        self.board_height = board_height
        self.components = components
        self.coordinates = self.build_coordinates()
        self.constraints = self.build_constraint_map()
        self.domain = self.build_domain()
        self.neighbor_map = self.build_neighbor_map()

    # builds the dictionary of possible coordinates for each component
    def build_domain(self):
        domain_map = {}  # key = component, value = coordinate tuples
        # loop through constraints
        for x1_id, x2_id in self.constraints:
            # get value combination list
            value_pair_list = self.constraints[(x1_id, x2_id)]

            # loop through values and add to domain map
            for value_pair in value_pair_list:
                x1_value = value_pair[0]

                if x1_id in domain_map:
                    curr_x1_domain = domain_map[x1_id]
                    # add to domain if x1 value not in value pair
                    if x1_value not in curr_x1_domain:
                        curr_x1_domain.add(x1_value)
                        domain_map[x1_id] = curr_x1_domain
                else:
                    domain_map[x1_id] = {x1_value}

        for comp_id in self.components:
            if comp_id not in domain_map:
                domain_map[comp_id] = set()

        return domain_map

    # creates a set of all the coordinates on the board
    def build_coordinates(self):
        coord_list = set()
        for x in range(0, self.board_width):
            for y in range(0, self.board_height):
                coord_list.add((x, y))
        return coord_list

    # builds the map of constraints for the components
    def build_constraint_map(self):
        constraint_map = {}  # keys = pairs of components, values = list of coordinates pairs that don't overlap

        # loop through a first component
        for c1_id in range(0, self.num_variables):
            comp1 = self.components[c1_id]
            c1_width = comp1[0]
            c1_height = comp1[1]
            # loop through board coordinates
            for c1_x, c1_y in self.coordinates:
                # skip loop if first component doesn't fit on board
                if not (c1_x + c1_width <= self.board_width and c1_y + c1_height <= self.board_height):
                    continue

                # loop through second component
                for c2_id in range(c1_id + 1, self.num_variables):
                    if c1_id == c2_id:
                        continue

                    comp2 = self.components[c2_id]
                    c2_width = comp2[0]
                    c2_height = comp2[1]
                    # loop through possible coordinates
                    for c2_x, c2_y in self.coordinates:
                        # continue if second component not on board
                        if not (c2_x + c2_width <= self.board_width and c2_y + c2_height <= self.board_height):
                            continue

                        # check if components don't overlap
                        c1_cords = (c1_x, c1_y)
                        c2_cords = (c2_x, c2_y)

                        # if two rectangles don't overlap add to constraint map possible values
                        if not self.overlap(c1_id, c1_cords, c2_id, c2_cords):
                            # add to constraint map
                            if (c1_id, c2_id) in constraint_map:
                                curr_values = constraint_map[(c1_id, c2_id)]
                                curr_values.add((c1_cords, c2_cords))
                                constraint_map[(c1_id, c2_id)] = curr_values
                            else:
                                constraint_map[(c1_id, c2_id)] = {(c1_cords, c2_cords)}

                            if (c2_id, c1_id) in constraint_map:
                                curr_values = constraint_map[(c2_id, c1_id)]
                                curr_values.add((c2_cords, c1_cords))
                                constraint_map[(c2_id, c1_id)] = curr_values
                            else:
                                constraint_map[(c2_id, c1_id)] = {(c2_cords, c1_cords)}

        return constraint_map

    # check if two rectangular components overlap
    def overlap(self, c1_id, c1_coords, c2_id, c2_coords):
        c1_dimensions = self.components[c1_id]  # width x height
        c2_dimensions = self.components[c2_id]  # width x height

        x1_top_right = c1_coords[0] + (c1_dimensions[0] - 1)
        x1_bottom_left = c1_coords[0]
        x2_top_right = c2_coords[0] + (c2_dimensions[0] - 1)
        x2_bottom_left = c2_coords[0]

        y1_top_right = c1_coords[1] + (c1_dimensions[1] - 1)
        y1_bottom_left = c1_coords[1]
        y2_top_right = c2_coords[1] + (c2_dimensions[1] - 1)
        y2_bottom_left = c2_coords[1]

        return not (x1_top_right < x2_bottom_left \
                    or x1_bottom_left > x2_top_right \
                    or y1_top_right < y2_bottom_left \
                    or y1_bottom_left > y2_top_right)

    # builds a map of the neighbors for each variable
    def build_neighbor_map(self):
        neighbor_map = {}
        # loop through components
        for comp_id in self.components:
            comp_neighbors = set()
            # loop through other components and make neighbor
            for neighbor_comp_id in self.components:
                if comp_id != neighbor_comp_id:
                    comp_neighbors.add(neighbor_comp_id)
            neighbor_map[comp_id] = comp_neighbors
        return neighbor_map

    # build the neighbor map from the constraints; can be used outside of circuit board for other constraint maps
    def build_neighbor_map_from_constraints(self):
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

    def print_assignment(self, assignment):
        if assignment is None:
            print("Failure")
            return

        coord_char_map = {}
        for i in range(0, len(assignment)):
            comp_width, comp_height = self.components[i]
            comp_bottom_left = assignment[i]
            for x in range(0, comp_width):
                for y in range (0, comp_height):
                    coord_x = comp_bottom_left[0] + x
                    coord_y = comp_bottom_left[1] + y
                    coord_char_map[(coord_x, coord_y)] = i

        # loop through board and print variable
        s = "Board:\n"
        for y in range(self.board_height - 1, -1, -1):
            for x in range(0, self.board_width):
                if (x, y) in coord_char_map:
                    s += chr(coord_char_map[(x, y)] + 97)
                else:
                    s += "."
            s += "\n"

        s += "\nAssignment: " + str(assignment)
        print(s)
