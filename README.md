# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: *Student should provide answer here*
The naked twins technique is implemented as following:
1. Find twin boxes and store them in a list of tuple
We use list comprehension to contrust a new list of tuple of 2 boxes if their values are the same
and they are peers
2. Iterate through every pair of twins. Find the peers that belong to both naked twins
We again use list comprehension to construct a list of boxes. Such a box will be inside both twins' peer list
3. Eliminate the naked twin possibilities for their peers
This is done iterating through all their peers and assign them a new string value where the naked twin values
are deleted.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: *Student should provide answer here*
To add diagonal sudoku as a new feature, we simply create a new unit list that has the two diaganol units.
Then we add this unit list to unitlist. 
Dictionaries units and peers will automatically take care of themselves with new added units.
The rest of the code will work just fine.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.