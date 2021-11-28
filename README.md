### Constraint Satisfaction Problem Solver
### Tate Toussaint

Table of Contents
---------------------

 * Project Overview
 * Parts of the Constraint Satisfaction Solver
   * Backtracking Search
   * Map Coloring Problem
   * Circuit Board Problem
 * Running the Constraint Satisfaction Solver

Project Overview
---------------------

In this project, I create a constraint satisfaction solver that solves constraint satisfaction problems (CSPs) using backtracking search, AC-3 inference, and heuristics. The problem is shown on the map-coloring problem for Canada and Australia and the circuit board problem in `TestCSP.py`. Results from the algorithm, heuristics, and AC-3 are described in `results.md`.

Parts of the Constraint Satisfaction Solver
---------------------

The constraint satisfaction solver consists of three main parts: the backtracking search algorithm, map coloring csp, and circuit board csp.

### Backtracking Search

`BacktrackingSearch` takes in a constraint satisfaction problem with a domain and constraint dictionary and attempts to return a complete and consistent assignment for the variables. The algorithm recursively assigns values to unassigned variables according to heuristics that define and the order to explore nodes and select values. It also can make inferences using the AC-3 algorithm to make multiple variable assignments at each recursive iteration. The heuristics and inference methods are described in depth in `results.md`.

### Map Coloring Problem

Description: The map coloring problem aims to assign colors to each region of a map in such a way that no neighboring regions are assigned the same color. 

Implementation: `MapColoringCSP` takes in a set of tuples defining the neighboring regions in the map and two dictionaries mapping integers to their corresponding region names and integers to possible color values. It builds the domain and constraint maps using these the neighbor map and possible values.

### Circuit Board Problem

Description: Given a rectangular circuit board of size n x m and k rectangular components of arbitrary sizes, the circuit board attempts to lay out the components in such a way that they do not overlap.
```
Example:
      bbbbb   cc
aaa   bbbbb   cc  eeeeeee
aaa           cc

Possible 10x3 grid solution:
eeeeeee.cc
aaabbbbbcc
aaabbbbbcc
```

Implementation: `CircuitBoardCSP` takes in a list of components (represented by tuples of their width and height), the board width, and the board height. It then builds the domain by looping through each position on the grid and checking if the component fits on the board at each position. Similarly, it builds the constraint map by looping through each pair of components and their domains, checking if both components fit in the grid at each position in their domains.

Running the Constraint Satisfaction Solver
---------------------

To run the CSP solver on various example problems, run `TestCSP.py`. You can edit the parameters to the initializations of BacktrackingSearch to turn on and off the heuristics and AC-3. You can also manually add region dictionaries for new map coloring problems or adjust the size of the circuit board width/height and the number and size of components to experiment with the solver.

Example Output:
```
Board:
bbbbbaaacc
bbbbbaaacc
ddddddd.cc
gghhhhhhh.
ggfffeee..
ggfffeee..

Assignment: [(5, 4), (0, 4), (8, 3), (0, 3), (5, 0), (0, 0), (0, 0), (2, 2)]
Nodes Visited: 299
```
