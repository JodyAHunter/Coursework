# Name: Jody Hunter
# OSU Email: huntejod@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 3: Linked List and ADT Implementation
# Due Date: 05/08/2023
# Description: Implementation of a singly linked list data structure


from SLNode import *


class SLLException(Exception):
    """
    Custom exception class to be used by Singly Linked List
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class LinkedList:
    def __init__(self, start_list=None) -> None:
        """
        Initialize new linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = SLNode(None)

        # populate SLL with initial values (if provided)
        # before using this feature, implement insert_back() method
        if start_list is not None:
            for value in start_list:
                self.insert_back(value)

    def __str__(self) -> str:
        """
        Return content of singly linked list in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'SLL ['
        node = self._head.next
        while node:
            out += str(node.value)
            if node.next:
                out += ' -> '
            node = node.next
        out += ']'
        return out

    def length(self) -> int:
        """
        Return the length of the linked list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        length = 0
        node = self._head.next
        while node:
            length += 1
            node = node.next
        return length

    def is_empty(self) -> bool:
        """
        Return True is list is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return not self._head.next

    # ------------------------------------------------------------------ #

    def insert_front(self, value: object) -> None:
        """
        Method that adds a new node to the beginning of the list,
        following the head of the list.
        """
        # Create a new Node with the given value
        new_node = SLNode(value)

        # Make the newly created node point to the node originally following
        # the head of the linked list
        new_node.next = self._head.next

        # Make the head of the linked list point to the newly created node
        self._head.next = new_node


    def insert_back(self, value: object) -> None:
        """
        Method that adds a new node to the end of a linked list.
        """

        # Create a new node with the given value
        new_node = SLNode(value)

        # If there is no node following the head (list has no values)
        if self._head.next == None:

            # Make the head point to the new node
            self._head.next = new_node

        else:
            # Create a variable to start at the beginning of the linked list
            current_node = self._head

            # While the current node doesn't point to None
            while current_node.next != None:
                # Set the variable to the following node
                current_node = current_node.next

            # When the current node is the last node,
            # make it point to the new node
            current_node.next = new_node

    def insert_at_index(self, index: int, value: object) -> None:
        """
        Method that takes a given index and value, and creates a new
        node with the given value, inserting it at the given index of the
        linked list.
        """
        # Case for invalid index given, which raises an Exception
        if index < 0 or index > self.length():
            raise SLLException

        # Case for when the index given is the first index of the list
        if index == 0:

            # Call the insert_front() method with the given value
            self.insert_front(value)
            return

        # Create a new node with the given value
        new_node = SLNode(value)

        # Create two variables to represent adjacent nodes
        previous_node = self._head
        current_node = self._head.next

        # i variable represents the index to be used in a while loop
        i = 0

        # Loop until i variable equals the given index
        while i < index:

            # Move both node variables to the next node in the list
            previous_node = current_node
            current_node = current_node.next
            i += 1

        # Point previous node to the new node
        previous_node.next = new_node
        # Point the new node to the current node
        new_node.next = current_node


    def remove_at_index(self, index: int) -> None:
        """
        Method that takes a given index and removes the node at that index.
        """
        # Case for invalid index given, raises Exception
        if index < 0 or index > self.length()-1:
            raise SLLException

        # Create two variables to represent adjacent nodes
        previous_node = self._head
        current_node = self._head.next

        # i variable represents the index to be used in a while loop
        i = 0

        # Loop until i variable equals the given index
        while i < index:

            # Move both node variables to the next node in the list
            previous_node = current_node
            current_node = current_node.next
            i += 1

        # Point the previous node to the node following the current node
        # This takes the current node out of the linked list
        previous_node.next = current_node.next


    def remove(self, value: object) -> bool:
        """
        Method that takes a given value and removes the first occurrence
        of the value from the linked list, if it exists. Returns True
        if value exists and is removed. Returns False otherwise.
        """
        # i variable represents the index to be used in a while loop
        i = 0

        # Create two variables to represent adjacent nodes
        previous_node = self._head
        current_node = self._head.next

        # Loop until i is equal to the length of the linked list
        while i < self.length():

            # If the value of the current node equals the given value
            if current_node.value == value:

                # Make previous node point to the node following current node
                previous_node.next = current_node.next
                return True
            # Increment i, move both variables to the next nodes in the list
            i += 1
            previous_node = current_node
            current_node = current_node.next
        return False

    def count(self, value: object) -> int:
        """
        Method that takes a value and returns how many times that
        value occurs in the linked list.
        """
        # Initialize i for index in while loop and a counter variable
        i = 0
        counter = 0

        # Initialize current node variable with first node of linked list
        current_node = self._head.next

        # Loop until i is equal to length of linked list
        while i < self.length():
            # If value of node equals value given, increment counter
            if current_node.value == value:
                counter += 1
            # Increment i and change current node to next node
            i += 1
            current_node = current_node.next

        return counter



    def find(self, value: object) -> bool:
        """
        Method that returns True if the given value exists in the
        linked list. Otherwise, returns False.
        """
        # i variable represents index for while loop
        i = 0

        # Initialize a current node variable starting with the first node
        current_node = self._head.next

        # Loop until i equals the length of the linked list
        while i < self.length():
            # Return True if the current node's value equals given value
            if current_node.value == value:
                return True
            # Increment i and move the current node to the following node
            i += 1
            current_node = current_node.next

        return False

    def slice(self, start_index: int, size: int) -> "LinkedList":
        """
        Method that takes a starting index and a size, representing
        a number of nodes, and returns a new linked list consisting
        of the number of elements given starting from the given index.
        """
        # Case that handles invalid start_index, raises Exception
        if start_index < 0 or start_index > self.length()-1:
            raise SLLException

        # Checks if the size given is non-positive or greater than the
        # available elements
        if size < 0 or self.length() < size:
            raise SLLException

        # Checks if the size given from starting index is greater than
        # available elements
        if start_index + size > self.length():
            raise SLLException

        # Create a new linked list
        new_linked_list = LinkedList()

        # i variable represents index for while loop
        i = 0

        # Initialize current node variable to the first node of linked list
        current_node = self._head.next
        # Initialize a current node variable to the head of the new list
        new_list_current = new_linked_list._head

        # Loop until i equals the starting index given
        while i < start_index:
            i += 1
            # Move current node to the following node
            current_node = current_node.next

        # Once i has reached the starting index, begin a second while loop
        while i <= start_index + size - 1:
            # Create a variable for a new node to be added to the new list
            # with the value of the current node from the original list
            new_list_node = SLNode(current_node.value)

            # Point the current new list node to the node just created
            new_list_current.next = new_list_node

            # Move the original list current node to the next node
            current_node = current_node.next

            # Move the new list current node to the next node
            new_list_current = new_list_current.next

            i += 1

        return new_linked_list


if __name__ == "__main__":

    print("\n# insert_front example 1")
    test_case = ["A", "B", "C"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_front(case)
        print(lst)

    print("\n# insert_back example 1")
    test_case = ["C", "B", "A"]
    lst = LinkedList()
    for case in test_case:
        lst.insert_back(case)
        print(lst)

    print("\n# insert_at_index example 1")
    lst = LinkedList()
    test_cases = [(0, "A"), (0, "B"), (1, "C"), (3, "D"), (-1, "E"), (5, "F")]
    for index, value in test_cases:
        print("Inserted", value, "at index", index, ": ", end="")
        try:
            lst.insert_at_index(index, value)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove_at_index example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6])
    print(f"Initial LinkedList : {lst}")
    for index in [0, 2, 0, 2, 2, -2]:
        print("Removed at index", index, ": ", end="")
        try:
            lst.remove_at_index(index)
            print(lst)
        except Exception as e:
            print(type(e))

    print("\n# remove example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [7, 3, 3, 3, 3]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# remove example 2")
    lst = LinkedList([1, 2, 3, 1, 2, 3, 1, 2, 3])
    print(f"Initial LinkedList, Length: {lst.length()}\n  {lst}")
    for value in [1, 2, 3, 1, 2, 3, 3, 2, 1]:
        print(f"remove({value}): {lst.remove(value)}, Length: {lst.length()}"
              f"\n {lst}")

    print("\n# count example 1")
    lst = LinkedList([1, 2, 3, 1, 2, 2])
    print(lst, lst.count(1), lst.count(2), lst.count(3), lst.count(4))

    print("\n# find example 1")
    lst = LinkedList(["Waldo", "Clark Kent", "Homer", "Santa Claus"])
    print(lst)
    print(lst.find("Waldo"))
    print(lst.find("Superman"))
    print(lst.find("Santa Claus"))

    print("\n# slice example 1")
    lst = LinkedList([1, 2, 3, 4, 5, 6, 7, 8, 9])
    ll_slice = lst.slice(1, 3)
    print("Source:", lst)
    print("Start: 1 Size: 3 :", ll_slice)
    ll_slice.remove_at_index(0)
    print("Removed at index 0 :", ll_slice)

    print("\n# slice example 2")
    lst = LinkedList([10, 11, 12, 13, 14, 15, 16])
    print("Source:", lst)
    slices = [(0, 7), (-1, 7), (0, 8), (2, 3), (5, 0), (5, 3), (6, 1)]
    for index, size in slices:
        print("Start:", index, "Size:", size, end="")
        try:
            print(" :", lst.slice(index, size))
        except:
            print(" : exception occurred.")
