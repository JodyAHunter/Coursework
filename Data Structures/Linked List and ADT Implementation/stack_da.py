# Name: Jody Hunter
# OSU Email: huntejod@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 3: Linked List and ADT Implementation
# Due Date: 05/08/2023
# Description: Implementation of Stack ADT with underlying dynamic array


from dynamic_array import *


class StackException(Exception):
    """
    Custom exception to be used by Stack class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Stack:
    def __init__(self):
        """
        Init new stack based on Dynamic Array
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._da = DynamicArray()

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = "STACK: " + str(self._da.length()) + " elements. ["
        out += ', '.join([str(self._da[i]) for i in range(self._da.length())])
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True is the stack is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.is_empty()

    def size(self) -> int:
        """
        Return number of elements currently in the stack
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._da.length()

    # -----------------------------------------------------------------------

    def push(self, value: object) -> None:
        """
        Method that adds the given value to the top of the stack.
        """
        # Call the underlying dynamic array append method with given value
        self._da.append(value)

    def pop(self) -> object:
        """
        Method that removes and returns the top value from the stack.
        """
        # Case that handles if stack is empty
        if self.is_empty() == True:
            raise StackException

        # Call underlying dynamic array get_at_index method on last index
        # Save the returned value from the last index to a variable
        popped_value = self._da.get_at_index(self.size()-1)

        # Call underlying dynamic array remove_at_index method on last index
        self._da.remove_at_index(self.size()-1)

        # Return the value that was popped from stack
        return popped_value



    def top(self) -> object:
        """
        Method that returns the top value of the stack, but does not
        remove it.
        """
        # Case that handles if the stack is empty
        if self.is_empty() == True:
            raise StackException

        # Call underlying dynamic array get_at_index method on last index
        # Save the returned value from the last index to a variable
        top_value = self._da.get_at_index(self.size()-1)

        # Return the top value variable
        return top_value


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# push example 1")
    s = Stack()
    print(s)
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    print(s)

    print("\n# pop example 1")
    s = Stack()
    try:
        print(s.pop())
    except Exception as e:
        print("Exception:", type(e))
    for value in [1, 2, 3, 4, 5]:
        s.push(value)
    for i in range(6):
        try:
            print(s.pop())
        except Exception as e:
            print("Exception:", type(e))

    print("\n# top example 1")
    s = Stack()
    try:
        s.top()
    except Exception as e:
        print("No elements in stack", type(e))
    s.push(10)
    s.push(20)
    print(s)
    print(s.top())
    print(s.top())
    print(s)
