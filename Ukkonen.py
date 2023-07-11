########################
#####  Question 1  #####
########################

import sys


class Node:

    def __init__(self, start=None, actual_end=None, global_end=None, is_leaf=False,
                 suffix_id=None, suffix_link=None, is_root=False):
        """
        Description: initialise the attributes of an instance of Node
        Written by: Kuah Jia Chen
        Input: start is an integer, actual_end is an integer, global_end is an End instance, is_leaf is a boolean,
               suffix_id is an integer, suffix_link is a Node instance, is_root is a boolean
        Return: None
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.start = start
        self.actual_end = actual_end
        self.global_end = global_end
        self.is_leaf = is_leaf
        self.suffix_id = suffix_id
        self.suffix_link = suffix_link
        self.edges = [None] * 91
        self.is_root = is_root

    def get_end_value(self):
        """
        Description: get the end value for the current Node instance
        Written by: Kuah Jia Chen
        Input: None
        Return: the end value for the current Node instance
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        if self.is_leaf:
            return self.global_end.global_end_value
        else:
            return self.actual_end

    def update_suffix_link(self, node):
        """
        Description: update the suffix_link attribute for the current Node instance
        Written by: Kuah Jia Chen
        Input: a Node instance
        Return: Node
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.suffix_link = node

    def get_suffix_link(self):
        """
        Description: get the suffix_link attribute for the current Node instance
        Written by: Kuah Jia Chen
        Input: None
        Return: the suffix_link attribute
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        return self.suffix_link


class End:

    def __init__(self):
        """
        Description: initialise the attributes of an instance of End
        Written by: Kuah Jia Chen
        Input: None
        Return: None
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.global_end_value = -1

    def update_end_value(self):
        """
        Description: update the end value for the End instance
        Written by: Kuah Jia Chen
        Input: None
        Return: None
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.global_end_value += 1


