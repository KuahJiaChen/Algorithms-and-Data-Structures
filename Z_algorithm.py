########################
#####  Question 1  #####
########################

import sys


# For documentation of each function, I had written two big O complexity, where the first one is a more detailed
# complexity, and the second one is the simplified one

def q1(pattern, text):
    """
    Description: find all occurrences of any given pattern pat[1 . . . m] within any given text txt[1 . . . n], while
                 allowing for at most one transposition error
    Written by: Kuah Jia Chen
    Input: pattern is a string and text is a string
    Return: the number of matched indices (both exact match and transposition error) and the list of matched indices
    Time complexity (Worst case) : O(N + M), where N is the length of the text and M is the length of
                                   the pattern
    Space complexity:
        Input: O(N + M), where N is the length of the text and M is the length of the pattern
        Aux: O(N + M + A + B), where N is the length of the text and M is the length of the
             pattern (due to forward z algo and backward z algo function), A and B is the number of matched indices with
             exact occurrence and matched indices with one transposition error respectively that both will be store in a
             list.
    """

    if not text or not pattern or len(pattern) > len(text):
        return 0, []

    # concatenate pattern to text and use it to get the z_array so that we can know that for each character in the
    # string, how many characters matching the pattern, starting from its index onwards
    # O(N + M)
    forward_z_algo_string = pattern + "$" + text

    # concatenate text to pattern and use it to get the reverse z_array so that we can know that for each character
    # in the text, how many characters matching the pattern, starting from its index backwards
    # O(N + M)
    backward_z_algo_string = text + "$" + pattern

    # get the foward z_array using normal z algorithm
    forward_z_array = z_algorithm(forward_z_algo_string)

    # get the back z_array using the backward z algorithm
    backward_z_array = reverse_z_algorithm(backward_z_algo_string)

    # stores the matched indices
    ans = []

    # loop through the forward_z_array and backward_z_array to find the position of each occurrence of the
    # pattern in the text and the starting position (again in the text) of any transposition, when this is
    # not an exact occurrence.

    for i in range(len(pattern) + 1, len(forward_z_array)):  # (5, 20)

        # when there is exact match of pattern occurs in the text starting from index (i - (len(pattern) + 1))th
        if forward_z_array[i] == len(pattern):
            ans.append([i + 1 - len(pattern) - 1])

        # when there is no exact match of pattern occurs in the text starting from index (i - (len(pattern) + 1))th
        else:

            # if there is enough remaining characters in text that possibly matches with pattern
            if i < len(forward_z_array) - len(pattern) + 1:

                # from forward_z_array, we can get the number of characters matching the pattern, starting from
                # this index onwards
                # from backward_z_array, we can get the number of characters matching the pattern, starting from
                # this index + len(pattern) + len("$")   backwards
                #
                # thus, at this (i + forward_z_array[i] - len(pattern) - 1)th index as the starting position of the
                # text, we will need to use the forward_z_array and backward_z_array to know the length of prefix and
                # length of suffix of this substring that matches the prefix or suffix of the pattern.
                #
                # The length of prefix can be obtained in the forward_z_array with index of (i)th.
                #
                # The length of prefix can be obtained in the backward_z_array with index of (i-2)th.
                #
                # backward_z_array[i - 2] is because backward_z_array[i + len(pattern) - 1 - len(pattern) - 1)

                if forward_z_array[i] + backward_z_array[i - 2] == len(pattern) - 2:

                    # check if it there is one transposition error
                    if text[i + forward_z_array[i] - len(pattern) - 1] == pattern[forward_z_array[i] + 1] and \
                            text[i + forward_z_array[i] + 1 - len(pattern) - 1] == pattern[forward_z_array[i]]:
                        ans.append([i + 1 - len(pattern) - 1, i + forward_z_array[i] + 1 - len(pattern) - 1])

    return len(ans), ans


def z_algorithm(input_string):
    """
    Description: return an array that stores the length of the longest substring, starting from that particular index
                 onwards, matches its prefix
    Written by: Kuah Jia Chen
    Input: input_string is a string
    Return: return an array that stores the length of the longest substring, starting from that particular index,
            matches its prefix
    Time complexity (Worst case) : O(K), where K is the length of the input string
    Space complexity:
        Input: O(K), where K is the length of the input string
        Aux: O(K), where K is the length of the input string
    """
    # initialize zarray to return
    return_zarray = [None] * len(input_string)  # O(n) space

    # initialize the zbox (left and right)
    # zbox_right is exclusive
    zbox_left, zbox_right = 0, 0

    # loop through the string
    i = 0
    while i < len(input_string):

        if i == 0:
            return_zarray[i] = len(input_string)

        elif i < zbox_right:  # if inbox

            # k is the ith mirror in the left box
            k = i - zbox_left + 1  # + 1 since i is inclusive
            # remaining
            remaining = zbox_right - i

            if return_zarray[k] < remaining:
                return_zarray[i] = return_zarray[k]

            elif return_zarray[k] > remaining:
                return_zarray[i] = remaining

            else:  # z[k] == remaining
                # explicit
                zbox_left, zbox_right, length = explicit_comparison(i, input_string)
                return_zarray[i] = length

        else:  # i >= zbox_right
            # explicit
            zbox_left, zbox_right, length = explicit_comparison(i, input_string)
            return_zarray[i] = length

        i += 1

    return return_zarray


