# Name: Jody Hunter
# OSU Email: huntejod@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 2: Dynamic Array and ADT Implementation
# Due Date: 05/01/2023
# Description: Implementation of various methods of Dynamic Array data structure


from static_array import StaticArray


class DynamicArrayException(Exception):
    """
    Custom exception class to be used by Dynamic Array
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class DynamicArray:
    def __init__(self, start_array=None):
        """
        Initialize new dynamic array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._size = 0
        self._capacity = 4
        self._data = StaticArray(self._capacity)

        # populate dynamic array with initial values (if provided)
        # before using this feature, implement append() method
        if start_array is not None:
            for value in start_array:
                self.append(value)

    def __str__(self) -> str:
        """
        Return content of dynamic array in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "DYN_ARR Size/Cap: "
        out += str(self._size) + "/" + str(self._capacity) + ' ['
        out += ', '.join([str(self._data[_]) for _ in range(self._size)])
        return out + ']'

    def __iter__(self):
        """
        Create iterator for loop
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._index = 0
        return self

    def __next__(self):
        """
        Obtain next value and advance iterator
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        try:
            value = self[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index += 1
        return value

    def get_at_index(self, index: int) -> object:
        """
        Return value from given index position
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        return self._data[index]

    def set_at_index(self, index: int, value: object) -> None:
        """
        Store value at given index in the array
        Invalid index raises DynamicArrayException
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if index < 0 or index >= self._size:
            raise DynamicArrayException
        self._data[index] = value

    def __getitem__(self, index) -> object:
        """
        Same functionality as get_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self.get_at_index(index)

    def __setitem__(self, index, value) -> None:
        """
        Same functionality as set_at_index() method above,
        but called using array[index] syntax
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.set_at_index(index, value)

    def is_empty(self) -> bool:
        """
        Return True is array is empty / False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size == 0

    def length(self) -> int:
        """
        Return number of elements stored in array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return the capacity of the array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    def print_da_variables(self) -> None:
        """
        Print information contained in the dynamic array.
        Used for testing purposes.
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        print(f"Length: {self._size}, Capacity: {self._capacity}, {self._data}")

    # -----------------------------------------------------------------------

    def resize(self, new_capacity: int) -> None:
        """
        Method that takes an integer and modifies the dynamic array's capacity
        to the new capacity passed as an argument.
        """
        # Checks if the given integer for the new capacity is too small
        # This means less than the size of the array or a non-positive integer
        if new_capacity < self._size or new_capacity < 1:
            return

        # Initialize a new static array with the new capacity given
        new_data = StaticArray(new_capacity)

        # Copy over the data from the original array to the newly created array
        for i in range(self._size):
            new_data[i] = self._data[i]

        # Update the original array's capacity to the new capacity given
        self._capacity = new_capacity

        # Update the original array's data to be the data of the new array
        self._data = new_data


    def append(self, value: object) -> None:
        """
        Method that adds a passed value to the end of the array's data.
        If the array's data has reached capacity, it will call the resize
        method to double the array's current capacity.
        """
        # Checks if the array has reached its capacity for data
        if self._size == self._capacity:

            # If capacity is reached, calls resize method to double current cap
            self.resize(self._capacity*2)

        # Places passed value at the end of data array
        self._data[self._size] = value

        # Increment size by 1
        self._size += 1

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Method that takes an integer representing an index and places a
        given value at the given index in the data of the array. It then shifts
        all other values to the right of the inserted value index.
        """
        # Checks for invalid index input and raises Exception
        if index < 0 or index > self._size:
            raise DynamicArrayException

        # If number of elements in data has reached current capacity
        # Resize method is called to double the current capacity
        if self._size == self._capacity:
            self.resize(self._capacity*2)

        # Iterates from number of elements - 1 backwards to the given index
        for i in range(self._size-1, index-1, -1):

            # The value of each index to the right of the given index where
            # given value is inserted is pushed to the right by 1 index
            self._data[i+1] = self._data[i]

        # The given value is placed at the given index now available
        self._data[index] = value

        # Increment number of elements in data by 1
        self._size += 1


    def remove_at_index(self, index: int) -> None:
        """
        Method that takes an integer representing an index and removes
        the value in data from that index. It then shifts the other
        values to fill in the index where the value was removed.
        """
        # Checks for invalid index input and raises Exception
        if index < 0 or index > self._size-1:
            raise DynamicArrayException

        # Checks if the number of elements is less than a quarter of capacity
        # This is the condition to resize the array's capacity
        if self._size < self._capacity*0.25:

            # Original capacity must be above 10 or do not resize at all
            # If the resized capacity would be less than 10
            if self._capacity > 10 and self._size * 2 < 10:

                # It is always resized with the new capacity of 10
                self.resize(10)

            # If resized capacity would be greater than or equal to 10
            # Resize new capacity to be double the current size
            elif self._capacity > 10 and self._size * 2 >= 10:
                self.resize(self._size*2)

        # If given index is the last element of the array, change val to None
        # No rotation of other elements needed
        if index == self._size-1:
            self._data[self._size-1] = None
            self._size -= 1
            return

        # Iterate from the index given up to but not including the last element
        for i in range(index, self._size-1):

            # Current iterated index becomes the value of the index following it
            # This shifts over the data to fill in the removed value's place
            self._data[i] = self._data[i+1]

        # Changes the original last data element to None after all values shift
        self._data[self._size-1] = None

        # Decrement the number of elements in data by 1
        self._size -= 1


    def slice(self, start_index: int, size: int) -> "DynamicArray":
        """
        Method that takes two integers, one representing a starting index,
        and one representing the size of a new dynamic array to be returned.
        The new dynamic array should be sliced from the original array,
        beginning at the starting index and the total number of elements
        should be equal to the number passed for the size.
        """
        # Checks if the start index given is an invalid index
        if start_index < 0 or start_index > self._size-1:
            raise DynamicArrayException

        # Checks if the size given is non-positive or greater than the
        if size < 0 or self._size < size:
            raise DynamicArrayException

        # Checks if the size given from starting is index is greater than
        # available elements
        if start_index + size > self._size:
            raise DynamicArrayException

        # Initialize a new array to be returned
        new_dyn_arr = DynamicArray()

        # Iterate from starting index to the last index of the given size
        for i in range(start_index, start_index+size):

            # Call append method to fill the new array with values from
            # the original array
            new_dyn_arr.append(self._data[i])

        return new_dyn_arr

    def merge(self, second_da: "DynamicArray") -> None:
        """
        Method that takes a second dynamic array and adds each element
        to the original array in the same order they are stored.
        """
        # Iterate through the second array
        for i in range(second_da._size):

            # Add each element by iterated index to the original array
            self.append(second_da._data[i])

    def map(self, map_func) -> "DynamicArray":
        """
        Method that takes a given function and returns a new dynamic array
        that is filled by using the given array on each index of the original
        array.
        """
        # Initialize a new dynamic array object
        new_dyn_arr = DynamicArray()

        # Iterate through the range of the size of the original array
        for i in range(self._size):

            # Use the append method with the value being the result
            # of the given function used on each element of original array
            new_dyn_arr.append(map_func(self._data[i]))

        return new_dyn_arr


    def filter(self, filter_func) -> "DynamicArray":
        """
        Method that takes a filter function and returns a new dynamic array.
        The returned array is filled with the values that return True from
        the filter function.
        """
        # Initialize a new dynamic array object
        new_dyn_arr = DynamicArray()

        # Iterate through the elements of the original array
        for i in range(self._size):

            # The filter function is called with the index of the original
            # array's data as input. If the filter function returns True
            # for that index, the value of data is added to the new array
            if filter_func(self._data[i]) == True:
                new_dyn_arr.append(self._data[i])

        return new_dyn_arr



    def reduce(self, reduce_func, initializer=None) -> object:
        """
        Method that takes a reduce function and an optional initializer.
        The reduce function acts on every element in the array, starting
        with the initializer if given, or the first element of the array
        if an initializer is not given. The final result is returned.
        """
        # Set a final_value variable equal to the value of the initializer
        final_value = initializer

        # Case for if no initializer is given
        if final_value == None:
            final_value = self._data[0]
            for i in range(1, self._size):
                final_value = reduce_func(final_value, self._data[i])

        # Case for if an initializer is given
        else:
            for i in range(self._size):
                final_value = reduce_func(final_value, self._data[i])

        return final_value


def find_mode(arr: DynamicArray) -> (DynamicArray, int):
    """
    Function that takes a dynamic array and creates a new dynamic array
    that is filled with the mode values of the original array.
    """
    # Create a new dynamic array object that will be returned by function
    new_dyn_arr = DynamicArray()

    # Initialize a counter variable to 1 for the occurrence of the first index
    counter = 1

    # This variable will hold the count for the value that occurs the most
    highest_count = 1

    # Iterate the original array, tracking the highest number of occurrences
    for i in range(1, arr.length()):

        # Compare value of current index to value of following index
        if arr.get_at_index(i) == arr.get_at_index(i-1):

            # Update counter if two sequential values are equal
            counter += 1

            if counter > highest_count:
                # Value of counter becomes the new highest count

                highest_count = counter

        # If two sequential values aren't equal, reset counter to 1
        else:
            counter = 1

    # Reset counter to 1
    counter = 1

    # Add first value of array to new array if mode's occurrence count is 1
    if highest_count == 1:
        new_dyn_arr.append(arr.get_at_index(0))

    # Iterate through the original array a second time, starting with the
    # second index, comparing counter to the highest_count variable.
    # When counter is equivalent to the highest_count variable, that
    # value is added to the new array
    for i in range(1, arr.length()):

        if arr.get_at_index(i) == arr.get_at_index(i-1):
            counter += 1
            if counter == highest_count:
                new_dyn_arr.append(arr.get_at_index(i))

        elif arr.get_at_index(i) != arr.get_at_index(i-1):
            counter = 1
            if counter == highest_count:
                new_dyn_arr.append(arr.get_at_index(i))


    return new_dyn_arr, highest_count



# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# resize - example 1")
    da = DynamicArray()

    # print dynamic array's size, capacity and the contents
    # of the underlying static array (data)
    da.print_da_variables()
    da.resize(8)
    da.print_da_variables()
    da.resize(2)
    da.print_da_variables()
    da.resize(0)
    da.print_da_variables()

    print("\n# resize - example 2")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8])
    print(da)
    da.resize(20)
    print(da)
    da.resize(4)
    print(da)

    print("\n# append - example 1")
    da = DynamicArray()
    da.print_da_variables()
    da.append(1)
    da.print_da_variables()
    print(da)

    print("\n# append - example 2")
    da = DynamicArray()
    for i in range(9):
        da.append(i + 101)
        print(da)

    print("\n# append - example 3")
    da = DynamicArray()
    for i in range(600):
        da.append(i)
    print(da.length())
    print(da.get_capacity())

    print("\n# insert_at_index - example 1")
    da = DynamicArray([100])
    print(da)
    da.insert_at_index(0, 200)
    da.insert_at_index(0, 300)
    da.insert_at_index(0, 400)
    print(da)
    da.insert_at_index(3, 500)
    print(da)
    da.insert_at_index(1, 600)
    print(da)

    print("\n# insert_at_index example 2")
    da = DynamicArray()
    try:
        da.insert_at_index(-1, 100)
    except Exception as e:
        print("Exception raised:", type(e))
    da.insert_at_index(0, 200)
    try:
        da.insert_at_index(2, 300)
    except Exception as e:
        print("Exception raised:", type(e))
    print(da)

    print("\n# insert at index example 3")
    da = DynamicArray()
    for i in range(1, 10):
        index, value = i - 4, i * 10
        try:
            da.insert_at_index(index, value)
        except Exception as e:
            print("Cannot insert value", value, "at index", index)
    print(da)

    print("\n# remove_at_index - example 1")
    da = DynamicArray([10, 20, 30, 40, 50, 60, 70, 80])
    print(da)
    da.remove_at_index(0)
    print(da)
    da.remove_at_index(6)
    print(da)
    da.remove_at_index(2)
    print(da)

    print("\n# remove_at_index - example 2")
    da = DynamicArray([1024])
    print(da)
    for i in range(17):
        da.insert_at_index(i, i)
    print(da.length(), da.get_capacity())
    for i in range(16, -1, -1):
        da.remove_at_index(0)
    print(da)

    print("\n# remove_at_index - example 3")
    da = DynamicArray()
    print(da.length(), da.get_capacity())
    [da.append(1) for i in range(100)]  # step 1 - add 100 elements
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(68)]  # step 2 - remove 68 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 3 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 4 - remove 1 element
    print(da.length(), da.get_capacity())
    [da.remove_at_index(0) for i in range(14)]  # step 5 - remove 14 elements
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 6 - remove 1 element
    print(da.length(), da.get_capacity())
    da.remove_at_index(0)  # step 7 - remove 1 element
    print(da.length(), da.get_capacity())

    for i in range(14):
        print("Before remove_at_index(): ", da.length(), da.get_capacity(), end="")
        da.remove_at_index(0)
        print(" After remove_at_index(): ", da.length(), da.get_capacity())

    print("\n# remove at index - example 4")
    da = DynamicArray([1, 2, 3, 4, 5])
    print(da)
    for _ in range(5):
        da.remove_at_index(0)
        print(da)

    print("\n# slice example 1")
    da = DynamicArray([1, 2, 3, 4, 5, 6, 7, 8, 9])
    da_slice = da.slice(1, 3)
    print(da, da_slice, sep="\n")
    da_slice.remove_at_index(0)
    print(da, da_slice, sep="\n")

    print("\n# slice example 2")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    print("SOURCE:", da)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1), (6, -1)]
    for i, cnt in slices:
        print("Slice", i, "/", cnt, end="")
        try:
            print(" --- OK: ", da.slice(i, cnt))
        except:
            print(" --- exception occurred.")

    print("\n# slice example 3")
    da = DynamicArray([10, 11, 12, 13, 14, 15, 16])
    da_slice = da.slice(0, 7)
    print(da, da_slice, sep="\n")


    print("\n# merge example 1")
    da = DynamicArray([1, 2, 3, 4, 5])
    da2 = DynamicArray([10, 11, 12, 13])
    print(da)
    da.merge(da2)
    print(da)

    print("\n# merge example 2")
    da = DynamicArray([1, 2, 3])
    da2 = DynamicArray()
    da3 = DynamicArray()
    da.merge(da2)
    print(da)
    da2.merge(da3)
    print(da2)
    da3.merge(da)
    print(da3)

    print("\n# map example 1")
    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    print(da.map(lambda x: x ** 2))

    print("\n# map example 2")


    def double(value):
        return value * 2


    def square(value):
        return value ** 2


    def cube(value):
        return value ** 3


    def plus_one(value):
        return value + 1


    da = DynamicArray([plus_one, double, square, cube])
    for value in [1, 10, 20]:
        print(da.map(lambda x: x(value)))

    print("\n# filter example 1")


    def filter_a(e):
        return e > 10


    da = DynamicArray([1, 5, 10, 15, 20, 25])
    print(da)
    result = da.filter(filter_a)
    print(result)
    print(da.filter(lambda x: (10 <= x <= 20)))

    print("\n# filter example 2")


    def is_long_word(word, length):
        return len(word) > length


    da = DynamicArray("This is a sentence with some long words".split())
    print(da)
    for length in [3, 4, 7]:
        print(da.filter(lambda word: is_long_word(word, length)))

    print("\n# reduce example 1")
    values = [100, 5, 10, 15, 20, 25]
    da = DynamicArray(values)
    print(da)
    print(da.reduce(lambda x, y: (x // 5 + y ** 2)))
    print(da.reduce(lambda x, y: (x + y ** 2), -1))

    print("\n# reduce example 2")
    da = DynamicArray([100])
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))
    da.remove_at_index(0)
    print(da.reduce(lambda x, y: x + y ** 2))
    print(da.reduce(lambda x, y: x + y ** 2, -1))

    print("\n# find_mode - example 1")
    test_cases = (
        [1, 1, 2, 3, 3, 4],
        [1, 2, 3, 4, 5],
        ["Apple", "Banana", "Banana", "Carrot", "Carrot",
         "Date", "Date", "Date", "Eggplant", "Eggplant", "Eggplant",
         "Fig", "Fig", "Grape"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}\n")

    case = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    da = DynamicArray()
    for x in range(len(case)):
        da.append(case[x])
        mode, frequency = find_mode(da)
        print(f"{da}\nMode: {mode}, Frequency: {frequency}")
