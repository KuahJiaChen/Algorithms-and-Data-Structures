########################
#####  Question 2  #####
########################

import sys


def q2(text, pattern):
    """
    Description:  find all exact occurrences of a pattern[1 . . . m] in any given text[1 . . . n],
                  however, the pattern pat[1 . . . m] can contain at most 1 wildcard character.
    Written by: Kuah Jia Chen
    Input: pattern is a string and text is a string
    Return: a list that contains the matched indices
    Time complexity (Worst case) : O(N / M) where N is the length of the text and M is the length of pattern
    Space complexity:
        Input: O(N + M), where N is the length of the text and M is the length of the pattern
        Aux: O(A + B + C + D), where A is the number of elements in bc_table, B is the number of elements in gs_array
             and C is the number of elements in mp_array, and D is the number of elements in the ans list that contain
             the number of matched indices
        """
    ans = []

    # return empty list of text is empty of pattern is empty of length of pattern is greater than length of text
    if not text or not pattern or len(pattern) > len(text):
        return []

    # preprocessing
    bc_table = bad_character_matrix(pattern)
    gs_array = good_suffix_array(pattern)
    mp_array = matched_prefix_array(pattern)

    # get the index of wildcard
    wildcard_index = None
    for i in range(len(pattern)):
        if pattern[i] == '.':
            wildcard_index = i
            break

    text_index = 0
    break_pointer, resume_pointer = 0, 0

    while text_index < len(text) - len(pattern) + 1:

        # pattern index start from the end of pattern
        pattern_index = len(pattern) - 1

        while pattern_index >= 0:

            if pattern_index == break_pointer:
                pattern_index = resume_pointer
                break_pointer, resume_pointer = -1, -1
            elif pattern[pattern_index] == '.' or text[text_index + pattern_index] == pattern[pattern_index]:
                pattern_index -= 1
            else:  # there is a mismatch character happen at pattern[pattern_index]
                break_pointer, resume_pointer = -1, -1
                break

        shift = 1

        # if there is a match
        if pattern_index < 0:
            ans.append(text_index)
            shift = len(pattern) - mp_array[1]

            # set the break pointer
            if wildcard_index is not None:
                break_pointer = wildcard_index
            else:
                break_pointer = mp_array[1] - 1

            # set the resume pointer
            if wildcard_index is not None:
                resume_pointer = wildcard_index - 1
            else:
                resume_pointer = 0

        # if there is a mismatch
        else:

            # check for bad character rule

            # get the number of shift to the wildcard if there is one before the mismatch character
            wildcard_shift = None
            if wildcard_index is not None and pattern_index > wildcard_index:
                wildcard_shift = pattern_index - wildcard_index

            # get the number of shift to the rightmost character that is same as the mismatch character if there is one
            mismatch_shift = None
            bc_char_array = bc_table[ord(text[text_index + pattern_index]) - 97]
            if bc_char_array is not None and bc_char_array[pattern_index] is not None:
                mismatch_shift = pattern_index - bc_char_array[pattern_index]

            # compare wildcard_shift and mismatch_shift to the get the optimal shift for bad character shift
            bc_num_shift = None
            shift_to_wildcard = False
            if wildcard_shift is not None and mismatch_shift is not None:
                # choose the smaller one as it is safer
                if wildcard_shift < mismatch_shift:
                    bc_num_shift = wildcard_shift
                    shift_to_wildcard = True  # this indicates that we had chosen to shift to dot
                else:
                    bc_num_shift = mismatch_shift
            elif wildcard_shift is not None:  # mismatch shift is None
                bc_num_shift = wildcard_shift
                shift_to_wildcard = True
            elif mismatch_shift is not None:
                bc_num_shift = mismatch_shift
            else:  # wildcard_shift is None and mismatch_shift is None, shift pattern_index + 1
                bc_num_shift = pattern_index + 1

            # get the number of shift for good suffix rule
            gs_num_shift = None
            select_gs_shift = False
            select_mp_shift = False
            gs_value = gs_array[pattern_index + 1]

            # if shift to wildcard, then assigned gs_num_shift to 0 so that we will only shift to wildcard
            if shift_to_wildcard:
                gs_num_shift = 0
            # gs[k + 1] > 0, which means there is substring in pattern matches the suffix
            elif gs_value is not None:
                if wildcard_shift is not None:
                    gs_num_shift = min(len(pattern) - gs_value - 1, wildcard_shift)
                    # print(gs_num_shift)
                else:
                    gs_num_shift = len(pattern) - gs_value - 1
                    select_gs_shift = True
            else:  # gs_value is None, which means gs[k + 1] == 0
                gs_num_shift = len(pattern) - mp_array[pattern_index]
                select_mp_shift = True

            # choose the optimal shift
            shift = max(bc_num_shift, gs_num_shift)

            # set the break and resume pointer for galil optimization
            if gs_num_shift > bc_num_shift:
                if select_gs_shift:

                    # set the break pointer
                    if wildcard_index is not None and (gs_num_shift >= pattern_index or pattern_index < wildcard_index):
                        break_pointer = wildcard_index
                    else:
                        break_pointer = gs_value

                    # set the resume pointer
                    if wildcard_index is not None and (gs_num_shift >= pattern_index or pattern_index < wildcard_index):
                        resume_pointer = wildcard_index - 1
                    else:
                        resume_pointer = break_pointer - len(pattern) + pattern_index + 1

                elif select_mp_shift:

                    # set the break pointer
                    if wildcard_index is not None:
                        break_pointer = wildcard_index
                    else:
                        break_pointer = mp_array[pattern_index + 1] - 1

                    # set the resume pointer
                    if wildcard_index is not None:
                        resume_pointer = wildcard_index - 1
                    else:
                        resume_pointer = 0

        text_index += shift

    return ans


