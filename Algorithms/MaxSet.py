# Jody Hunter - Assignment 4, Question 1

def max_independent_set(nums):
    """Function that takes a given array of integers and returns an array
    consisting of the integers used to find the highest possible sum without
    using adjacent integers."""

    # If the integer with the highest value is 0, return a list with only 0
    if max(nums) == 0:
        return [0]

    # If the integer with the highest value is -1, return an empty list
    if max(nums) == -1:
        return []

    # size of the array given
    n = len(nums)

    # memoization array
    cache = [0] * n

    for i in range(n):
        # First value of cache will be the first value of the given array,
        # unless it is a negative value, then it will be 0
        if i == 0:
            cache[i] = max(nums[i], 0)

        # Second value of cache will be the highest value between cache[0] and
        # the first value of the given array
        elif i == 1:
            cache[i] = max(nums[i], cache[0])

        # After the second element, each index of cache will be the max value
        # between the current index of the given array plus the i-2th index
        # of cache or the value of cache[i-1]
        else:
            cache[i] = max(nums[i] + cache[i-2], cache[i-1])

    # Initialize an index variable equal to the last element of the cache
    index = n - 1
    # This array will store the integers used to form the highest sum
    nums_used = []

    # Backtracking while loop used to fill the nums_used array
    while index >= 0:
        # If adjacent values of cache are not the same value or index is 0
        # the value at the current index of the given array will be added and
        # index will be decremented by 2.
        # If the value to be added is negative, it will be skipped
        # and index will decrement by 1 without adding the value.
        # Otherwise, index is decremented by 1.
        if cache[index] != cache[index - 1] or index == 0:
            if nums[index] < 0:
                index -= 1
            else:
                nums_used.append(nums[index])
                index -= 2
        else:
            index -= 1

    return nums_used[::-1]
