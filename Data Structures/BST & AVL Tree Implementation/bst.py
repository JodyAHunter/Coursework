# Name: Jody Hunter
# OSU Email: huntejod@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 4: BST/AVL Tree Implementation
# Due Date: 05/22/2023
# Description: Implementation of the Binary Search Tree data structure


import random
from queue_and_stack import Queue, Stack


class BSTNode:
    """
    Binary Search Tree Node class
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """

    def __init__(self, value: object) -> None:
        """
        Initialize a new BST node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.value = value   # to store node's data
        self.left = None     # pointer to root of left subtree
        self.right = None    # pointer to root of right subtree

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'BST Node: {}'.format(self.value)


class BST:
    """
    Binary Search Tree class
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize new Binary Search Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._root = None

        # populate BST with initial values (if provided)
        # before using this feature, implement add() method
        if start_tree is not None:
            for value in start_tree:
                self.add(value)

    def __str__(self) -> str:
        """
        Override string method; display in pre-order
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        self._str_helper(self._root, values)
        return "BST pre-order { " + ", ".join(values) + " }"

    def _str_helper(self, node: BSTNode, values: []) -> None:
        """
        Helper method for __str__. Does pre-order tree traversal
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if not node:
            return
        values.append(str(node.value))
        self._str_helper(node.left, values)
        self._str_helper(node.right, values)

    def get_root(self) -> BSTNode:
        """
        Return root of tree, or None if empty
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._root

    def is_valid_bst(self) -> bool:
        """
        Perform pre-order traversal of the tree.
        Return False if nodes don't adhere to the bst ordering property.

        This is intended to be a troubleshooting method to help find any
        inconsistencies in the tree after the add() or remove() operations.
        A return of True from this method doesn't guarantee that your tree
        is the 'correct' result, just that it satisfies bst ordering.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                if node.left and node.left.value >= node.value:
                    return False
                if node.right and node.right.value < node.value:
                    return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        BST method that adds a new value to an existing tree.
        """
        # Create variables for parent node with value of None and current
        # node with the value of the root node
        parent_node = None
        current_node = self._root

        # Branch down the tree by comparing the current node's value to the
        # value to be added to the tree. Branch left if value being added is
        # lower than the current node's value, or right otherwise.
        # The while loop ends when an empty spot is reached
        # (current node is None)
        while current_node is not None:
            parent_node = current_node
            if value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right

        # Case for when the tree is empty. Added value becomes root
        if parent_node == None:
            self._root = BSTNode(value)

        # Add the new node by pointing the parent node to it depending on value
        elif value >= parent_node.value:
            parent_node.right = BSTNode(value)
        elif value < parent_node.value:
            parent_node.left = BSTNode(value)


    def remove(self, value: object) -> bool:
        """
        BST method that removes a node from the tree.
        """
        # Create variables for parent node with value of None and current node
        # with value of root
        parent_node = None
        current_node = self._root

        # Branch down tree until current node is None or the value is found
        while current_node is not None and current_node.value != value:
            parent_node = current_node
            if value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right

        # Case for if the value to be removed is not found, return False
        if current_node is None:
            return False

        # Case for if the node to be removed has no children
        if current_node.right is None and current_node.left is None:
            self._remove_no_subtrees(parent_node, current_node)

        # Case for if the node to be removed has only one child
        elif current_node.right is None or current_node.left is None:
            self._remove_one_subtree(parent_node, current_node)

        # Case for if the node to be removed has two children
        elif current_node.right is not None and current_node.left is not None:
            self._remove_two_subtrees(parent_node, current_node)

        # return True if value was found and removed from tree
        return True


    def _remove_no_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Helper method that is called when removing a node that has no children.
        """
        # remove node that has no subtrees (no left or right nodes)

        # Case where node to be removed is root
        if remove_node == self._root:
            self._root = None
            return

        # If removed node is left child of parent node, parent node left pointer
        # becomes None, or vice-versa for if the removed node is the right child
        if remove_parent.left == remove_node:
            remove_parent.left = None
        elif remove_parent.right == remove_node:
            remove_parent.right = None

    def _remove_one_subtree(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Helper method that is called when removing a node that has one child.
        """
        # remove node that has a left or right subtree (only)

        # If the node to be removed is the right child of the parent node
        if remove_node.right is not None:
            remove_node_child = remove_node.right

        # If the node to be removed is the left child of the parent node
        else:
            remove_node_child = remove_node.left

        # Case if node to be removed is root
        if remove_node == self._root:
            self._root = remove_node_child
            return

        # Sets child of removed node to become the child of the parent node
        if remove_node == remove_parent.left:
            remove_parent.left = remove_node_child
        else:
            remove_parent.right = remove_node_child


    def _remove_two_subtrees(self, remove_parent: BSTNode, remove_node: BSTNode) -> None:
        """
        Helper method that is called when removing a node that has two children.
        """
        # remove node that has two subtrees
        # need to find inorder successor and its parent (make a method!)

        # Find the successor and its parent by using a while loop
        successor = remove_node.right
        successor_parent = remove_node
        while successor.left != None:
            successor_parent = successor
            successor = successor.left

        # Make successor's left pointer equal to the removed node's left pointer
        successor.left = remove_node.left

        # If successor node is also the right child of the removed node,
        # Make the successor's parent's left child the right child of successor
        if successor != remove_node.right:
            successor_parent.left = successor.right
            # Make successor's right child equal to removed node's right child
            successor.right = remove_node.right

        # Case for if the node to be removed is root. Make successor new root
        if remove_parent is None:
            self._root = successor

        # Removed node not root, make successor the new child of the removed
        # node's parent
        else:
            if remove_node == remove_parent.left:
                remove_parent.left = successor
            elif remove_node == remove_parent.right:
                remove_parent.right = successor

    def contains(self, value: object) -> bool:
        """
        Method that takes a given value and returns True if the value exists
        in the tree. Otherwise, it returns False.
        """
        # Create variables for parent node with value of None and current node
        # with value of root
        parent_node = None
        current_node = self._root

        # Branch down through tree until value is found or current node is None
        while current_node is not None and current_node.value != value:
            parent_node = current_node
            if value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right

        # If current node reaches None, value was not found. Return False
        if current_node is None:
            return False

        # Value was found
        else:
            return True

    def inorder_traversal(self) -> Queue:
        """
        Method that performs an inorder traversal and returns a Queue
        that contains the values found in the tree.
        """
        # Create a queue object
        values = Queue()

        # Create a current node variable with value of root
        current_node = self._root

        # Call helper method with current node and created queue as arguments
        self.inorder_traversal_helper(current_node, values)

        # Return the queue object
        return values

    def inorder_traversal_helper(self, current_node, values):
        """
        Helper method that is called from the inorder_traversal method.
        """
        # Use an if statement that checks if current node is None and
        # recursively calls the help method to traverse the tree and enqueue
        # each visited node's value to the values Queue
        if current_node is not None:
            self.inorder_traversal_helper(current_node.left, values)
            values.enqueue(current_node.value)
            self.inorder_traversal_helper(current_node.right, values)

    def find_min(self) -> object:
        """
        Method that finds the minimum value of all of the nodes in the tree.
        """
        # Case for if the tree is empty. Returns None
        if self._root is None:
            return self._root

        # Create a current node variable with the value of root
        current_node = self._root

        # While loop until current node's left child is None
        # Branch down the tree as far left as possible
        while current_node.left is not None:
            current_node = current_node.left

        # Return the value of current node
        return current_node.value

    def find_max(self) -> object:
        """
        Method that finds the maximum values of all of the nodes in the tree.
        """
        # Case for if the tree is empty. Returns None
        if self._root is None:
            return self._root

        # Create a current node variable with the value of root
        current_node = self._root

        # While loop until current node's right child is None
        # Branch down the tree as far right as possible
        while current_node.right is not None:
            current_node = current_node.right

        # Return the value of current node
        return current_node.value

    def is_empty(self) -> bool:
        """
        Method that returns True if a tree is empty, or False if it is not.
        """
        # Checks if the root node is None
        if self._root is None:
            # Returns True if root is None (Tree is empty)
            return True
        else:
            return False

    def make_empty(self) -> None:
        """
        Method that makes a tree become empty by changing the root to None.
        """
        self._root = None


# ------------------- BASIC TESTING -----------------------------------------

if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),
        (3, 2, 1),
        (1, 3, 2),
        (3, 1, 2),
    )
    for case in test_cases:
        tree = BST(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),
        (10, 20, 30, 50, 40),
        (30, 20, 10, 5, 1),
        (30, 20, 10, 1, 5),
        (5, 4, 6, 3, 7, 2, 8),
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = BST(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = BST()
        for value in case:
            tree.add(value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),
        ((1, 2, 3), 2),
        ((1, 2, 3), 3),
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),
    )
    for case, del_value in test_cases:
        tree = BST(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = BST(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = BST(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        if not tree.is_valid_bst():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
        print('RESULT :', tree)

    print("\nPDF - method remove() example 5")
    print("----------------------------")
    case = (67, 3, -29, 71, 10, -15, -13, 22, -71, -70)
    del_value1 = 67
    del_value2 = -29
    del_value3 = 10
    del_value4 = -13
    del_value5 = -71
    tree = BST(case)
    print('INPUT  :', tree, "DEL:", del_value1, del_value2, del_value3, del_value4, del_value5)
    tree.remove(del_value1)
    print('RESULT :', tree)
    tree.remove(del_value2)
    print('RESULT :', tree)
    tree.remove(del_value3)
    print('RESULT :', tree)
    tree.remove(del_value4)
    print('RESULT :', tree)
    tree.remove(del_value5)
    print('RESULT :', tree)


    print("\nPDF - method remove() example 6")
    print("----------------------------")
    case = (-6, -29, -27, -79, 82, -12, 90, -4, 63, 95)
    del_value = -6
    tree = BST(case)
    print('INPUT  :', tree, "DEL:", del_value)
    tree.remove(del_value)
    print('RESULT :', tree)

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = BST([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = BST()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = BST([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = BST([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = BST()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
