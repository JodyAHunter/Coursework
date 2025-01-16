# Name: Jody Hunter
# OSU Email: huntejod@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 3: Linked List and ADT Implementation
# Due Date: 05/08/2023
# Description: Implementation of Queue ADT with underlying static array


# Note: Changing any part of the pre-implemented methods (besides adding  #
#       default parameters) will cause the Gradescope tests to fail.      #


from static_array import StaticArray


class QueueException(Exception):
    """Custom exception to be used by Queue class."""
    pass


class Queue:
    def __init__(self) -> None:
        """Initialize new queue based on Static Array."""
        self._sa = StaticArray(4)
        self._front = 0
        self._back = -1
        self._current_size = 0

    def __str__(self) -> str:
        """Override string method to provide more readable output."""

        size = self._current_size
        out = "QUEUE: " + str(size) + " element(s). ["

        front_index = self._front
        for _ in range(size - 1):
            out += str(self._sa[front_index]) + ', '
            front_index = self._increment(front_index)

        if size > 0:
            out += str(self._sa[front_index])

        return out + ']'

    def is_empty(self) -> bool:
        """Return True if the queue is empty, False otherwise."""
        return self._current_size == 0

    def size(self) -> int:
        """Return number of elements currently in the queue."""
        return self._current_size

    def print_underlying_sa(self) -> None:
        """Print underlying StaticArray. Used for testing purposes."""
        print(self._sa)

    def _increment(self, index: int) -> int:
        """Move index to next position."""

        # employ wraparound if needed
        index += 1
        if index == self._sa.length():
            index = 0

        return index

    # ---------------------------------------------------------------------- #

    def enqueue(self, value: object) -> None:
        """
        Method that adds a given value to the end of the queue.
        """
        # If the queue size equals the length of underlying static array
        # call the double_queue method to double the underlying array length
        if self._current_size == self._sa.length():
            self._double_queue()

        # Call the increment method on self._back to increment its index
        self._back = self._increment(self._back)

        # Place the given value in the newly incremented index in self._sa
        self._sa[self._back] = value

        # Increment current size of the queue
        self._current_size += 1


    def dequeue(self) -> object:
        """
        Method that removes and returns the value at the beginning of
        the queue.
        """
        # Raises exception if the queue is already empty
        if self._current_size == 0:
            raise QueueException

        # Initialize a variable with the value of the self._front index
        # of the underlying static array. This var will be returned
        value_returned = self._sa[self._front]

        # Increment self._front index by calling increment method
        self._front = self._increment(self._front)

        # Increment current size of queue
        self._current_size -= 1

        return value_returned

    def front(self) -> object:
        """
        Method that returns the value at the front of the queue.
        """
        # Raises exception if queue is empty
        if self._current_size == 0:
            raise QueueException

        # Initialize a variable with the value of the self._front index
        front_returned = self._sa[self._front]

        # Return front value variable
        return front_returned

    # The method below is optional, but recommended, to implement. #
    # You may alter it in any way you see fit.                     #

    def _double_queue(self) -> None:
        """
        Method that doubles the size of the queue's underlying static array
        """
        new_stat_arr = StaticArray(self._sa.length()*2)
        start_index = self._front
        for i in range(self._current_size):
            new_stat_arr[i] = self._sa[start_index]
            start_index = self._increment(start_index)
        self._sa = new_stat_arr
        self._front = 0
        self._back = self._current_size-1



# ------------------- BASIC TESTING -----------------------------------------

if __name__ == "__main__":

    print("\n# Basic functionality tests #")
    print("\n# enqueue()")
    q = Queue()
    print(q)
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)

    print("\n# dequeue()")
    q = Queue()
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)
    for _ in range(q.size() + 1):
        try:
            print(q.dequeue())
        except Exception as e:
            print("No elements in queue", type(e))
    for value in [6, 7, 8, 111, 222, 3333, 4444]:
        q.enqueue(value)
    print(q)
    q.print_underlying_sa()

    print("\n# front()")
    q = Queue()
    print(q)
    for value in ['A', 'B', 'C', 'D']:
        try:
            print(q.front())
        except Exception as e:
            print("No elements in queue", type(e))
        q.enqueue(value)
    print(q)

    print("\n# Circular buffer tests: #\n")

    def action_and_print(
            header: str, action: callable, values: [], queue: Queue) -> None:
        """
        Print header, perform action,
        then print queue and its underlying storage.
        """
        print(header)
        if values:
            for value in values:
                action(value)
        else:
            action()
        print(queue)
        queue.print_underlying_sa()
        print()

    q = Queue()

    # action_and_print("# Enqueue: 2, 4, 6, 8", q.enqueue, [2, 4, 6, 8], q)

    # Calling the action_and_print() function declared two lines above,
    # would be equivalent to following lines of code:
    print("# Enqueue: 2, 4, 6, 8")
    test_case = [2, 4, 6, 8]
    for value in test_case:
        q.enqueue(value)
    print(q)
    q.print_underlying_sa()
    print()

    action_and_print("# Dequeue a value", q.dequeue, [], q)
    action_and_print("# Enqueue: 10", q.enqueue, [10], q)
    action_and_print("# Enqueue: 12", q.enqueue, [12], q)

    print("# Dequeue until empty")
    while not q.is_empty():
        q.dequeue()
    print(q)
    q.print_underlying_sa()
    print()

    action_and_print("# Enqueue: 14, 16, 18", q.enqueue, [14, 16, 18], q)
    action_and_print("# Enqueue: 20", q.enqueue, [20], q)
    action_and_print("# Enqueue: 22, 24, 26, 28", q.enqueue,
                     [22, 24, 26, 28], q)
    action_and_print("# Enqueue: 30", q.enqueue, [30], q)