def bad_character_matrix(pattern):
    """
    Description: create the bad character matrix that contains the elements that will help the boyer moore function
                 to find the right most occurrence of the mismatch character if there is one
    Written by: Kuah Jia Chen
    Input: pattern is a string
    Return: a list of list that contains the numbers to achieve bad character rule
    Time complexity (Worst case) : O(k * M), where k is the number of unique characters in pattern, and M is the length
                                   of pattern
    Space complexity:
        Input: O(M), where M is the length of the pattern
        Aux: O(k * M), where k is the number of unique characters in pattern, and M is the length of pattern
    """
    matrix = [None] * 26

    # right to left
    for i in range(len(pattern) - 1, -1, -1):
        current_char = pattern[i]

        if current_char == ".":
            continue

        current_index = ord(current_char) - 97

        if matrix[current_index] is None:
            matrix[current_index] = [None] * len(pattern)

        matrix[current_index][i] = i
        pointer = i
        while pointer < len(pattern) - 1 and matrix[current_index][pointer + 1] is None:
            matrix[current_index][pointer + 1] = i
            pointer += 1

    return matrix


def good_suffix_array(pattern):
    """
    Description: create the good suffix array that contains the elements that will help the boyer moore function
                 to find the optimal shift when there is a mismatch character
    Written by: Kuah Jia Chen
    Input: pattern is a string
    Return: a list that contains the good suffix values
    Time complexity (Worst case) : O(M), where M is the length of pattern
    Space complexity:
        Input: O(M), where M is the length of the pattern
        Aux: O(M), where M is the length of pattern
    """

    suffix_z_array = reverse_z_algorithm(pattern)  # O(M)
    m = len(pattern)
    good_suffix_array = [None] * (len(pattern) + 1)
    for p in range(len(suffix_z_array) - 1):  # O(M)
        j = m - suffix_z_array[p]
        # print(j,p)
        good_suffix_array[j] = p
    return good_suffix_array


