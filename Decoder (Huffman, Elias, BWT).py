########################
# Question 2 (Decoder) #
########################

import sys


class BinaryUnPacker:

    def __init__(self, file_name):
        """
        Description: initialise the attributes of an instance of BinaryUnpacker
        Written by: Kuah Jia Chen
        Input: file_name is a string
        Return: None
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.my_bit_string = []
        self.file = open(file_name, "rb")

    def get_bit_string(self):
        """
        Description: get the bit string from the file
        Written by: Kuah Jia Chen
        Input: None
        Return: the bit stream represented in bit string form that reads from the binary file
        Time complexity (Worst case) : O(N + M), where N and M is the length of all bit strings in ans and
                                       the number of bytes in the file respectively
        Space complexity:
            Input: O(1)
            Aux: O(N), where N is the length of all bit strings in ans
        """
        ans = []

        current_byte = self.file.read(1)

        while current_byte:
            # read the byte
            current_byte = bin(int.from_bytes(current_byte, byteorder='big'))

            # exclude the prefix "0b"
            current_byte = current_byte[2:]

            # add leading zero(s)
            current_byte = self.add_leading_zero(current_byte)

            ans.append(current_byte)

            # for each iteration, read one byte from the file
            current_byte = self.file.read(1)

        return "".join(ans)

    def add_leading_zero(self, byte):
        """
        Description: add leading zero(s) to byte if its length is less than 8
        Written by: Kuah Jia Chen
        Input: byte is a string
        Return: byte is a string with a length of 8
        Time complexity (Worst case) : O(A), where A is 8 - len(byte)
        Space complexity:
            Input: O(1)
            Aux: O(N), where N is the length of all bit strings in ans
        """
        if len(byte) == 8:
            return byte
        else:
            number_of_leading_zeros = 8 - len(byte)
            byte = (number_of_leading_zeros * "0") + byte
            return byte

    def close(self):
        """
        Description: close the file
        Written by: Kuah Jia Chen
        Input: None
        Return: None
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.file.close()


def q2_decoder(bit_string):
    """
    Description:  decode and recover the original string str[1 . . . n] from a binary encoded file
    Written by: Kuah Jia Chen
    Input: bit_string is a string
    Return: original string str[1 . . . n] from a binary encoded file
    Time complexity (Worst case) : O(N + log N + number_unique_char * log N),
                                   where N is the length of bit_string
    Space complexity:
        Input: O(N), where N is the length of bit_string
        Aux: O(N + M), where N is the length of bwt_string,, where M is the number_unique_char
    """

    # initialize the pointer that will always pointer at the first unprocessed bit in bit_string
    current_start_index = 0

    bit_string = list(bit_string)

    # get the length of the original string in bwt string form and update the pointer
    length_of_string, current_start_index = elias_decoder(bit_string, current_start_index)

    # get the number of unique characters of the original string in bwt string form and update the pointer
    number_unique_char, current_start_index = elias_decoder(bit_string, current_start_index)

    # create huffman decoder
    huffman_tree = HuffmanDecoder()

    for i in range(number_unique_char):
        # get the ascii of the current character of the original string in bwt string form and update the pointer
        current_ascii, current_start_index = ascii_to_int(bit_string, current_start_index)

        # get the huffman code word length of the current character of the original string in bwt string form
        # and update the pointer
        code_length, current_start_index = elias_decoder(bit_string, current_start_index)

        # insert it to the huffman tree
        huffman_tree.insert(bit_string[current_start_index: current_start_index + code_length], chr(current_ascii))
        # update the pointer
        current_start_index += code_length

    run_length_encode_tuples = []
    # create a pointer to check when to stop processing the bit string
    pointer = 0
    while current_start_index < len(bit_string):
        # get the current character of the original string in bwt string form and update the pointer
        current_char, current_start_index = huffman_tree.find_character(bit_string, current_start_index)

        # get the run length of the current character of the original string in bwt string form and update the pointer
        current_run_length, current_start_index = elias_decoder(bit_string, current_start_index)

        run_length_encode_tuples.append([current_char, current_run_length])

        pointer += current_run_length

        # if pointer is equal to the length of string, we can stop processing the bit string
        if pointer == length_of_string:
            break

    ans = []

    # loop through the run_length_encode_tuples to get the original string in bwt string form
    for run_length_tuple in run_length_encode_tuples:

        for _ in range(run_length_tuple[1]):
            ans.append(run_length_tuple[0])

    # get the original string by invert the original string in bwt string form
    ans = invert_bwt_string("".join(ans))

    return ans


