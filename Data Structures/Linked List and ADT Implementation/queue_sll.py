# Name: Jody Hunter
# OSU Email: huntejod@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 3: Linked List and ADT Implementation
# Due Date: 05/08/2023
# Description: Implementation of Queue ADT with underlying singly linked list


from SLNode import SLNode


class QueueException(Exception):
    """
    Custom exception to be used by Queue class
    DO NOT CHANGE THIS METHOD IN ANY WAY
    """
    pass


class Queue:
    def __init__(self):
        """
        Initialize new queue with head and tail nodes
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._head = None
        self._tail = None

    def __str__(self):
        """
        Return content of queue in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = 'QUEUE ['
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
        Return True is the queue is empty, False otherwise
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._head is None

    def size(self) -> int:
        """
        Return number of elements currently in the queue
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        node = self._head
        length = 0
        while node:
            length += 1
            node = node.next
        return length

    # -----------------------------------------------------------------------

    def enqueue(self, value: object) -> None:
        """
        Method that adds a given value to the end of the queue.
        """
        # Create a new node with the given value
        new_node = SLNode(value)

        # If the queue is empty, set both the head and tail to the new node
        if self.is_empty() == True:
            self._head = new_node
            self._tail = new_node

        else:
            # Make the tail point to the new node
            self._tail.next = new_node

            # Make the newly created node the new tail of the queue
            self._tail = new_node


    def dequeue(self) -> object:
        """
        Method that removes and returns the value at the beginning of
        the queue.
        """
        # Raises exception if queue is empty
        if self.is_empty() == True:
            raise QueueException

        # Initialize a variable to the value of the head node
        dequeued_value = self._head.value

        # Make the node following the head become the new node of the queue
        self._head = self._head.next

        # Return the original head node's value
        return dequeued_value

    def front(self) -> object:
        """
        Method that returns the value at the front of the queue.
        """
        # Raises exception if the queue is empty
        if self.is_empty() == True:
            raise QueueException

        # Return the value of the head of the queue
        return self._head.value


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == "__main__":

    print("\n# enqueue example 1")
    q = Queue()
    print(q)
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)

    print("\n# dequeue example 1")
    q = Queue()
    for value in [1, 2, 3, 4, 5]:
        q.enqueue(value)
    print(q)
    for i in range(6):
        try:
            print(q.dequeue())
        except Exception as e:
            print("No elements in queue", type(e))

    print('\n#front example 1')
    q = Queue()
    print(q)
    for value in ['A', 'B', 'C', 'D']:
        try:
            print(q.front())
        except Exception as e:
            print("No elements in queue", type(e))
        q.enqueue(value)
    print(q)
