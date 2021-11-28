### CSP Solver Analysis
### Tate Toussaint

# Definitions

Minimum Remaining Value Heuristic (MRV): This heuristic selects the unassigned variable with the minimum remaining domain values as the next variable to assign.

Degree Heuristic: This heuristic, often used as a tiebreak alongside the MRV heuristic, selects the unassigned variable with the largest number of neighbors as the next variable to assign.

Least Constraining Value Heuristic (LCV): This heuristic selects the value to assign a given variable that is involved in the least number of constraints with neighboring variables.

Arc Consistency Inference (AC-3): This method of inference loops through the variable domains and reduces them, making assignments when a domain is reduced to one. The algorithm is described in more depth here: https://en.m.wikipedia.org/wiki/AC-3_algorithm.

# Results

To test the time complexity of the CSP solver with different combinations of heuristics and inference, I solve the circuit board problem on a controlled 6x10 board with 8 total components that leave only 6 gaps.

Using `Test 0` as a baseline, the solver visits 29447 nodes when there are no heuristics or inference. This is expected to be a large number as AC-3 cannot reduce the domain and the heuristics cannot improve the rate of pruning.

With only MRV, `Test 1` visits 1317 nodes, which illustrates the effectiveness of choosing the variable with the fewest remaining values. This works because choosing the variable with the minimum remaining values is more likely to fail sooner than other variables, pruning the current search tree quicker.

In `Test 2` with only degree, the solver again visits 29447 nodes, which is the same amount of nodes that were visited with no heuristic despite using the degree heuristic. This is because the degree heuristic does not have any effect on the circuit board problem, as all components are initialized with all other components as their neighbors. The degree heuristic could have an effect on a CSPs such as the map coloring problem where variables can have different number of neighbors.

`Test 3` runs with only LCV and visits 1751 nodes, which shows the effectiveness of choosing the value involved in the least constraints on unassigned neighbors. This strategy works as it maximizes flexibility for future variable assignments as the domains of the neighboring variables will be reduced less. 

Combining the three heuristics, `Test 4` visits 2046 nodes which surprisingly is slightly more than MRV or LCV individually. However, I this is likely due to chance as other boards have resulted in fewer nodes visited when combining the heuristics. Further analysis would be necessary to test the effectiveness of combining the heuristics together over various problems.

The use of no heuristics and just inference in `Test 5` resulted in 299 nodes visited, which is far less than any combination of heuristics without inference. This is because the use of AC-3 for inference reduces the domains of variables that aren't arc consistent at every iteration, as well as makes automatic assignments to variables whose domain is reduced to one. 

Switching on all the heuristics and inference in `Test 6` results in a slightly larger number of nodes visited at 494, but still is far less than any combinations without inference. In other (mainly more complicated) tests, the addition of heuristics to inference reduced the number of nodes visited, so the slight increase in this example is likely an outlier. 

Overall, all tests returned complete and consistent assignments with nodes visited following the rough range expected. These tests are still somewhat simple and more analysis should be done when there are less time and computational limitations. 
