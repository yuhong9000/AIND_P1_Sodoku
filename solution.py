assignments = []


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Find (b1,b2) where b1 and b2 are peers and the have same 2 values
    twin_values = [(b1,b2) for b1 in values.keys() for b2 in peers[b1] 
        if values[b1]==values[b2] and 
        len(values[b1])==len(values[b2])==2]

    # Eliminate the naked twins as possibilities for their peers
    # For each naked twins tuple
    for b1,b2 in twin_values:
        digits = values[b1] # Find their values
        # Find the twins' common peers
        twins_peer = [box for box in values.keys() if box in peers[b1] and box in peers[b2]]

        # For each twins' peer, eliminate naked twins as possibilities
        for box in twins_peer:
            values[box] = ''.join([c for c in values[box] if not(c in digits)])
    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

rows = 'ABCDEFGHI'
cols = '123456789'
# debugging code for sudoku of smaller size
#rows = 'ABCD'
#cols = '1234'
boxes = cross(rows,cols)
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
sqr_units = [cross(rs, cs) for  rs in ('ABC','DEF','GHI') 
    for cs in ('123','456','789')]
#sqr_units = [cross(rs,cs) for rs in ('AB','CD') for cs in ('12','34')]
diag_units = [[''.join(x) for x in list(zip(rows,cols))],[''.join(x) for x in list(zip(rows,cols[::-1]))]]

unitlist = row_units + col_units + sqr_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    #all_digits = '1234'
    for c in grid:
        if (c == '.'):
            values.append(all_digits)
        elif (c in all_digits):
            values.append(c)
    assert len(grid) == 81
    #assert len(grid) == 16
    return dict(zip(boxes,values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return
    
def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    # Find all boxes that has one assigned value
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    # Look for peers of solved boxes, and eliminate possibilities
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
                values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """

    # implementation general logic:
    # for each unit in unitlist
    # for each answer digit (check all digits in '123456789') 
    # find a list (named potential_box) of - all boxes that contain this digit
    # if we only find one such box, a.k.a., the list potential_box only has one item
    # we will change the solution of that box to digit in the dictionary values
    
    for unit in unitlist:
        for digit in '123456789':
            potential_box = [box for box in unit if digit in values[box]]
            if len(potential_box)==1:
                values[potential_box[0]] = digit 
            
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Use the Naked Twins Strategy
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    Using depth-first search and propagation, try all possible values.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')


