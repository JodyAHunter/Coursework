# Name: Jody Hunter
# OSU Email: huntejod@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 2: Dynamic Array and ADT Implementation
# Due Date: 05/01/2023
# Description: Implementation of various methods of the Bag ADT


from dynamic_array import *


class Bag:
    def __init__(self, start_bag=None):
        """
        Init new bag based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

        # populate bag with initial values (if provided)
        # before using this feature, implement add() method
        if start_bag is not None:
            for value in start_bag:
                self.add(value)

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "BAG: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da.get_at_index(_))
                          for _ in range(self._da.length())])
        return out + ']'

    def size(self) -> int:
        """
        Return total number of items currently in the bag
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def add(self, value: object) -> None:
        """
        Method that adds a new element to the bag.
        """
        self._da.append(value)

    def remove(self, value: object) -> bool:
        """
        Method that removes a given value from the bag. If an element is
        successfully removed, True is returned. Otherwise, False is returned.
        """
        # Iterate through elements in bag
        for i in range(self.size()):

            # If given value matches element in bag
            if self._da.get_at_index(i) == value:

                # Remove value at that index
                self._da.remove_at_index(i)

                return True

        return False

    def count(self, value: object) -> int:
        """
        Method that returns the number of occurrences of a given value.
        """
        # Initialize a counter variable
        count = 0

        # Iterate through elements of the bag
        for i in range(self.size()):

            # If given value matches value of index in bag
            if self._da.get_at_index(i) == value:

                # Increment counter
                count += 1

        return count

    def clear(self) -> None:
        """
        Method that removes every element in the bag by initializing a
        new dynamic array and setting self._da to the new array.
        """
        # Initialize a new, empty dynamic array
        new_data = DynamicArray()

        # Set self._da to the new, empty dynamic array
        self._da = new_data

    def equal(self, second_bag: "Bag") -> bool:
        """
        Method that takes a second bag and compares self to the second bag.
        If the two bahs have the exact same elements, the method returns True.
        Otherwise, it returns False.
        """
        # Case for when two empty bags are compared
        if self.size() == 0 and second_bag.size() == 0:
            return True

        # If the two bags don't have the same number of elements,
        # we know that they aren't equal
        if self.size() != second_bag.size():
            return False
        else:
            # Iterate over each element in the bag
            for i in range(self.size()):
                value_at_index = self._da.get_at_index(i)
                # Call the count method on the value at each index for both bags
                if self.count(value_at_index) !=\
                        second_bag.count(value_at_index):
                    # If the results are not equal, return False
                    return False
        return True

    def __iter__(self):
        """
        Method that allows the bag to iterate across itself.
        """
        self._index = 0

        return self

    def __next__(self):
        """
        Method that returns the next value in the bag, depending on the
        current index.
        """
        try:
            value = self._da[self._index]
        except DynamicArrayException:
            raise StopIteration

        self._index = self._index + 1

        return value


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# add example 1")
    bag = Bag()
    print(bag)
    values = [10, 20, 30, 10, 20, 30]
    for value in values:
        bag.add(value)
    print(bag)

    print("\n# remove example 1")
    bag = Bag([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(bag)
    print(bag.remove(7), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)
    print(bag.remove(3), bag)

    print("\n# count example 1")
    bag = Bag([1, 2, 3, 1, 2, 2])
    print(bag, bag.count(1), bag.count(2), bag.count(3), bag.count(4))

    print("\n# clear example 1")
    bag = Bag([1, 2, 3, 1, 2, 3])
    print(bag)
    bag.clear()
    print(bag)

    print("\n# equal example 1")
    bag1 = Bag([10, 20, 30, 40, 50, 60])
    bag2 = Bag([60, 50, 40, 30, 20, 10])
    bag3 = Bag([10, 20, 30, 40, 50])
    bag_empty = Bag()

    print(bag1, bag2, bag3, bag_empty, sep="\n")
    print(bag1.equal(bag2), bag2.equal(bag1))
    print(bag1.equal(bag3), bag3.equal(bag1))
    print(bag2.equal(bag3), bag3.equal(bag2))
    print(bag1.equal(bag_empty), bag_empty.equal(bag1))
    print(bag_empty.equal(bag_empty))
    print(bag1, bag2, bag3, bag_empty, sep="\n")

    bag1 = Bag([100, 200, 300, 200])
    bag2 = Bag([100, 200, 30, 100])
    print(bag1.equal(bag2))

    print("\n# __iter__(), __next__() example 1")
    bag = Bag([5, 4, -8, 7, 10])
    print(bag)
    for item in bag:
        print(item)

    print("\n# __iter__(), __next__() example 2")
    bag = Bag(["orange", "apple", "pizza", "ice cream"])
    print(bag)
    for item in bag:
        print(item)