def explicit_comparison(i, input_string):
    """
    Description: perform explicit comparison to return the new z box's range and its length
    Written by: Kuah Jia Chen
    Input: i is an integer that indicates the starting position of the new z box and input_string is a string
    Return: return the range of new z box and its length
    Time complexity (Worst case) : O(K), where K is the length of the input string
    Space complexity:
        Input: O(K), where K is the length of the input string
        Aux: O(1)
    """
    zbox_left, zbox_right, index = i, i, 0
    while i < len(input_string) and input_string[zbox_right] == input_string[index]:
        i += 1
        zbox_right = i
        index += 1
    return zbox_left + 1, zbox_right, zbox_right - zbox_left


def reverse_z_algorithm(input_string):
    """
    Description: return an array that stores the length of the longest substring, starting from that particular index
                 backwards, matches its suffix
    Written by: Kuah Jia Chen
    Input: input_string is a string
    Return: return an array that stores the length of the longest substring, starting from that particular index
            backwards, matches its suffix
    Time complexity (Worst case) : O(K), where K is the length of the input string
    Space complexity:
        Input: O(K), where K is the length of the input string
        Aux: O(K), where K is the length of the input string
    """
    # initialize zarray to return
    return_zarray = [None] * len(input_string)  # O(n) space

    # initialize the zbox (left and right)
    # zbox_right is exclusive
    zbox_left, zbox_right = len(input_string) - 1, len(input_string) - 1

    # loop through the string
    i = len(input_string) - 1
    while i >= 0:

        if i == len(input_string) - 1:
            return_zarray[i] = len(input_string)

        elif i > zbox_left:  # if inbox

            # k is the ith mirror in the right box
            k = zbox_right - i + 1  # - zbox_right + 1  # + 1 since i is inclusive
            k = - k - 1

            # remaining
            remaining = i - zbox_left

            if return_zarray[k] < remaining:
                return_zarray[i] = return_zarray[k]

            elif return_zarray[k] > remaining:
                return_zarray[i] = remaining

            else:  # z[k] == remaining
                # explicit
                zbox_left, zbox_right, length = reverse_explicit_comparison(i, input_string)
                return_zarray[i] = length

        else:  # i >= zbox_right
            # explicit
            zbox_left, zbox_right, length = reverse_explicit_comparison(i, input_string)
            return_zarray[i] = length

        i -= 1
    return return_zarray


def reverse_explicit_comparison(i, input_string):
    """
    Description: perform explicit comparison to return the new z box's range and its length
    Written by: Kuah Jia Chen
    Input: i is an integer that indicates the starting position of the new z box and input_string is a string
    Return: return the range of new z box and its length
    Time complexity (Worst case) : O(K), where K is the length of the input string
    Space complexity:
        Input: O(K), where K is the length of the input string
        Aux: O(1)
    """
    zbox_left, zbox_right, index = i, i, len(input_string) - 1
    while i >= 0 and input_string[zbox_left] == input_string[index]:
        i -= 1
        zbox_left = i
        index -= 1
    return zbox_left, zbox_right - 1, zbox_right - zbox_left


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


def writeOutput(occurrences):
    """
    Description: write the answer to the output file
    Written by: Kuah Jia Chen
    Input: occurrences is the answer for q1
    Return: None
    """
    # Open output file with correct name
    outputFile = open("output_q1.txt", "w")

    # if no matches
    if occurrences[0] == 0:
        outputFile.write(str(occurrences[0]))
    else:  # if there is a matches
        outputFile.write(str(occurrences[0]))

        outputFile.write("\n")

        matched_indices = occurrences[1]

        # the first element in the matched_indices list
        if len(matched_indices[0]) == 1:
            outputFile.write(str(matched_indices[0][0]))
        else:
            outputFile.write(str(matched_indices[0][0]) + " " + str(matched_indices[0][1]))

        for i in range(1, len(matched_indices)):
            outputFile.write("\n")
            if len(matched_indices[i]) == 1:
                outputFile.write(str(matched_indices[i][0]))
            else:
                outputFile.write(str(matched_indices[i][0]) + " " + str(matched_indices[i][1]))

    # close output file
    outputFile.close()


if __name__ == '__main__':
    # retrieve the file paths from the commandline arguments
    _, filename1, filename2 = sys.argv
    print("Number of arguments passed : ", len(sys.argv))
    # since we know the program takes two arguments
    print("First argument : ", filename1)
    print("Second argument : ", filename2)
    file1content = read_file(filename1)
    print("\nContent of first file : ", file1content)
    file2content = read_file(filename2)
    print("\nContent of second file : ", file2content)
    text = file1content[0]
    pat = file2content[0]
    ans = q1(pat, text)
    writeOutput(ans)
