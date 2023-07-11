########################
# Question 2 (Encoder) #
########################

import heapq
import sys


class BinaryPacker:

    def __init__(self, file_name):
        """
        Description: initialise the attributes of an instance of BinaryPacker
        Written by: Kuah Jia Chen
        Input: file_name is a string
        Return: None
        Time complexity (Worst case) : O(1)
        Space complexity:
            Input: O(1)
            Aux: O(1)
        """
        self.my_bit_string = []
        self.file = open(file_name, "wb")

    def append(self, bit_string):
        """
        Description: append the bit_string to self.bit_string and pack it to file
        Written by: Kuah Jia Chen
        Input: bit_string is an array of "bits" string, e.g., ["0", "1", "0"]
        Return: None
        Time complexity (Worst case) : O(N + M), where N and M is the length of self.my_bit_string and
                                       bit_string respectively
        Space complexity:
            Input: O(M), where M is the length of bit_string
            Aux: O(N + M), where N and M is the length of self.my_bit_string and bit_string respectively
        """
        self.my_bit_string = self.my_bit_string + bit_string
        # pack to file whenever my_bit_string exceed 8 characters to keep the bit string short throughout the process
        self.pack_to_file()

    def pack_to_file(self):
        """
        Description: pack the current bits into file
        Written by: Kuah Jia Chen
        Input: None
        Return: None
        Time complexity (Worst case) : O(N), where N is the length of self.my_bit_string
        Space complexity:
            Input: O(1)
            Aux: O(N), where N is the length of self.bit_string
        """
        # while there is more than 8 bits in the self.my_bit_string
        while len(self.my_bit_string) >= 8:
            # get the first eight bit string to write
            my_bit_string_to_write = "".join(self.my_bit_string[:8])
            # update self.my_bit_string
            self.my_bit_string = self.my_bit_string[8:]
            # convert it to integer
            my_number = int(my_bit_string_to_write, 2)
            # convert it to bytes and write it to file
            my_byte = my_number.to_bytes(1, byteorder='big')
            self.file.write(my_byte)

    def pack_to_file_last_byte(self):
        """
        Description: pack the last byte into file
        Written by: Kuah Jia Chen
        Input: None
        Return: None
        Time complexity (Worst case) : O(N), where N is the length of self.my_bit_string
        Space complexity:
            Input: O(1)
            Aux: O(N), where N is the length of self.bit_string
        """
        if len(self.my_bit_string) >= 1:
            my_bit_string_to_write = "".join(self.my_bit_string[:])
            # print(my_bit_string_to_write)
            while len(my_bit_string_to_write) < 8:
                my_bit_string_to_write += "0"
            my_number = int(my_bit_string_to_write, 2)
            my_byte = my_number.to_bytes(1, byteorder='big')
            self.file.write(my_byte)

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


