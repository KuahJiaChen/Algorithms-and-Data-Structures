class Node:
    def __init__(self):
        """
        Purpose: initialise the attributes of an instance of node
        Argument: self is an instance of node
        Return: none
        Complexity:
            - time complexity: O(1)
            - auxiliary space complexity: O(1)
        References: Referred to the lecture recording https://youtu.be/gr647pytPso
        """
        # initialize the link with a size of 27, where index 0 is for the terminal $
        self.link = [None] * 27
        self.frequency = 0


class Trie:
    def __init__(self):
        """
        Purpose: initialise the attributes of an instance of trie
        Argument: self is an instance of trie
        Return: none
        Complexity:
            - time complexity: O(1)
            - auxiliary space complexity: O(1)
        References: Referred to the lecture recording https://youtu.be/gr647pytPso
        """
        self.root = Node()

    def insert(self, input_string):
        """
        Purpose: insert the input string into this instance of trie
        Argument: self is an instance of trie, input_string is a string
        Return: none
        Complexity:
            - time complexity: O(N), where N is the number of characters in input_string
            - auxiliary space complexity: O(N), where N is the number of characters in input_string
        References: Referred to the lecture recording https://youtu.be/gr647pytPso
        """
        current_node = self.root
        current_node.frequency += 1
        for char in input_string:
            index = ord(char) - 97 + 1
            # if path exits
            if current_node.link[index] is not None:
                current_node = current_node.link[index]
            # if path doesnt exist
            else:
                # create a new node
                current_node.link[index] = Node()
                current_node = current_node.link[index]
            current_node.frequency += 1
        # now go to the terminal
        if current_node.link[0] is not None:
            current_node = current_node.link[0]
        # if path doesnt exist
        else:
            # create a new node
            current_node.link[0] = Node()
            current_node = current_node.link[0]
        current_node.frequency += 1

    def find_lexicographically_later(self, input_string):
        """
        Purpose: find the number of words that is lexicographically later than the input_string
        Argument: self is an instance of trie, input_string is a string
        Return: return the number of words that is lexicographically later than the input_string
        Complexity:
            - time complexity: O(N), where N is the number of characters in input_string
            - auxiliary space complexity: O(1)
        """
        count = 0
        current_node = self.root
        for char in input_string:
            # a = 1, b = 2, c = 3 ...
            index = ord(char) - 97 + 1
            for i in range(index + 1, 27):  # since the maximum of loop always be 27, it can be treated as constant
                # complexity hence O(1)
                if current_node.link[i] is not None:
                    count += current_node.link[i].frequency
                else:
                    count += 0
            current_node = current_node.link[index]
        if current_node.link[0] is not None:
            # minus the frequency of words that same as the string
            count += current_node.frequency - current_node.link[0].frequency
        else:
            count += current_node.frequency
        return count


def lex_pos(text, queries):
    """
    Purpose: Find the number of words in the text list that is lexicographically later than the each of the string
             in the queries list
    Argument: text is an unsorted list of strings and each of the string in text list only contains lowercase a-z
              characters, queries is a list of strings and each of the string in queries list only contains lowercase
              a-z characters. Besides that, each string in queries is a prefix of some string in text
    Return: Return a list of numbers such that the i(th) element in this list represents that number of words in text
            which are lexicographically greater than the i(th) element in queries
    Complexity:
        - time complexity: O(T+Q), where T is the sum of the number of characters in all strings in text list and Q is
                           the total number of characters in all strings in queries list.
        - auxiliary space complexity: O(T+N), where T is the sum of number of characters in all strings in text list and
                                      N is the total number of elements in queries list.
    """
    ans = []
    strings = Trie()
    for i in range(len(text)):
        strings.insert((text[i]))
    for j in range(len(queries)):
        ans.append(strings.find_lexicographically_later(queries[j]))
    return ans