def matched_prefix_array(pattern):
    """
    Description: create the matched prefix array that contains the elements that will help the boyer moore function
                 to find the optimal shift when there is a mismatch character
    Written by: Kuah Jia Chen
    Input: pattern is a string
    Return: a list that contains the matched prefix values
    Time complexity (Worst case) : O(M), where M is the length of pattern
    Space complexity:
        Input: O(M), where M is the length of the pattern
        Aux: O(M), where M is the length of pattern
    """
    z_array = z_algorithm(pattern)  # O(M)
    matched_prefix_array = [0] * (len(pattern) + 1)
    for i in range(len(z_array) - 1, -1, -1):  # O(M)
        if z_array[i] + i == len(pattern):
            matched_prefix_array[i] = z_array[i]
        else:
            # print(i)
            if i != len(z_array) - 1:
                matched_prefix_array[i] = matched_prefix_array[i + 1]
    return matched_prefix_array


def z_algorithm(string):
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
    return_zarray = [None] * len(string)  # O(n) space
    # initialize the zbox (left and right)
    # zbox_right is exclusive
    zbox_left, zbox_right = 0, 0

    # loop through the string
    i = 0
    while i < len(string):
        # i += 1
        # print(zbox_right)
        if i == 0:
            return_zarray[i] = len(string)
        elif i < zbox_right and string[i] != ".":  # if inbox
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
                zbox_left, zbox_right, length = explicit_comparison(i, string)
                return_zarray[i] = length
        else:  # i >= zbox_right
            # explicit
            zbox_left, zbox_right, length = explicit_comparison(i, string)
            return_zarray[i] = length
        # return_zarray = 5
        # remaining = 7 - 2 = 5
        # k = 1 , return_zarray[1] = 0
        i += 1
    return return_zarray


def explicit_comparison(i, string):
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
    wildcard_index = -1
    while i < len(string) and (string[zbox_right] == string[index] or string[zbox_right] == "."
                               or string[index] == "."):
        if string[zbox_right] == ".":
            wildcard_index = zbox_right
        i += 1
        zbox_right = i
        index += 1
    # print(zbox_left + 1, zbox_right , zbox_right - zbox_left)
    return zbox_left + 1, wildcard_index if wildcard_index != -1 else zbox_right, zbox_right - zbox_left


def reverse_z_algorithm(string):
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
    return_zarray = [None] * len(string)  # O(n) space
    # initialize the zbox (left and right)
    # zbox_right is exclusive
    zbox_left, zbox_right = len(string) - 1, len(string) - 1

    # loop through the string
    i = len(string) - 1
    while i >= 0:
        # i += 1
        # print(zbox_left)
        if i == len(string) - 1:
            return_zarray[i] = len(string)
        elif i > zbox_left and string[i] != ".":  # if inbox
            # k is the ith mirror in the left box
            k = zbox_right - i + 1  # - zbox_right + 1  # + 1 since i is inclusive
            k = - k - 1
            remaining = i - zbox_left
            if return_zarray[k] < remaining:
                return_zarray[i] = return_zarray[k]
            elif return_zarray[k] > remaining:
                return_zarray[i] = remaining
            else:  # z[k] == remaining
                # explicit
                zbox_left, zbox_right, length = reverse_explicit_comparison(i, string)
                return_zarray[i] = length
        else:  # i >= zbox_right
            zbox_left, zbox_right, length = reverse_explicit_comparison(i, string)
            return_zarray[i] = length
        i -= 1
    return return_zarray


def reverse_explicit_comparison(i, string):
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
    zbox_left, zbox_right, index = i, i, len(string) - 1
    wildcard_index = -1
    while i >= 0 and (string[zbox_left] == string[index] or string[zbox_left] == "."
                      or string[index] == "."):
        if string[zbox_left] == ".":
            wildcard_index = zbox_left
        i -= 1
        zbox_left = i
        index -= 1
    return wildcard_index if wildcard_index != -1 else zbox_left, zbox_right - 1, zbox_right - zbox_left


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
    Input: occurrences is the answer for q2
    Return: None
    """
    # open output file with correct name
    outputFile = open("output_q2.txt", "w")

    if len(occurrences) > 0:
        outputFile.write(str(occurrences[0] + 1))

    for i in range(1, len(occurrences)):
        outputFile.write("\n")
        outputFile.write(str(occurrences[i] + 1))

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
    ans = q2(text, pat)
    writeOutput(ans)