class SuffixTree:

    def __init__(self, input_string):
        """
        Description: initialise the attributes of an instance of SuffixTree
        Written by: Kuah Jia Chen
        Input: the input_string is a string
        Return: None
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(N), where N is the length of the input_string
            Aux: O(1)
        """
        self.input_string = input_string + "$"
        self.root = Node(is_root=True)
        self.root.suffix_link = self.root
        self.active_node = self.root
        self.active_edge = None
        self.active_length = 0
        self.previous_node = None
        self.ukkonen()

    def skip_count(self, current_i):
        """
        Description: call the skip_count_sux function to perform the traversal using skip count trick
        Written by: Kuah Jia Chen
        Input: the current_i is an integer
        Return: a Node instance
        Time complexity (Worst case) : O(N), where N is the length of self.input_string
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        return self.skip_count_aux(self.active_node, self.active_length, current_i)

    def skip_count_aux(self, current_node, current_active_length, current_end):
        """
        Description: perform the traversal of skip count trick and update the active node and active length
        Written by: Kuah Jia Chen
        Input: current_node is a Node instance, current_active_length is an integer, current_end is an integer
        Return: current_node is a Node instance
        Time complexity (Worst case) : O(N), where N is the length of self.input_string
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """

        # while not yet reached the last node discovered when active_length is not equal to 0
        while current_active_length != 0:

            # obtain the active edge based on the index for [current_end - current_active_length]th character
            # which represents the first character of the remaining in the edges of the current_node
            current_char = self.input_string[current_end - current_active_length]
            current_index = ord(current_char) - 36  # Index corresponding to first character of remaining
            current_edge = current_node.edges[current_index]

            # if active_length is equal to 0, return current_node
            if current_active_length == 0:
                self.active_length = current_active_length
                return current_node

            #  if active_length is not equal to 0
            else:

                #  if there is no such edge at that index, return current_node
                if current_edge is None:
                    break

                # else obtain the current edge length and new active length
                current_edge_length = current_edge.get_end_value() - current_edge.start + 1
                new_active_length = current_active_length - (current_edge.get_end_value() - current_edge.start + 1)

                # if current edge length is greater than the current_active_length, return current_node
                if current_edge_length > current_active_length:
                    break

                # else update the current_node and current_active_length
                else:
                    current_node = current_edge
                    current_active_length = new_active_length

        # update the active_length and return the current_node
        self.active_length = current_active_length
        return current_node

    def branch(self, current_index, active_edge, current_i, global_end, current_j):
        """
        Description: perform the action of creating the branch node, update the original edge as the new edge of the
                     branch node and create the new edge that causes tha branch and insert it to the branch node
        Written by: Kuah Jia Chen
        Input: current_index is an integer, active_edge is a Node instance, current_i is an integer, global_end is an
               End instance and current_j is an integer
        Return: branch_node is a Node instance
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """

        # get the current_edge using the current_index
        current_edge = active_edge[current_index]
        # calculate the start and end for the branch node
        branch_node_start = current_edge.start
        branch_node_end = current_edge.start + self.active_length - 1
        # create the branch node
        branch_node = Node(branch_node_start, actual_end=branch_node_end, is_leaf=False)
        # replace the original node of teh active node with this branch node
        self.active_node.edges[current_index] = branch_node

        # calculate the start for the new edge and keep the end value the same
        current_edge.start = current_edge.start + self.active_length
        new_char = self.input_string[current_edge.start]
        new_index = ord(new_char) - 36
        # update the original edge as the new edge for the branch node
        branch_node.edges[new_index] = current_edge

        # calculate the start and end of the new edge that causes the branch
        new_edge_start_index = current_i
        new_edge_end_index = global_end
        is_leaf = True
        suffix_id = current_j
        # create the new edge that causes teh branch
        new_node = Node(start=new_edge_start_index, global_end=new_edge_end_index, is_leaf=is_leaf,
                        suffix_id=suffix_id)
        new_node_char = self.input_string[current_i]
        new_node_index = ord(new_node_char) - 36
        # insert the new edge as the edge of the branch node
        branch_node.edges[new_node_index] = new_node

        # update the suffix link for the branch node and return the branch_node
        branch_node.update_suffix_link(self.root)
        return branch_node

    def create_new_edge(self, current_node, current_i, global_end, current_j, current_index):
        """
        Description: create a new edge for the current_node
        Written by: Kuah Jia Chen
        Input: current_node is a Node instance, current_i is an integer, global_end is an End instance, current_j
               is an integer and current_index is an integer
        Return: None
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """

        # calculate the start and end for the new edge
        start_index = current_i - self.active_length
        end_index = global_end
        is_leaf = True
        suffix_id = current_j
        # create the new edge and add it as the edge of the current_node
        new_node = Node(start=start_index, global_end=end_index, is_leaf=is_leaf, suffix_id=suffix_id)
        current_node.edges[current_index] = new_node

        return None

    def ukkonen(self):
        """
        Description: construct the suffix tree for the self.input_string using ukkonen algorithm
        Written by: Kuah Jia Chen
        Input: None
        Return: None
        Time complexity (Worst case) : O(N), where N is the length of self.input_string
        Space complexity:
            Input: O(1)
            Aux: O(N), where N is the length of the self.input_string
        """

        # initialize the i and j pointer where represents the phase and extension respectively
        i, j = 0, 0

        # create the End instance
        global_end = End()

        # for each phase
        while i < len(self.input_string):

            # increment the value of global end
            global_end.update_end_value()

            # reset the previous_node to None for every phase
            self.previous_node = None

            while j <= i:

                # perform the skip count trick and get the current active node
                self.active_node = self.skip_count(i)

                # the get current active edge for the first character of the active length at active edge
                current_char = self.input_string[i - self.active_length]
                current_index = ord(current_char) - 36
                active_edge = self.active_node.edges

                # check if a new edge should be created
                create_edge = active_edge[current_index] is None

                # check if a new branch should be created
                create_branch = self.input_string[i] != self.input_string[active_edge[current_index].start \
                                                                          + self.active_length] if active_edge[
                                                                                                       current_index] is not None else False

                # Rule 3: Already exists, then freeze the j
                if not create_edge and not create_branch:
                    break

                # Rule 2 : Need to create a new edge
                elif create_edge:
                    self.create_new_edge(self.active_node, i, global_end, j, current_index)

                # Rule 2: Create branch
                else:

                    # implement branch
                    branch_node = self.branch(current_index, active_edge, i, global_end, j)

                    # set the suffix link of the previous node as the branch node and update the self.previous_node
                    if self.previous_node is not None:
                        self.previous_node.update_suffix_link(branch_node)
                        self.previous_node = branch_node
                    else:
                        self.previous_node = branch_node

                # increment the j and update the self.active_node to its suffix_link
                j += 1
                self.active_node = self.active_node.get_suffix_link()

                # if self.active_node is the root, self.active_length should be i - j for next extension
                if self.active_node.is_root:
                    self.active_length = i - j

            # increment i and self.active_length
            i += 1
            self.active_length += 1

    def traverse_inorder(self):
        """
        Description: perform in order traversal to the suffix tree created using ukkonen algorithm by calling
                     self.traverse_inorder_aux function
        Written by: Kuah Jia Chen
        Input: None
        Return: ans is an array that stores the suffix_id of the self.input_string
        Time complexity (Worst case) : O(N), where N is the length of self.input_string
        Space complexity:
            Input: O(1)
            Aux: O(N), where N is the length of the self.input_string
        """
        ans = []
        ans = self.traverse_inorder_aux(self.root, ans)
        return ans

    def traverse_inorder_aux(self, current_node, current_list):
        """
        Description: perform in order traversal to the suffix tree created using ukkonen algorithm
        Written by: Kuah Jia Chen
        Input: current_node is a Node instance, and current_list is an array
        Return: the current_list is an array
        Time complexity (Worst case) : O(M), where M is the number of edges in the current_node
        Space complexity:
            Input: O(A), where A is the length of current_list
            Aux: O(1)
        """
        if current_node is not None and current_node.is_leaf:
            current_list.append(current_node.suffix_id)

        elif current_node is not None:
            for edge in current_node.edges:
                self.traverse_inorder_aux(edge, current_list)

        return current_list


def read_file(file_path):
    """
    Description: read the input from the input text file
    Written by: Kuah Jia Chen
    Input: file_path is the file path to access the file
    Return: return the content in the file
    """
    f = open(file_path, 'r')
    line = f.readlines()
    f.close()
    return line


def writeOutput(suffix_array):
    """
    Description: write the answer to the output file
    Written by: Kuah Jia Chen
    Input: the suffix_array of the input_string
    Return: None
    """
    # open output file with correct name
    outputFile = open("output_sa.txt", "w")

    for suffix_id in suffix_array:
        outputFile.write(str(suffix_id + 1))
        outputFile.write("\n")

    # close output file
    outputFile.close()


if __name__ == '__main__':
    # retrieve the file paths from the commandline arguments
    _, filename1 = sys.argv
    print("Number of arguments passed : ", len(sys.argv))
    # since we know the program takes one argument
    print("First argument : ", filename1)
    file1content = read_file(filename1)
    print("\nContent of first file : ", file1content)
    input_string = file1content[0]
    suffix_tree = SuffixTree(input_string)
    suffix_array = suffix_tree.traverse_inorder()
    writeOutput(suffix_array)
