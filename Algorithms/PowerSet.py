# Jody Hunter - Assignment 4, Question 2

import copy

def powerset_helper(pointer, choices_made, input, result):
    """Helper function called by the powerset function"""
    # If index pointer has gone past the last element of the input array,
    # add a deep copy of the array of choices made to the result array,
    # return to previous call
    if (pointer > len(input)-1):
        result.append(copy.deepcopy(choices_made))
        return

    # Add the value from input array at the index of the pointer to choices_made
    choices_made.append(input[pointer])

    # Call helper function with index pointer incremented by 1
    powerset_helper(pointer + 1, choices_made, input, result)

    # Backtracking, remove the last value from choices made
    choices_made.pop()

    # Call helper function with index pointer incremented by 1
    powerset_helper(pointer + 1, choices_made, input, result)

def powerset(input):
    """Function that returns the powerset of an array of distinct numbers."""
    # Final powerset array that will be returned from function
    result = []

    # Index pointer initialized with value of 0
    pointer = 0

    # Call helper function, empty array will be the choices_made array
    powerset_helper(pointer, [], input, result)
    return result
