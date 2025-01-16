# Name: Jody Hunter
# OSU Email: huntejod@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 3: Linked List and ADT Implementation
# Due Date: 05/08/2023
# Description: Implementation of Stack ADT with underlying singly linked list


from SLNode import SLNode


class StackException(Exception):
    """
    Custom exception to be used by Stack class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Stack:
    def __init__(self) -> None:
        """
        Initialize new stack with head node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = None

    def __str__(self) -> str:
        """
        Return content of stack in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'STACK ['
        if not self.is_empty():
            node = self._head
            out = out + str(node.value)
            node = node.next
            while node:
                out = out + ' -> ' + str(node.value)
                node = node.next
        return out + ']'

    def is_empty(self) -> bool:
        """
        Return True is the stack is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._head is None

    def size(self) -> int:
        """
        Return number of elements currently in the stack
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        node = self._head
        length = 0
        while node:
            length += 1
            node = node.next
        return length

    # -----------------------------------------------------------------------

    def push(self, value: object) -> None:
        """
        Method that adds a given value to the top of the stack.
        """
        # Initialize a variable with the head of the stack
        current_head = self._head

        # Create a new node with the given value
        new_node = SLNode(value)

        # Make the newly created node the new head of the stack
        self._head = new_node

        # Make the new head point to the previous head
        self._head.next = current_head

    def pop(self) -> object:
        """
        Method that removes and returns the value at the top of the stack.
        """
        # Raises an exception if the stack is empty
        if self.is_empty() == True:
            raise StackException

        # Initialize a variable with the value of the current head
        popped_head = self._head

        # Make the node following the head become the new head of the stack
        self._head = self._head.next

        # Return the variable with the previous head
        return popped_head.value

    def top(self) -> object:
        """
        Method that returns the value at the top of the stack without removing.
        """
        # Raises exception if the stack is empty
        if self.is_empty() == True:
            raise StackException

        # Return the value of the current head of the stack
        return self._head.value

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