def q2_encoder(input_string, file_name):
    """
    Description: encode the input_string using its Burrows-Wheeler Transform and write it to the file
    Written by: Kuah Jia Chen
    Input: input_string is a string and file_name is a string
    Return: None
    Time complexity (Worst case) : O(N^2 * log N + N * log N + N + log N), where N is the length of bwt_string
    Space complexity:
        Input: O(N + M), where N is the length of input_string and M is the length of file_name
        Aux: O(N^2 + A + B * C), where N is the length of bwt_string, A is the length of the bwt_run_length_tuples,
             B is the length of frequency_table, C is the max(len(codeword)) in character_encoding
    """

    # get the bwt string for input_string
    bwt_string = bwt(input_string)

    # get the elias codewords for the length of bwt_string
    elias_length = elias(len(bwt_string))

    # construct the frequency table and get the unique characters in the bwt_string
    frequency_table, unique_characters = get_frequency_unique(bwt_string)

    # get the elias codewords for the number of unique characters
    elias_unique_char = elias(len(unique_characters))

    # get the ascii code word in 7 bits for each unique character
    ascii_code_word = []
    character_encoding = huffman_encoder(bwt_string, frequency_table, unique_characters)
    for i in range(len(character_encoding)):

        if character_encoding[i] is not None:
            current_ascii = i + 37 if i != len(character_encoding) - 1 else 36
            ascii_code_word.append("".join(bit_representation(current_ascii, True)))

    # get the huffman code word for each unique character
    huffman_code_word = []
    for i in range(len(character_encoding)):
        if character_encoding[i] is not None:
            current_code_word = "".join(character_encoding[i])[::-1]
            huffman_code_word.append(current_code_word)

    # get the elias code word the length of its constructed Huffman code word for each unique character
    elias_code_word = []
    for i in range(len(huffman_code_word)):
        current_length = len(huffman_code_word[i])
        current_elias_code_word = elias(current_length)
        elias_code_word.append(current_elias_code_word)

    # create BinaryPacker instance
    output_binary_stream = BinaryPacker(file_name)

    # append and write the elias code word for length of bwt_string and number of unique characters to file
    output_binary_stream.append(list(elias_length))
    output_binary_stream.append(list(elias_unique_char))

    # append and write the ascii, elias of length for Huffman code word, and huffman code word
    # for each character to file
    for i in range(len(ascii_code_word)):
        output_binary_stream.append(list(ascii_code_word[i]))
        output_binary_stream.append(list(elias_code_word[i]))
        output_binary_stream.append(list(huffman_code_word[i]))

    # get the run length tuples for the bwt_string
    bwt_run_length_tuples = run_length_encoded_tuples(bwt_string)

    # for each run length encoded tuple, get the Huffman codeword of the character being encoded and
    # the Elias codeword of its run length and write it to file
    for i in range(len(bwt_run_length_tuples)):
        current_char = bwt_run_length_tuples[i][0]
        current_index = ord(current_char) - 37 if current_char != '$' else len(character_encoding) - 1

        current_huffman = "".join(character_encoding[current_index])[::-1]
        current_elias = elias(bwt_run_length_tuples[i][1])

        output_binary_stream.append(list(current_huffman))
        output_binary_stream.append(list(current_elias))

    # write the last byte to file
    output_binary_stream.pack_to_file_last_byte()
    # close the file
    output_binary_stream.close()

    return None


def run_length_encoded_tuples(bwt_string):
    """
    Description: compute the run length encoded tuples for the bwt_string
    Written by: Kuah Jia Chen
    Input: bwt_string is a string
    Return: the run length encoded tuples for the bwt_string
    Time complexity (Worst case) : O(N), where N is the length of bwt_string
    Space complexity:
        Input: O(N), where N is the length of bwt_string
        Aux: O(M), where M is the length of the output array
    """
    if len(bwt_string) == 0:
        return []

    tuples = [[bwt_string[0], 1]]

    for i in range(1, len(bwt_string)):

        last_tuple = tuples[len(tuples) - 1]
        previous_char = last_tuple[0]
        current_char = bwt_string[i]

        if previous_char == current_char:
            tuples[len(tuples) - 1][1] += 1
        else:
            tuples.append([bwt_string[i], 1])

    return tuples


def naive_suffix_array(input_string):
    """
    Description: use the naive approach to generate the suffix array of the input_string
    Written by: Kuah Jia Chen
    Input: input_string is a string
    Return: the suffix array of the input_string
    Time complexity (Worst case) : O(N^2 * log N), where N is the length of bwt_string
    Space complexity:
        Input: O(N), where N is the length of bwt_string
        Aux: O(N^2), where N is the length of bwt_string
    """
    suffixes = []

    for i in range(len(input_string)):
        current_string = input_string[i:]
        current_tuple = (current_string, i)
        suffixes.append(current_tuple)

    suffixes = sorted(suffixes)

    suffix_array = []

    for suffix, suffix_id in suffixes:
        suffix_array.append(suffix_id)

    return suffix_array


