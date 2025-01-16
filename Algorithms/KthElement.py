# Jody Hunter - CS325 Assignment 2, Question 3

def kthElement(Arr1, Arr2, k):
    """Function that takes two sorted arrays and a value k, combines the two
    sorted arrays into one, and returns the kth value in the combined array."""
    # m is the number of elements in Arr1
    m = len(Arr1)
    # n is the number of elements in Arr2
    n = len(Arr2)
    # total_size of both arrays used to create a new combined array
    total_size = m + n

    # new array that will store the elements from both given arrays
    combined_array = [0] * total_size

    # i acts as the index of Arr1
    i = 0
    # j acts as the index of Arr2
    j = 0
    # acts as the index of the newly created combined array
    combined_array_index = 0

    # while loop until the end of either Arr1 or Arr2 is reached
    while i < m and j < n:
        # if value in Arr1 is less than value in Arr2
        if Arr1[i] < Arr2[j]:
            # Place value from Arr1 into combined array, increment Arr1 index
            combined_array[combined_array_index] = Arr1[i]
            i += 1
        # otherwise, place value from Arr2 into combined array, increment Arr2 index
        else:
            combined_array[combined_array_index] = Arr2[j]
            j += 1
        # increment combined array index
        combined_array_index += 1

    # fill the rest of the combined array with the values leftover from the previous loop
    while i < m:
        combined_array[combined_array_index] = Arr1[i]
        combined_array_index += 1
        i += 1

    while j < n:
        combined_array[combined_array_index] = Arr2[j]
        combined_array_index += 1
        j += 1

    # Return the kth value from the final array. Minus one due to zero indexing
    return combined_array[k-1]

