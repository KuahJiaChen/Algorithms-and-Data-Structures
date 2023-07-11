# import random, math

outputdebug = False


def debug(msg):
    if outputdebug:
        print(msg)


class Node():
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class AVLTree():
    def __init__(self, *args):
        self.node = None
        self.height = -1
        self.balance = 0;

        if len(args) == 1:
            for i in args[0]:
                self.insert(i)

    def height(self):
        if self.node:
            return self.node.height
        else:
            return 0

    def is_leaf(self):
        return (self.height == 0)

    def insert(self, key):
        tree = self.node

        newnode = Node(key)

        if tree == None:
            self.node = newnode
            self.node.left = AVLTree()
            self.node.right = AVLTree()
            debug("Inserted key [" + str(key) + "]")

        elif key < tree.key:
            self.node.left.insert(key)

        elif key > tree.key:
            self.node.right.insert(key)

        else:
            debug("Key [" + str(key) + "] already in tree.")

        self.rebalance()

    def rebalance(self):
        '''
        Rebalance a particular (sub)tree
        '''
        # key inserted. Let's check if we're balanced
        self.update_heights(False)
        self.update_balances(False)
        while self.balance < -1 or self.balance > 1:
            if self.balance > 1:
                if self.node.left.balance < 0:
                    self.node.left.lrotate()  # we're in case II
                    self.update_heights()
                    self.update_balances()
                self.rrotate()
                self.update_heights()
                self.update_balances()

            if self.balance < -1:
                if self.node.right.balance > 0:
                    self.node.right.rrotate()  # we're in case III
                    self.update_heights()
                    self.update_balances()
                self.lrotate()
                self.update_heights()
                self.update_balances()

    def rrotate(self):
        # Rotate left pivoting on self
        debug('Rotating ' + str(self.node.key) + ' right')
        A = self.node
        B = self.node.left.node
        T = B.right.node

        self.node = B
        B.right.node = A
        A.left.node = T

    def lrotate(self):
        # Rotate left pivoting on self
        debug('Rotating ' + str(self.node.key) + ' left')
        A = self.node
        B = self.node.right.node
        T = B.left.node

        self.node = B
        B.left.node = A
        A.right.node = T

    def update_heights(self, recurse=True):
        if not self.node == None:
            if recurse:
                if self.node.left != None:
                    self.node.left.update_heights()
                if self.node.right != None:
                    self.node.right.update_heights()

            self.height = max(self.node.left.height,
                              self.node.right.height) + 1
        else:
            self.height = -1

    def update_balances(self, recurse=True):
        if not self.node == None:
            if recurse:
                if self.node.left != None:
                    self.node.left.update_balances()
                if self.node.right != None:
                    self.node.right.update_balances()

            self.balance = self.node.left.height - self.node.right.height
        else:
            self.balance = 0

    def delete(self, key):
        # debug("Trying to delete at node: " + str(self.node.key))
        if self.node != None:
            if self.node.key == key:
                debug("Deleting ... " + str(key))
                if self.node.left.node == None and self.node.right.node == None:
                    self.node = None  # leaves can be killed at will
                # if only one subtree, take that
                elif self.node.left.node == None:
                    self.node = self.node.right.node
                elif self.node.right.node == None:
                    self.node = self.node.left.node

                # worst-case: both children present. Find logical successor
                else:
                    replacement = self.logical_successor(self.node)
                    if replacement != None:  # sanity check
                        debug("Found replacement for " + str(key) + " -> " + str(replacement.key))
                        self.node.key = replacement.key

                        # replaced. Now delete the key from right child
                        self.node.right.delete(replacement.key)

                self.rebalance()
                return
            elif key < self.node.key:
                self.node.left.delete(key)
            elif key > self.node.key:
                self.node.right.delete(key)

            self.rebalance()
        else:
            return

    def logical_predecessor(self, node):
        '''
        Find the biggest valued node in LEFT child
        '''
        node = node.left.node
        if node != None:
            while node.right != None:
                if node.right.node == None:
                    return node
                else:
                    node = node.right.node
        return node

    def logical_successor(self, node):
        '''
        Find the smallese valued node in RIGHT child
        '''
        node = node.right.node
        if node != None:  # just a sanity check

            while node.left != None:
                debug("LS: traversing: " + str(node.key))
                if node.left.node == None:
                    return node
                else:
                    node = node.left.node
        return node

    def check_balanced(self):
        if self == None or self.node == None:
            return True

        # We always need to make sure we are balanced
        self.update_heights()
        self.update_balances()
        return ((abs(self.balance) < 2) and self.node.left.check_balanced() and self.node.right.check_balanced())

    def inorder_traverse(self):
        if self.node == None:
            return []

        inlist = []
        l = self.node.left.inorder_traverse()
        for i in l:
            inlist.append(i)

        inlist.append(self.node.key)

        l = self.node.right.inorder_traverse()
        for i in l:
            inlist.append(i)

        return inlist

    def display(self, level=0, pref=''):
        '''
        Display the whole tree. Uses recursive def.
        TODO: create a better display using breadth-first search
        '''
        self.update_heights()  # Must update heights before balances
        self.update_balances()
        if (self.node != None):
            print('-' * level * 2, pref, self.node.key, "[" + str(self.height) + ":" + str(self.balance) + "]",
                  'L' if self.is_leaf() else ' ')
            if self.node.left != None:
                self.node.left.display(level + 1, '<')
            if self.node.left != None:
                self.node.right.display(level + 1, '>')

    def uncorrupted_merge(self, other, corrupted):
        """
        Purpose: let all the elements in other that is not in the corrupted list to appears in self, hence eventually
                 self would contains all the elements that it originally contains and also the elements in other that is
                 not corrupted
        Argument: self is an instance of AVLTree, other is an instance of AVLTree, corrupted is a list of keys
        Return: return an instance of AVLTree and it would contains all the elements originally it contains and also the
                elements in other that not in the corrupted list
        Complexity:
            - time complexity: O(k log N), where k is the number of keys in corrupted and N is the number of nodes in
                               the larger of two AVL trees
            - auxiliary space complexity: O(1)
        Assumption: The comparison cost always be O(1) (same as for Nathan's approach)
        """
        # delete corrupted items
        for i in range(len(corrupted)):
            other.delete(corrupted[i])

        minimum = None
        maximum = None

        # find minimum in self
        left_most_tree = self
        if left_most_tree.node is not None:
            while left_most_tree.node.left.node is not None:
                left_most_tree = left_most_tree.node.left
            minimum = left_most_tree.node.key

            self.delete(minimum)
            # if self only have one element, no need to delete, hence insert back, make sure self would not be empty
            if self.node is None:
                self.insert(minimum)

        # find maximum in other
        right_most_tree = other
        if right_most_tree.node is not None:
            while right_most_tree.node.right.node is not None:
                right_most_tree = right_most_tree.node.right
            maximum = right_most_tree.node.key

            other.delete(maximum)

        # find the left most node in self
        left_most_tree = self
        if left_most_tree.node is not None:
            while left_most_tree.node.left.node is not None:
                left_most_tree = left_most_tree.node.left

        if self.node is None:  # if self is empty
            self.node = other.node
        else:
            left_most_tree.node.left = other

        if minimum is not None:
            # left sub tree of left node of root is balanced
            self.insert(minimum)
        if maximum is not None:
            # right sub tree of right node of root is balanced
            self.insert(maximum)

        # In some extreme cases, the tree might still not be balanced, hence we need to reinsert predecessor
        # and successor

        # find predecessor
        if self.node is not None:
            current_tree = self.node.left
            while current_tree.node.right.node is not None:
                current_tree = current_tree.node.right
            predecessor = current_tree.node.key
            self.delete(predecessor)
            self.insert(predecessor)

        # find successor
        if self.node is not None:
            current_tree = self.node.right
            while current_tree.node.left.node is not None:
                current_tree = current_tree.node.left
            successor = current_tree.node.key
            self.delete(successor)
            self.insert(successor)


