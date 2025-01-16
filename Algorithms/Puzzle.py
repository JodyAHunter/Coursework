from collections import deque

def solve_puzzle(board, source, destination):
    """Function that solves a 2D array of size N rows * M columns.
    Input: board, source, destination.
    Puzzle: A list of lists, each list represents a row in the rectangular puzzle.
    Each element is either ‘-’ for empty (passable) or ‘#’ for obstacle (impassable).
    Example: Puzzle = [
    ['-', '-', '-', '-', '-'],
    ['-', '-', '#', '-', '-'],
    ['-', '-', '-', '-', '-'],
    ['#', '-', '#', '#', '-'],
    ['-', '#', '-', '-', '-']
    ]
    Output: A list of tuples representing the indices of each position in the path.
    The first tuple should be the starting position, or source, and the last tuple
    should be the destination. If there is no valid path, None should be returned.
    Not an empty list, but the None object. If source and destination are same
    return the same cell.
    Extra Credit: Function will return a string with letters representing directions
    taken to get from source to destination i.e. 'LDDR' (left, down, down, right)
    """

    # n_rows & m_cols provide the number of rows and columns that make the matrix
    n_rows = len(board)
    m_cols = len(board[0])

    # 4 element array of tuples representing possible directions with their row,
    # col values and string letter used for the extra credit portion
    directions = [(0, -1, 'L'), (0, 1, 'R'), (-1, 0, 'U'), (1, 0, 'D')]

    # queue that begins with a tuple that holds 3 values. The first value is a
    # tuple containing the current cell by its row, column values. This starts
    # as the source cell. The second value is an array that starts with just the
    # source cell. This array will represent the path taken to get to the
    # current cell. The third value starts as an empty string. This will hold
    # the directions taken to get to the current cell, for the extra credit
    queue = deque([(source, [source], "")])

    # array that holds all of the cells that have been visited, initialized with
    # source cell, as that is where the puzzle begins
    visited = [source]

    def is_valid(x, y):
        """Helper function that takes a row, col or x, y pair and confirms if it
        is a valid location on the puzzle board."""
        if 0 <= x < n_rows and 0 <= y < m_cols and board[x][y] == '-' and \
                (x, y) not in visited:
            return True

    while queue:
        # dequeue with tuple unpacking
        (row, col), path, direction_string = queue.popleft()
        # If source == destination, return the path, should just be source cell
        if source == destination:
            return path
        # Iterate over each possible direction with tuple unpacking
        for (x, y, dir) in directions:
            next_x = row + x
            next_y = col + y
            # Test validity of adjacent cell with helper function
            if is_valid(next_x, next_y):
                # If at destination, return path and string along with new cell
                if (next_x, next_y) == destination:
                    return path + [(next_x, next_y)], direction_string + dir
                # Otherwise, append to queue with (new cell, updated path, updated string
                queue.append(((next_x, next_y),
                              path + [(next_x, next_y)],
                              direction_string + dir))
                # Add new cell to visited array
                visited.append((next_x, next_y))
    return None