def invert_bwt_string(bwt_string):
    """
    Description:  invert the bwt_string to get the original string
    Written by: Kuah Jia Chen
    Input: bwt_string is a string
    Return: original string str[1 . . . n] from a binary encoded file
    Time complexity (Worst case) : O(N), where N is the length of bwt_string
    Space complexity:
        Input: O(N), where N is the length of bwt_string
        Aux: O(N), where N is the length of bwt_string
    """

    order_table, rank_table, frequency_table = get_frequency_order_rank_table(bwt_string)

    original_string = [None] * len(bwt_string)
    original_string[-1] = "$"
    original_string_index = len(original_string) - 2

    current_bwt_index = 0

    while bwt_string[current_bwt_index] != "$":
        current_char = bwt_string[current_bwt_index]
        original_string[original_string_index] = current_char
        current_rank = rank_table[ord(current_char) - 36]
        current_order = order_table[current_bwt_index] - 1
        next_char = current_rank + current_order - 1
        current_bwt_index = next_char
        original_string_index -= 1

    original_string = original_string[:-1]

    return "".join(original_string)


def get_frequency_order_rank_table(bwt_string):
    """
    Description:  get the frequency table, order table and rank table for the bwt_string
    Written by: Kuah Jia Chen
    Input: bwt_string is a string
    Return: get the frequency table, order table and rank table for the bwt_string
    Time complexity (Worst case) : O(N), where N is the length of bwt_string
    Space complexity:
        Input: O(N), where N is the length of bwt_string
        Aux: O(N), where N is the length of bwt_string
    """
    frequency_table = [0] * 91
    order_table = []
    rank_table = []

    for i in range(len(bwt_string)):
        current_char = bwt_string[i]
        current_index = ord(current_char) - 36
        frequency_table[current_index] += 1
        order_table.append(frequency_table[current_index])

    for i in range(len(frequency_table)):
        if i == 0:
            rank_table.append(frequency_table[0])
        else:
            current_num = rank_table[i - 1] + frequency_table[i - 1]
            rank_table.append(current_num)

    return order_table, rank_table, frequency_table


class Node:

    def __init__(self, value=None):
        """
        Description: initialise the attributes of an instance of Node
        Written by: Kuah Jia Chen
        Input: value is a character
        Return: None
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.value = value
        self.child = [None] * 3

    def __str__(self):
        """
        Description: return the string that contains the value and child of the instance of Node
        Written by: Kuah Jia Chen
        Input: None
        Return: the string that contains the value and child of the instance of Node
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        # debug purpose
        return str(self.value) + "" + str(self.child)


