# Jody Hunter - Assignment 3, Question 1a and 1b

def topdown_helper(s1, s2, s1_len, s2_len, cache):
    """Helper function called by the Top-down Approach"""
    # Base Case: Either string 1 or string 2 is an empty string, return 0
    if s1_len == 0 or s2_len == 0:
        return 0

    # Sub-problem has already been solved, return value from cache
    if cache[s1_len][s2_len] > -1:
        return cache[s1_len][s2_len]

    # Case where the character from each string matches
    elif s1[s1_len-1] == s2[s2_len-1]:

        # Return 1 plus recursive call with length of strings decreased by 1
        cache[s1_len][s2_len] = 1 + topdown_helper(s1, s2, s1_len-1, s2_len-1, cache)
        return cache[s1_len][s2_len]

    # Case where the characters do not match, return the max value between two
    # separate recursive calls, one with string 1 length subtracted by 1 and
    # one with string 2 length subtracted by 1
    else:
        cache[s1_len][s2_len] = max(topdown_helper(s1, s2, s1_len-1, s2_len, cache),
                                    topdown_helper(s1, s2, s1_len, s2_len-1, cache))
        return cache[s1_len][s2_len]


def dna_match_topdown(DNA1, DNA2):
    """Top-down approach function for the DNA sequence problem"""
    s1_len = len(DNA1)
    s2_len = len(DNA2)

    # Initialize a two-dimensional array filled with -1 values
    cache = [[-1 for x in range(s2_len + 1)] for x in range(s1_len + 1)]

    # Call the helper function
    return topdown_helper(DNA1, DNA2, s1_len, s2_len, cache)


def dna_match_bottomup(DNA1, DNA2):
    """Bottom-up approach function for the DNA sequence problem"""
    s1_len = len(DNA1)
    s2_len = len(DNA2)

    # Initialize a two-dimensional array to store results
    cache = [[0 for x in range(s2_len + 1)] for x in range(s1_len + 1)]

    # Iteratively fill out the two-dimensional array
    for i in range(s1_len + 1):
        for j in range(s2_len + 1):
            # Base case: If either string is empty, make index value of 0
            if i == 0 or j == 0:
                cache[i][j] = 0
            # characters match, make index 1 + [i-1][j-1]
            elif DNA1[i - 1] == DNA2[j - 1]:
                cache[i][j] = cache[i - 1][j - 1] + 1
            # characters dont match, make index max value between [i-1][j] and [i][j-1]
            else:
                cache[i][j] = max(cache[i - 1][j], cache[i][j - 1])

    # Return value from the bottom right corner of two-dimensional table
    return cache[s1_len][s2_len]
