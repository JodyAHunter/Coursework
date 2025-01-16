# Name: Jody Hunter
# OSU Email: huntejod@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 4: BST/AVL Tree Implementation
# Due Date: 05/22/2023
# Description: Implementation of the AVL Tree data structure


import random
from queue_and_stack import Queue, Stack
from bst import BSTNode, BST


class AVLNode(BSTNode):
    """
    AVL Tree Node class. Inherits from BSTNode
    DO NOT CHANGE THIS CLASS IN ANY WAY
    """
    def __init__(self, value: object) -> None:
        """
        Initialize a new AVL node
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(value)

        # new variables needed for AVL
        self.parent = None
        self.height = 0

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return 'AVL Node: {}'.format(self.value)


class AVL(BST):
    """
    AVL Tree class. Inherits from BST
    """

    def __init__(self, start_tree=None) -> None:
        """
        Initialize a new AVL Tree
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        # call __init__() from parent class
        super().__init__(start_tree)

    def __str__(self) -> str:
        """
        Override string method
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        values = []
        super()._str_helper(self._root, values)
        return "AVL pre-order { " + ", ".join(values) + " }"

    def is_valid_avl(self) -> bool:
        """
        Perform pre-order traversal of the tree. Return False if there
        are any problems with attributes of any of the nodes in the tree.

        This is intended to be a troubleshooting 'helper' method to help
        find any inconsistencies in the tree after the add() or remove()
        operations. Review the code to understand what this method is
        checking and how it determines whether the AVL tree is correct.

        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        stack = Stack()
        stack.push(self._root)
        while not stack.is_empty():
            node = stack.pop()
            if node:
                # check for correct height (relative to children)
                left = node.left.height if node.left else -1
                right = node.right.height if node.right else -1
                if node.height != 1 + max(left, right):
                    return False

                if node.parent:
                    # parent and child pointers are in sync
                    if node.value < node.parent.value:
                        check_node = node.parent.left
                    else:
                        check_node = node.parent.right
                    if check_node != node:
                        return False
                else:
                    # NULL parent is only allowed on the root of the tree
                    if node != self._root:
                        return False
                stack.push(node.right)
                stack.push(node.left)
        return True

    # ------------------------------------------------------------------ #

    def add(self, value: object) -> None:
        """
        Method that adds a node to an AVL tree.
        """
        # Create a new node with the given value
        new_node = AVLNode(value)

        # Create variables for current node and parent node
        parent_node = None
        current_node = self._root

        # Branch down the tree using a while loop until current node is None,
        # comparing the added value to the current node as we progress down
        # the tree
        while current_node is not None:
            parent_node = current_node
            if value < current_node.value:
                current_node = current_node.left
            elif value > current_node.value:
                current_node = current_node.right
            # If the value is equivalent to the current node, return
            # No duplicates allowed
            else:
                return

        # Case if the tree is empty, make the added node become root
        if parent_node is None:
            self._root = new_node

        # Once current node is None

        # If added value is > parent node value, make new node the right child
        elif value > parent_node.value:
            parent_node.right = new_node

        # If added value is < parent node value, make new node the left child
        elif value < parent_node.value:
            parent_node.left = new_node

        # If added value is equivalent to parent node value, return
        # No duplicates allowed
        elif value == parent_node.value:
            return

        # Make the newly added node's parent the parent node
        new_node.parent = parent_node

        # Starting at the parent node, branch back upwards to root
        # Rebalance the node at each iteration
        while parent_node is not None:
            self._rebalance(parent_node)
            parent_node = parent_node.parent

    def remove(self, value: object) -> bool:
        """
        Method that removes a node from an AVL tree.
        """
        # Create variables for current node and parent node
        parent_node = None
        current_node = self._root

        # Branch down the tree using a while loop until current node is None
        # or the value to be removed is found
        while current_node is not None and current_node.value != value:
            parent_node = current_node
            if value < current_node.value:
                current_node = current_node.left
            else:
                current_node = current_node.right

        # If current node is None, value to be removed does not exist
        if current_node is None:
            return False

        # If node to be removed has no children, call the remove_no_subtrees
        # helper function
        if current_node.right is None and current_node.left is None:
            self._remove_no_subtrees(parent_node, current_node)

        # If node to be removed has only one child, call the remove_one_subtree
        # helper function
        elif current_node.right is None or current_node.left is None:
            self._remove_one_subtree(parent_node, current_node)

            # If removed node is not root, parent node will not be None,
            # Make parent node the parent of the removed node's child
            if parent_node is not None:
                if parent_node.right is not None:
                    parent_node.right.parent = parent_node
                else:
                    parent_node.left.parent = parent_node

        # If node to be removed has two children, call the remove_two_subtrees
        # helper function
        elif current_node.right is not None and current_node.left is not None:
            parent_node = self._remove_two_subtrees(parent_node, current_node)

        # Starting with the parent node (lowest modified node after removal)
        # branch back up the tree, re-balancing each node on the way, until
        # parent node is None
        while parent_node is not None:
            self._rebalance(parent_node)
            parent_node = parent_node.parent

        # Return True if value was successfully removed from the tree
        return True

    # Experiment and see if you can use the optional                         #
    # subtree removal methods defined in the BST here in the AVL.            #
    # Call normally using self -> self._remove_no_subtrees(parent, node)     #
    # You need to override the _remove_two_subtrees() method in any case.    #
    # Remove these comments.                                                 #
    # Remove these method stubs if you decide not to use them.               #
    # Change this method in any way you'd like.                              #

    def _remove_two_subtrees(self, remove_parent: AVLNode, remove_node: AVLNode) -> AVLNode:
        """
        Helper method for removing a node with two subtrees from an AVL tree.
        """
        # Find the successor and its parent by using a while loop
        successor = remove_node.right
        successor_parent = remove_node
        while successor.left is not None:
            successor_parent = successor
            successor = successor.left

        # Case for when the node to be removed is the tree's root
        if remove_node == self._root:
            successor.left = remove_node.left
            remove_node.left.parent = successor

            # Case for when successor node is not the right child of node
            # to be removed from tree. Successor parent will be returned
            if successor != remove_node.right:
                successor_parent.left = successor.right
                if successor_parent.left is not None:
                    successor_parent.left.parent = successor_parent
                self._root = successor
                successor.right = remove_node.right
                successor.right.parent = successor
                successor.parent = None
                return successor_parent

            # Case for when successor node is the right child of the node
            # to be removed from the tree. Successor will be returned
            else:
                self._root = successor
                successor.right = remove_node.right.right
                if successor.right is not None:
                    successor.right.parent = successor
                successor.parent = None
                return successor

        # Case for when the node to be removed is not the tree's root
        else:
            successor.left = remove_node.left
            remove_node.left.parent = successor

            # Case for when successor node is not the right child of node
            # to be removed from tree.
            if successor != remove_node.right:
                successor_parent.left = successor.right
                if successor_parent.left is not None:
                    successor_parent.left.parent = successor_parent
                successor.right = remove_node.right
                successor.right.parent = successor

            # Reassign relationship between removed node's parent and successor
            if remove_node == remove_parent.left:
                remove_parent.left = successor
                successor.parent = remove_parent
            elif remove_node == remove_parent.right:
                remove_parent.right = successor
                successor.parent = remove_parent

            # If the removed node is the successor parent, return successor
            if remove_node == successor_parent:
                return successor
            # Otherwise return the successor parent
            else:
                return successor_parent

    # It's highly recommended to implement                          #
    # the following methods for balancing the AVL Tree.             #
    # Remove these comments.                                        #
    # Remove these method stubs if you decide not to use them.      #
    # Change these methods in any way you'd like.                   #

    def _balance_factor(self, node: AVLNode) -> int:
        """
        Method that returns the balance factor of a given node
        """
        # Get the height of the left child
        left_height = self._get_height(node.left)

        # Get the height of the right child
        right_height = self._get_height(node.right)

        # Calculate the balance factor and return the result
        b_factor = right_height-left_height
        return b_factor

    def _get_height(self, node: AVLNode) -> int:
        """
        Method that returns the height of a node
        """
        # If node does not exist returns height of -1
        if node is None:
            return -1

        # Return height value of given node
        return node.height

    def _rotate_left(self, node: AVLNode) -> AVLNode:
        """
        Method that perform a left rotation of a given node
        """
        # Create a variable for the right child of the given node
        child = node.right

        # Make the child's left child become the right child of the given node
        node.right = child.left

        # If node has a right child, make the parent of that child point to node
        if node.right is not None:
            node.right.parent = node

        # Make node the left child of child
        child.left = node

        # Make child the parent of node
        node.parent = child

        # Call the update height method for both node and child
        self._update_height(node)
        self._update_height(child)

        # Return the child node
        return child

    def _rotate_right(self, node: AVLNode) -> AVLNode:
        """
        Method that perform a right rotation of a given node
        """
        # Create a variable for the left child of the given node
        child = node.left

        # Make the child's right child become the left child of the given node
        node.left = child.right

        # If node has a left child, make the parent of that child point to node
        if node.left is not None:
            node.left.parent = node

        # Make node the right child of child
        child.right = node

        # Make child the parent of node
        node.parent = child

        # Call the update height method for both node and child
        self._update_height(node)
        self._update_height(child)

        # Return the child node
        return child

    def _update_height(self, node: AVLNode) -> None:
        """
        Method that updates the height value of a given node.
        """
        # Get the heights of the left and right child of a node
        left_height = self._get_height(node.left)
        right_height = self._get_height(node.right)

        # The node's height will be the highest of the two child heights + 1
        node.height = max(left_height, right_height) + 1

    def _rebalance(self, node: AVLNode) -> None:
        """
        Method that checks a given node and re-balances the tree as needed.
        """
        # Create a variable for the node's parent
        node_parent = node.parent

        # Left-Heavy, L-L Rotation
        if self._balance_factor(node) < -1:

            # Child is right-heavy, L-R Rotation
            if self._balance_factor(node.left) > 0:
                node.left = self._rotate_left(node.left)
                node.left.parent = node

            new_sub_root = self._rotate_right(node)
            new_sub_root.parent = node_parent

            # Case where the new sub-root after rotation is the new root
            if node_parent is None:
                self._root = new_sub_root

            # Case where new sub-root is left child of the parent node
            elif new_sub_root.value < node_parent.value:
                node_parent.left = new_sub_root

            # Case where new sub-root is the right child of the parent node
            else:
                node_parent.right = new_sub_root

        # Right-Heavy, R-R Rotation
        elif self._balance_factor(node) > 1:

            # Child is left-heavy, R-L Rotation
            if self._balance_factor(node.right) < 0:
                node.right = self._rotate_right(node.right)
                node.right.parent = node

            new_sub_root = self._rotate_left(node)
            new_sub_root.parent = node_parent

            # Case where the new sub-root after rotation is the new root
            if node_parent is None:
                self._root = new_sub_root

            # Case where new sub-root is left child of the parent node
            elif new_sub_root.value < node_parent.value:
                node_parent.left = new_sub_root

            # Case where new sub-root is the right child of the parent node
            else:
                node_parent.right = new_sub_root

        # If balance factor is within normal limits, update node's height
        else:
            self._update_height(node)