class HuffmanDecoder:

    def __init__(self):
        """
        Description: initialise the attributes of an instance of HuffmanDecoder
        Written by: Kuah Jia Chen
        Input: None
        Return: None
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.root = Node()

    def insert(self, bit_encoding, character):
        """
        Description: insert the bit_encoding for the character to the Huffman tree
        Written by: Kuah Jia Chen
        Input: bit_encoding is a list of bit strings and character is a string
        Return: None
        Time complexity (Worst case) : O(N), where N is the length of bit_encoding
        Space complexity:
            Input: O(N), where N is the length of bit_encoding
            Aux: O(N), where N is the length of bit_encoding
        """

        current_node = self.root

        for bit in bit_encoding:
            # if path exists, then insert the bit
            if current_node.child[int(bit)] is not None:
                current_node = current_node.child[int(bit)]
            # if path doesn't exist, create a node and insert the bit
            else:
                current_node.child[int(bit)] = Node()
                current_node = current_node.child[int(bit)]
        # put the character at the last node
        current_node.value = character

    def find_character(self, bit_string, start_index):
        """
        Description: find the character using the bit string from the Huffman tree
        Written by: Kuah Jia Chen
        Input: bit_string is a string, start_index is an integer
        Return: ans is the character with the bit_string encoding and (start_index + counter)
                is the updated pointer value
        Time complexity (Worst case) : O(N), where N is the length of bit_string
        Space complexity:
            Input: O(N), where N is the length of bit_string
            Aux: O(1)
        """
        ans = None
        current_node = self.root
        counter = 0

        for i in range(start_index, len(bit_string)):
            current_bit = bit_string[i]
            current_node = current_node.child[int(current_bit)]
            counter += 1

            if current_node.value is not None:
                ans = current_node.value
                current_node = self.root
                break

        return ans, start_index + counter


def bin_to_int(bit_string, flip=False):
    """
    Description: convert binary to integer
    Written by: Kuah Jia Chen
    Input: bit_string is a string
    Return: the bit_string in integer form
    Time complexity (Worst case) : O(N), where N is the length of bit_string
    Space complexity:
        Input: O(N), where N is the length of bit_string
        Aux: O(1)
    """
    if flip:
        bit_string[0] = "1"

    ans = 0
    i = len(bit_string) - 1
    j = 0

    while i >= 0:
        ans += 2 ** j * (int(bit_string[i]))
        i -= 1
        j += 1
    return ans


def ascii_to_int(bit_string, start_index):
    """
    Description: convert ascii to integer
    Written by: Kuah Jia Chen
    Input: bit_string is a string, start_index is an integer
    Return: ans is the bit_string in integer form, and (start_index + 7) is the updated pointer value
    Time complexity (Worst case) : O(1)
    Space complexity:
        Input: O(N), where N is the length of bit_string
        Aux: O(1)
    """
    ans = 0

    i = start_index + 7 - 1
    j = 0
    counter = 7

    while counter > 0:
        ans += 2 ** j * (int(bit_string[i]))
        i -= 1
        j += 1
        counter -= 1

    return ans, start_index + 7


def elias_decoder(bit_string, start_index):
    """
    Description: decode the elias code word to the integer
    Written by: Kuah Jia Chen
    Input: bit_string is a string, start_index is an integer
    Return: ans is the current elias code word in integer form, and pointer is the updated pointer value
    Time complexity (Worst case) : O(log N), where N is the value of ans
    Space complexity:
        Input: O(M), where M is the length of bit_string
        Aux: O(1)
    """
    pointer = start_index
    length_to_check = 1
    ans = None

    while pointer < len(bit_string):

        current_bit = bit_string[pointer]
        # use the formula to get the current elias encoding and find the length that used to encode the final integer
        if current_bit == "0":
            current_elias_encoding = bit_string[pointer:pointer + length_to_check]
            current_elias_int = bin_to_int(current_elias_encoding, True) + 1
            pointer += length_to_check
            length_to_check = current_elias_int

        else:
            # if current_bit is not "0", (i.e., "1"), it means we reach the bit that represents the final integer
            # thus, we can use the length_to_check to find the value of final integer
            current_elias_encoding = bit_string[pointer:pointer + length_to_check]
            current_elias_int = bin_to_int(current_elias_encoding)
            pointer += length_to_check
            # reset previous elias
            length_to_check = 1
            ans = current_elias_int
            break

    return ans, pointer


def writeOutput(original_string):
    """
    Description: write the original_string to the text file
    Written by: Kuah Jia Chen
    Input: original_string is the string to write to the file
    Return: None
    """
    # Open output file with correct name
    outputFile = open("recovered.txt", "w")
    # write results to an output file
    outputFile.write(original_string)
    # Close output file
    outputFile.close()


if __name__ == '__main__':
    # retrieve the file paths from the commandline arguments
    _, filename1 = sys.argv
    print("Number of arguments passed : ", len(sys.argv))
    # since we know the program takes one argument
    print("First argument : ", filename1)
    input_bit_stream = BinaryUnPacker(filename1)
    input_string = input_bit_stream.get_bit_string()
    print("input_string", input_string)
    # print(("ans", q2_decoder(input_string)))
    writeOutput(q2_decoder(input_string))
