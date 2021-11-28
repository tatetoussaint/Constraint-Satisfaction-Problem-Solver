"""
Date: 10/19/21
Author: Tate Toussaint
Description: tests the CSP solver on various map problems and circuit board problems
"""

from BacktrackingSearch import BacktrackingSearch
from MapColoringCSP import MapColoringCSP
from CircuitBoardCSP import CircuitBoardCSP


'''MAP PROBLEM'''
## Map Problem Australia
# seven regions: WA:0, NT:1, SA:2, Q:3, NSW:4, V:5, T:6
half_neighbors_australia = {(0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (2, 5), (3, 4), (4, 5)}
region_dictionary_australia = {0: "WA", 1: "NT", 2: "SA", 3: "Q", 4: "NSW", 5: "V", 6: "T"}
color_dictionary_australia = {0: "Red", 1: "Green", 2: "Blue"}

## Map Problem Canada
# ten regions: Y:0, NWT:1, N:2, BC:3, A:4, M:5, O:6, Q:7, NFL:8, NS:9
half_neighbors_canada = {(0, 1), (0, 3), (1, 2), (1, 3), (1, 4), (1, 5), (2, 4), (2, 5), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8)}
region_dictionary_canada = {0: "Y", 1: "NWT", 2: "N", 3: "BC", 4: "A", 5: "M", 6: "O", 7: "Q", 8: "NFL", 9: "NS"}
color_dictionary_canada = {0: "Red", 1: "Green", 2: "Blue", 3: "Yellow"}

## Initialize CSPs and Search
map_csp_australia = MapColoringCSP(half_neighbors_australia, region_dictionary_australia, color_dictionary_australia)
map_csp_canada = MapColoringCSP(half_neighbors_canada, region_dictionary_canada, color_dictionary_canada)
map_backtracking_search = BacktrackingSearch(mrv=True, degree=True, lcv=True, ac3=True)

## Canada Solution
print("\n--------------------------------------------------------------TEST 0: Canada Map w/ All heuristics + Inference---------------------------------------------------------------")
map_assignment = map_backtracking_search.backtracking_search(map_csp_canada)
map_csp_canada.print_assignment(map_assignment)
print("Nodes Visited: " + str(map_backtracking_search.recursive_calls) + "\n")
map_backtracking_search.recursive_calls = 0

## Australia Solution
print("-------------------------------------------------------------TEST 1: Australia Map w/ All heuristics + Inference-------------------------------------------------------------")
map_assignment = map_backtracking_search.backtracking_search(map_csp_australia)
map_csp_australia.print_assignment(map_assignment)
print("Nodes Visited: " + str(map_backtracking_search.recursive_calls))
map_backtracking_search.recursive_calls = 0

## Heuristic and Inference Tests
print("-----------------------------------------------------------TEST 2: Australia Map w/ all heuristics + no Inference-----------------------------------------------------------")
map_backtracking_search.ac3 = False  # turn off inference
map_assignment = map_backtracking_search.backtracking_search(map_csp_australia)
map_csp_australia.print_assignment(map_assignment)
print("Nodes Visited: " + str(map_backtracking_search.recursive_calls))
map_backtracking_search.recursive_calls = 0

print("\n------------------------------------------------------------TEST 3: Australia Map w/ no heuristics + no Inference------------------------------------------------------------")
map_backtracking_search.mrv = False  # turn off heuristics
map_backtracking_search.degree = False
map_backtracking_search.lcv = False
map_assignment = map_backtracking_search.backtracking_search(map_csp_australia)
map_csp_australia.print_assignment(map_assignment)
print("Nodes Visited: " + str(map_backtracking_search.recursive_calls))
map_backtracking_search.recursive_calls = 0

print("\n------------------------------------------------------------TEST 4: Australia Map w/ no heuristics + Inference------------------------------------------------------------")
map_backtracking_search.ac3 = True  # turn on inference
map_assignment = map_backtracking_search.backtracking_search(map_csp_australia)
map_csp_australia.print_assignment(map_assignment)
print("Nodes Visited: " + str(map_backtracking_search.recursive_calls))
map_backtracking_search.recursive_calls = 0



'''CIRCUIT BOARD PROBLEM'''
print("\n                                                                           +=====================+" +
      "\n===========================================================================| Circuit Board Tests |==========================================================================="
      "\n                                                                           +=====================+")