def bwt(text):
    """
    Description: generate the bwt string for the text
    Written by: Kuah Jia Chen
    Input: text is a string
    Return: the bwt string for the text
    Time complexity (Worst case) : O(N^2 * log N), where N is the length of bwt_string
    Space complexity:
        Input: O(N), where N is the length of bwt_string
        Aux: O(N^2), where N is the length of bwt_string
    """
    text = text + "$"
    suffix_array = naive_suffix_array(text)
    n = len(text)
    ans = []

    for i in range(n):
        current_index = suffix_array[i] - 1
        ans.append(text[current_index])

    return "".join(ans)


def huffman_encoder(input_string, frequency_table, unique_characters):
    """
    Description: compute the Huffman codeword for each unique characters
    Written by: Kuah Jia Chen
    Input: input_string is a string, frequency_table is an array contains the frequency for each
           characters and unique_characters is an array contains the unique characters
    Return: the character_encoding that contains the Huffman code word for each character
    Time complexity (Worst case) : O(N * log N), where N is the length of input_string
    Space complexity:
        Input: O(N + A + B), where N is the length of input_string, A and B is the length of frequency_table
               and unique_characters respectively
        Aux: O(A * max(len(codeword))), where A is the length of frequency_table
    """

    # create the min heap by adding each unique characters with frequency

    min_heap = []

    for i in range(len(unique_characters)):
        current_char = unique_characters[i]

        current_index = ord(current_char) - 37 if current_char != "$" else len(frequency_table) - 1

        current_frequency = frequency_table[current_index]

        # For lists, the comparison uses lexicographical ordering: first the first two items are compared,
        # and if they differ this determines the outcome of the comparison; if they are equal, the next
        # two items are compared, and so on, until either sequence is exhausted.

        # since we need to consider the length of character for the comparison happen in min heap
        # we need to include the length of the character (or string when we start to concatenate them)
        # in the tuple

        current_ascii = ord(current_char) if current_char != "$" else 127
        current_elem = [current_frequency, len(current_char), current_ascii, current_char]

        min_heap.append(current_elem)

    # heapify the min_heap list
    heapq.heapify(min_heap)

    # store the encoding of the characters
    character_encoding = [None] * 91

    if len(unique_characters) == 1:

        # append 0 to the only characters
        char_from_first = unique_characters[0]

        for i in range(len(char_from_first)):
            current_elem_char = char_from_first[i]
            current_elem_index = ord(current_elem_char) - 37 if current_elem_char != "$" else len(frequency_table) - 1

            if character_encoding[current_elem_index] is None:
                character_encoding[current_elem_index] = []
            character_encoding[current_elem_index].append("0")

    while len(min_heap) >= 2:

        first_elem = heapq.heappop(min_heap)
        second_elem = heapq.heappop(min_heap)

        # append 0 to characters in the first element
        char_from_first = first_elem[3]

        for i in range(len(char_from_first)):

            current_elem_char = char_from_first[i]
            current_elem_index = ord(current_elem_char) - 37 if current_elem_char != "$" else len(frequency_table) - 1

            if character_encoding[current_elem_index] is None:
                character_encoding[current_elem_index] = []

            character_encoding[current_elem_index].append("0")

        # append 1 to characters in the first element
        char_from_second = second_elem[3]
        for i in range(len(char_from_second)):

            current_elem_char = char_from_second[i]
            current_elem_index = ord(current_elem_char) - 37 if current_elem_char != "$" else len(frequency_table) - 1

            if character_encoding[current_elem_index] is None:
                character_encoding[current_elem_index] = []

            character_encoding[current_elem_index].append("1")

        current_sum_freq_char = first_elem[0] + second_elem[0]
        current_sum_length = first_elem[1] + second_elem[1]
        current_ascii = max(first_elem[2], second_elem[2])
        current_characters = first_elem[3] + second_elem[3]

        heapq.heappush(min_heap, [current_sum_freq_char, current_sum_length, current_ascii, current_characters])

    ans = []

    # get the Huffman code word for each character
    for i in range(len(input_string)):
        current_char = input_string[i]
        current_index = ord(current_char) - 37 if current_char != "$" else len(frequency_table) - 1
        current_encoding = character_encoding[current_index]

        for j in range(len(current_encoding) - 1, -1, -1):
            ans.append(current_encoding[j])

    return character_encoding