# ------------------- BASIC TESTING -----------------------------------------


if __name__ == '__main__':

    print("\nPDF - method add() example 1")
    print("----------------------------")
    test_cases = (
        (1, 2, 3),  # RR
        (3, 2, 1),  # LL
        (1, 3, 2),  # RL
        (3, 1, 2),  # LR
    )
    for case in test_cases:
        tree = AVL(case)
        print(tree)

    print("\nPDF - method add() example 2")
    print("----------------------------")
    test_cases = (
        (10, 20, 30, 40, 50),   # RR, RR
        (10, 20, 30, 50, 40),   # RR, RL
        (30, 20, 10, 5, 1),     # LL, LL
        (30, 20, 10, 1, 5),     # LL, LR
        (5, 4, 6, 3, 7, 2, 8),  # LL, RR
        (range(0, 30, 3)),
        (range(0, 31, 3)),
        (range(0, 34, 3)),
        (range(10, -10, -2)),
        ('A', 'B', 'C', 'D', 'E'),
        (1, 1, 1, 1),
    )
    for case in test_cases:
        tree = AVL(case)
        print('INPUT  :', case)
        print('RESULT :', tree)

    print("\nPDF - method add() example 3")
    print("----------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL()
        for value in case:
            tree.add(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH ADD OPERATION")
    print('add() stress test finished')

    print("\nPDF - method remove() example 1")
    print("-------------------------------")
    test_cases = (
        ((1, 2, 3), 1),  # no AVL rotation
        ((1, 2, 3), 2),  # no AVL rotation
        ((1, 2, 3), 3),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 0),
        ((50, 40, 60, 30, 70, 20, 80, 45), 45),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 40),  # no AVL rotation
        ((50, 40, 60, 30, 70, 20, 80, 45), 30),  # no AVL rotation
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.is_valid_avl()

    print("\nPDF - method remove() example 2")
    print("-------------------------------")
    test_cases = (
        ((50, 40, 60, 30, 70, 20, 80, 45), 20),  # RR
        ((50, 40, 60, 30, 70, 20, 80, 15), 40),  # LL
        ((50, 40, 60, 30, 70, 20, 80, 35), 20),  # RL
        ((50, 40, 60, 30, 70, 20, 80, 25), 40),  # LR
    )
    for case, del_value in test_cases:
        tree = AVL(case)
        print('INPUT  :', tree, "DEL:", del_value)
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.is_valid_avl()

    print("\nPDF - method remove() example 3")
    print("-------------------------------")
    case = range(-9, 16, 2)
    tree = AVL(case)
    for del_value in case:
        print('INPUT  :', tree, del_value)
        tree.remove(del_value)
        print('RESULT :', tree)
        tree.is_valid_avl()

    print("\nPDF - method remove() example 4")
    print("-------------------------------")
    case = range(0, 34, 3)
    tree = AVL(case)
    for _ in case[:-2]:
        root_value = tree.get_root().value
        print('INPUT  :', tree, root_value)
        tree.remove(root_value)
        print('RESULT :', tree)
        tree.is_valid_avl()

    print("\nPDF - method remove() example 5")
    print("-------------------------------")
    for _ in range(100):
        case = list(set(random.randrange(1, 20000) for _ in range(900)))
        tree = AVL(case)
        for value in case[::2]:
            tree.remove(value)
        if not tree.is_valid_avl():
            raise Exception("PROBLEM WITH REMOVE OPERATION")
    print('remove() stress test finished')

    print("\nPDF - method contains() example 1")
    print("---------------------------------")
    tree = AVL([10, 5, 15])
    print(tree.contains(15))
    print(tree.contains(-10))
    print(tree.contains(15))

    print("\nPDF - method contains() example 2")
    print("---------------------------------")
    tree = AVL()
    print(tree.contains(0))

    print("\nPDF - method inorder_traversal() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree.inorder_traversal())

    print("\nPDF - method inorder_traversal() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree.inorder_traversal())

    print("\nPDF - method find_min() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_min() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Minimum value is:", tree.find_min())

    print("\nPDF - method find_max() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method find_max() example 2")
    print("---------------------------------")
    tree = AVL([8, 10, -4, 5, -1])
    print(tree)
    print("Maximum value is:", tree.find_max())

    print("\nPDF - method is_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method is_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree is empty:", tree.is_empty())

    print("\nPDF - method make_empty() example 1")
    print("---------------------------------")
    tree = AVL([10, 20, 5, 15, 17, 7, 12])
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)

    print("\nPDF - method make_empty() example 2")
    print("---------------------------------")
    tree = AVL()
    print("Tree before make_empty():", tree)
    tree.make_empty()
    print("Tree after make_empty(): ", tree)