# Usage example
if __name__ == "__main__":
    """
    a = AVLTree()
    print("----- Inserting -------")
    # inlist = [5, 2, 12, -4, 3, 21, 19, 25]
    inlist = [7, 5, 2, 6, 3, 4, 1, 8, 9, 0]
    for i in inlist:
        a.insert(i)

    a.display()

    print("----- Deleting -------")
    a.delete(3)
    a.delete(4)
    # a.delete(5)
    a.display()

    print()
    print("Input            :", inlist)
    print("deleting ...       ", 3)
    print("deleting ...       ", 4)
    print("Inorder traversal:", a.inorder_traverse())

    t1 = AVLTree()
    t1.insert(1)
    t1.insert(2)
    t1.insert(3)
    t1.insert(4)
    t1.insert(5)

    t2 = AVLTree()
    t2.insert(6)
    t2.insert(7)
    t2.insert(8)
    t2.insert(9)
    t2.insert(10)

    corrupted = [1, 3, 5]
    t2.uncorrupted_merge(t1, corrupted)
    print("t2 display")
    t2.display()

    t3 = AVLTree()
    t3.insert(1)
    t3.insert(2)
    t3.insert(3)
    t3.insert(4)
    t3.insert(5)

    t4 = AVLTree()
    t4.insert(6)
    t4.insert(7)
    t4.insert(8)
    t4.insert(9)
    t4.insert(10)

    corrupted = [1, 3, 5]
    t4.uncorrupted_merge(t3, corrupted)
    print("t4 display")
    t4.display()

    t5 = AVLTree()
    for i in range(15551):
        t5.insert(i)

    t6 = AVLTree()
    for i in range(15551,30001):
        t6.insert(i)
    corrupted = []
    t6.uncorrupted_merge(t5, corrupted)
    print("t6 display")
    print(t6.check_balanced())
    """