## Circuit Board Parameters
board_width = 10  # 10/20
board_height = 6  # 6/3
# components = {0: (3, 2), 1: (5, 2), 2: (2, 3), 3: (7, 1)}
components = {0: (3, 2), 1: (5, 2), 2: (2, 3), 3: (7, 1), 4: (3, 2), 5: (5, 2), 6: (2, 3), 7: (7, 1)}
# components = {0: (3, 2), 1: (5, 2), 2: (2, 3), 3: (7, 1), 4: (3, 1), 5: (5, 2), 6: (2, 3), 7: (7, 1), 8: (3, 1)}  # operates with exact expected values


# Initialize Circuit Board CSP
circuit_board_csp = CircuitBoardCSP(components, board_width, board_height)

print("\n------------------------------------------------------------TEST 0: Circuit Board w/ no heuristics + no Inference------------------------------------------------------------")
circuit_backtracking_search_1 = BacktrackingSearch(mrv=False, degree=False, lcv=False, ac3=False)
cb_assignment = circuit_backtracking_search_1.backtracking_search(circuit_board_csp)
circuit_board_csp.print_assignment(cb_assignment)
print("Nodes Visited: " + str(circuit_backtracking_search_1.recursive_calls))

print("\n------------------------------------------------------------------TEST 1: Circuit Board w/ mrv + no Inference----------------------------------------------------------------")
circuit_backtracking_search_1 = BacktrackingSearch(mrv=True, degree=False, lcv=False, ac3=False)
cb_assignment = circuit_backtracking_search_1.backtracking_search(circuit_board_csp)
circuit_board_csp.print_assignment(cb_assignment)
print("Nodes Visited: " + str(circuit_backtracking_search_1.recursive_calls))

print("\n----------------------------------------------------------------TEST 2: Circuit Board w/ degree + no Inference---------------------------------------------------------------")
circuit_backtracking_search_1 = BacktrackingSearch(mrv=False, degree=True, lcv=False, ac3=False)
cb_assignment = circuit_backtracking_search_1.backtracking_search(circuit_board_csp)
circuit_board_csp.print_assignment(cb_assignment)
print("Nodes Visited: " + str(circuit_backtracking_search_1.recursive_calls))

print("\n------------------------------------------------------------------TEST 3: Circuit Board w/ lcv + no Inference----------------------------------------------------------------")
circuit_backtracking_search_1 = BacktrackingSearch(mrv=False, degree=False, lcv=True, ac3=False)
cb_assignment = circuit_backtracking_search_1.backtracking_search(circuit_board_csp)
circuit_board_csp.print_assignment(cb_assignment)
print("Nodes Visited: " + str(circuit_backtracking_search_1.recursive_calls))

print("\n-----------------------------------------------------------TEST 4: Circuit Board w/ all heuristics + no Inference------------------------------------------------------------")
circuit_backtracking_search_1 = BacktrackingSearch(mrv=True, degree=True, lcv=True, ac3=False)
cb_assignment = circuit_backtracking_search_1.backtracking_search(circuit_board_csp)
circuit_board_csp.print_assignment(cb_assignment)
print("Nodes Visited: " + str(circuit_backtracking_search_1.recursive_calls))

print("\n--------------------------------------------------------------TEST 5: Circuit Board w/ no heuristics + Inference-------------------------------------------------------------")
circuit_backtracking_search_1 = BacktrackingSearch(mrv=False, degree=False, lcv=False, ac3=True)
cb_assignment = circuit_backtracking_search_1.backtracking_search(circuit_board_csp)
circuit_board_csp.print_assignment(cb_assignment)
print("Nodes Visited: " + str(circuit_backtracking_search_1.recursive_calls))

print("\n-------------------------------------------------------------TEST 6: Circuit Board w/ all heuristics + Inference-------------------------------------------------------------")
circuit_backtracking_search_1 = BacktrackingSearch(mrv=True, degree=True, lcv=True, ac3=True)
cb_assignment = circuit_backtracking_search_1.backtracking_search(circuit_board_csp)
circuit_board_csp.print_assignment(cb_assignment)
print("Nodes Visited: " + str(circuit_backtracking_search_1.recursive_calls))
