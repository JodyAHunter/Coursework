# Name: Jody Hunter
# OSU Email: huntejod@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: A5: MinHeap Implementation
# Due Date: 05/30/2023
# Description: Implementation of the MinHeap data structure using Dynamic Array


from dynamic_array import *


class MinHeapException(Exception):
    """
    Custom exception to be used by MinHeap class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    pass


class MinHeap:
    def __init__(self, start_heap=None):
        """
        Initialize a new MinHeap
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._heap = DynamicArray()

        # populate MH with initial values (if provided)
        # before using this feature, implement add() method
        if start_heap:
            for node in start_heap:
                self.add(node)

    def __str__(self) -> str:
        """
        Return MH content in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        heap_data = [self._heap[i] for i in range(self._heap.length())]
        return 'HEAP ' + str(heap_data)

    def add(self, node: object) -> None:
        """
        Method that adds a node to a MinHeap and maintains heap property by
        moving the newly inserted node to its correct position.
        """
        # Add the new node to the end of the heap's underlying dynamic array
        self._heap.append(node)

        # initialize an index variable to the last element of the heap
        index = self._heap.length()-1

        # initialize a parent variable to the value of (index-1 // 2)
        parent = (index-1)//2

        # Loop while parent is greater than or equal to 0 and the value of
        # the parent index is greater than the child index (index)
        while parent >= 0 and self._heap[parent] > self._heap[index]:

            # swap the parent and the child values
            self._heap[parent], self._heap[index] = \
                self._heap[index], self._heap[parent]

            # update index to the value of child
            index = parent

            # update parent to the value of parent-1 // 2
            parent = (parent-1)//2


    def is_empty(self) -> bool:
        """
        Method that returns True if the heap is empty, otherwise returns False.
        """
        # Return True if heap's length (number of elements) is 0
        if self._heap.length() == 0:
            return True
        return False

    def get_min(self) -> object:
        """
        Method that returns the node with the smallest value in the heap.
        """
        # If the heap is empty, raises MinHeapException
        if self.is_empty():
            raise MinHeapException

        # Return the first element of the heap, by heap property, should be
        # the smallest value
        return self._heap.get_at_index(0)

    def remove_min(self) -> object:
        """
        Method that removes the smallest element from the heap, then percolates
        down the heap from the root, modifying elements to maintain heap
        property.
        """
        # Raise MinHeapException if the heap is empty
        if self._heap.length() == 0:
            raise MinHeapException

        # initialize a min_value variable to the first element of the heap
        min_value = self._heap[0]

        # Swap the first and last elements of the heap
        self._heap[0], self._heap[(self._heap.length()-1)] = \
            self._heap[self._heap.length()-1], self._heap[0]

        # Remove the last element in the heap
        self._heap.remove_at_index(self._heap.length()-1)

        # If only one element in heap after removal, return min_value
        if self._heap.length() == 1:
            return min_value

        # Call _percolate_down function starting at the root element
        elif self._heap.length() > 0:
            _percolate_down(self._heap, 0)

        # Return the min value that was removed
        return min_value


    def build_heap(self, da: DynamicArray) -> None:
        """
        Method that takes a dynamic array and creates a MinHeap from it,
        overwriting the current MinHeap of the object calling the method.
        """
        # Starting with the first non leaf element of the given array,
        # percolate down to the root element by going backwards one
        # index at a time
        for i in range(da.length()//2 - 1, -1, -1):
            _percolate_down(da, i)

        # Call the clear method to give the current heap a new blank array
        self.clear()

        # Append each element of the given array that has been percolated down
        # to the newly cleared underlying array of the heap object
        for i in range(da.length()):
            self._heap.append(da[i])

    def size(self) -> int:
        """
        Method that returns the number of elements in the heap.
        """
        # Return number of elements of the underlying dynamic array of the heap
        return self._heap.length()

    def clear(self) -> None:
        """
        Method that empties a heap by creating a new empty dynamic array
        and pointing the heap to the new empty dynamic array.
        """
        # Create a new empty dynamic array object
        new_da = DynamicArray()

        # Make the new dynamic array the underlying array of the heap
        self._heap = new_da

def heapsort(da: DynamicArray) -> None:
    """
    Function that takes a dynamic array and sorts the array in non-ascending
    order
    """
    # Heapify the given dynamic array to build a proper heap
    for i in range(da.length()//2 - 1, -1, -1):
        _percolate_down(da, i)

    # Initialize a variable to the index of the last element in the array
    k = da.length()-1

    # Sort the array by starting at the last index (k) and stepping backwards
    # through the array one element at a time
    # At each iteration, swap the root element and the element at index i
    # After swapping the values, call the _percolate_down_heapsort method
    for i in range(k, -1, -1):
        da[0], da[i] = da[i], da[0]
        _percolate_down_heapsort(da, 0, i)


# It's highly recommended that you implement the following optional          #
# function for percolating elements down the MinHeap. You can call           #
# this from inside the MinHeap class. You may edit the function definition.  #

def _percolate_down(da: DynamicArray, parent: int) -> None:
    """
    Function that percolates elements down the MinHeap to place them in the
    correct spot to maintain heap property.
    """
    # initialize child variable with index equal to 2 * parent index + 1
    # This will be the left child by default
    child = 2*parent+1

    # Case where there is only 2 elements in heap
    # Swap the two is parent > child; Return
    if da.length() == 2:
        if da[parent] > da[child]:
            da[parent], da[child] = da[child], da[parent]
            return
        return

    # Loop until child index is out of bounds of the heap
    while child < da.length():

        # Case where there is only a left child
        if child+1 == da.length():
            child = child

        # If left child is greater than right child, make child = right child
        elif da[child] > da[child+1]:
            child = child+1

        # If parent is greater than child, swap elements
        if da[parent] > da[child]:
            da[parent], da[child] = da[child], da[parent]

        # Update parent to child
        parent = child

        # Update child to new parent's child
        child = 2*parent+1


def _percolate_down_heapsort(da: DynamicArray, parent: int, i: int) -> None:
    """
    Function that percolates elements down the MinHeap to place them in the
    correct spot to maintain heap property. This function is used specifically
    in the heapsort method. The difference between this function and the
    _percolate_down function is this function takes an index parameter (i)
    that provides the out-of-bounds limit for the while loop.
    """
    # initialize child variable with index equal to 2 * parent index + 1
    # This will be the left child by default
    child = 2*parent+1

    # Loop until child index is out of bounds of the heap portion
    while child < i:

        # Case where there is only a left child
        if child+1 == i:
            child = child

        # If left child is greater than right child, make child = right child
        elif da[child] > da[child+1]:
            child = child+1

        # If parent is greater than child, swap elements
        if da[parent] > da[child]:
            da[parent], da[child] = da[child], da[parent]

        # Update parent to child
        parent = child

        # Update child to new parent's child
        child = 2*parent+1

# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - add example 1")
    print("-------------------")
    h = MinHeap()
    print(h, h.is_empty())
    for value in range(300, 200, -15):
        h.add(value)
        print(h)

    print("\nPDF - add example 2")
    print("-------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    for value in ['monkey', 'zebra', 'elephant', 'horse', 'bear']:
        h.add(value)
        print(h)

    print("\nPDF - is_empty example 1")
    print("-------------------")
    h = MinHeap([2, 4, 12, 56, 8, 34, 67])
    print(h.is_empty())

    print("\nPDF - is_empty example 2")
    print("-------------------")
    h = MinHeap()
    print(h.is_empty())

    print("\nPDF - get_min example 1")
    print("-----------------------")
    h = MinHeap(['fish', 'bird'])
    print(h)
    print(h.get_min(), (h.get_min()))

    print("\nPDF - remove_min example 1")
    print("--------------------------")
    h = MinHeap([1, 10, 2, 9, 3, 8, 4, 7, 5, 6])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - remove_min example 2")
    print("--------------------------")
    h = MinHeap([-73255, -32005, -32005, -28494, -20332, 47683, 24389, 71598, 20449, 9332])
    while not h.is_empty() and h.is_empty() is not None:
        print(h, end=' ')
        print(h.remove_min())

    print("\nPDF - build_heap example 1")
    print("--------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    h = MinHeap(['zebra', 'apple'])
    print(h)
    h.build_heap(da)
    print(h)

    print("--------------------------")
    print("Inserting 500 into input DA:")
    da[0] = 500
    print(da)

    print("Your MinHeap:")
    print(h)
    if h.get_min() == 500:
        print("Error: input array and heap's underlying DA reference same object in memory")

    print("\nPDF - heapsort example 1")
    print("------------------------")
    da = DynamicArray([100, 20, 6, 200, 90, 150, 300])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 2")
    print("------------------------")
    da = DynamicArray(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - heapsort example 3")
    print("------------------------")
    da = DynamicArray([44986, 4628])
    print(f"Before: {da}")
    heapsort(da)
    print(f"After:  {da}")

    print("\nPDF - size example 1")
    print("--------------------")
    h = MinHeap([100, 20, 6, 200, 90, 150, 300])
    print(h.size())

    print("\nPDF - size example 2")
    print("--------------------")
    h = MinHeap([])
    print(h.size())

    print("\nPDF - clear example 1")
    print("---------------------")
    h = MinHeap(['monkey', 'zebra', 'elephant', 'horse', 'bear'])
    print(h)
    print(h.clear())
    print(h)