def get_frequency_unique(input_string):
    """
    Description: get the frequency table and the unique characters in input_string
    Written by: Kuah Jia Chen
    Input: input_string is a string
    Return: the frequency table and the unique characters in input_string
    Time complexity (Worst case) : O(N), where N is the length of input_string
    Space complexity:
        Input: O(N), where N is the length of input_string
        Aux: O(M), where M is the length of unique_character
    """
    # create a list to store unique character
    unique_character = []

    # ASCII values from 37 to 126 (36 "$" is included because it will be generated as part of the bwt string)
    frequency_table = [0] * 91

    # construct the frequency table and store all the unique character into a list
    for i in range(len(input_string)):

        current_char = input_string[i]

        current_index = ord(current_char) - 37 if current_char != "$" else len(frequency_table) - 1

        # it means that this character has not been added to unique character list
        if frequency_table[current_index] == 0:
            frequency_table[current_index] = 1
            unique_character.append(current_char)

        else:
            frequency_table[current_index] += 1

    return frequency_table, unique_character


def elias(input_num):
    """
    Description: get the elias code word for the input_num
    Written by: Kuah Jia Chen
    Input: input_num is an integer
    Return: the elias code word for the input_num
    Time complexity (Worst case) : O(log N), where N is the input_num
    Space complexity:
        Input: O(1)
        Aux: O(log N), where N is the input_num
    """

    # get the bit representation of the input_num
    input_num_bit = bit_representation(input_num)

    length_of_bits = len(input_num_bit)

    ans = []

    # use the elias formula to get the bits that encode the length of input_num_bit
    while length_of_bits > 1:

        current_length = length_of_bits - 1
        current_length_bits = bit_representation(current_length)
        current_length_bits[0] = '0'

        for i in range(len(current_length_bits) - 1, -1, -1):
            ans.append(current_length_bits[i])

        length_of_bits = len(current_length_bits)

    # reverse the whole list since they are now in reverse order
    ans = ans[::-1]

    # append the input_num_bit to ans
    for j in range(len(input_num_bit)):
        ans.append(input_num_bit[j])

    return ''.join(ans)


def bit_representation(num, is_seven=False):
    """
    Description: get the bit representation for the num, if is_seven is true, then the function we make
                 sure that output is length of 7
    Written by: Kuah Jia Chen
    Input: num is an integer
    Return: the bit representation for the num
    Time complexity (Worst case) : O(log N), where N is the num
    Space complexity:
        Input: O(1)
        Aux: O(log N), where N is the num
    """
    ans = []

    # get the bit representation of the num
    while num > 1:
        remainder = num % 2
        ans.append(str(remainder))
        num //= 2

    ans.append(str(num))

    # append "0" until the length of output is seven if is_seven is true
    if is_seven:
        while len(ans) < 7:
            ans.append("0")

    # return the ans in reverse order
    return ans[::-1]


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


if __name__ == '__main__':
    # # retrieve the file paths from the commandline arguments
    # _, filename1 = sys.argv
    # print("Number of arguments passed : ", len(sys.argv))
    # # since we know the program takes one argument
    # print("First argument : ", filename1)
    # file1content = read_file(filename1)
    # print("\nContent of first file : ", file1content)
    # input_string = file1content[0]
    # q2_encoder(input_string, "bwtencoded.bin")
    print(elias(17))
