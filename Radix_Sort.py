# import necessary libraries
import timeit
import random
import matplotlib.pyplot as plt
import math


########################
#####  Question 1  #####
########################

def num_rad_sort(nums, b):
    """
    Purpose: sort the nums list that contains a list of integer into ascending numerical order according to the base (b)
            and return the sorted list
    Argument: nums is an unsorted list that contains a list of non-negative integers, b is an integer that is >= 2 which
              actually represent the base
    Return: a sorted nums list in ascending numerical order
    Complexity:
        - time complexity: O((n+b)*log(b)M), where n is the number of elements in nums, b is the value of b which
                           indicate the base and M is the numerical value of the maximum elements in nums
        - auxiliary space complexity: O(n+b), where n is the number of elements in nums and b is the value of b which
                                      indicate the base
    References: Referred to the lecture recording https://youtu.be/Zw5IxI_ccGY
    """
    # if nums list does not contain any elements, it is already sorted, so just return it
    if len(nums) == 0:
        return nums
    # find the maximum
    max_item = nums[0]
    for item in nums:
        if item > max_item:
            max_item = item
    # find the number of column/digit in order to determine how many times sort_counting_stable function should be call
    col = 0
    while max_item > 0:
        max_item //= b
        col += 1
    # call counting sort col times
    for i in range(col):
        nums = sort_counting_stable(nums, b, i)
    return nums


def sort_counting_stable(nums, b, col):
    """
    Purpose: sort the nums list according to the (col)th digit (after converting to base b) in each element in nums list
    Argument: nums is an unsorted list that contains a list of non-negative integers, b is an integer that is >= 2 which
              actually represent the base and col is an integer that is >= 0 which indicates which digit the function
              should sort the nums list.
    Return: a list that is sorted based on the (col)th digit (after converting to base b) in each element in nums list
    Complexity:
        - time complexity: O(n+b), where n is the number of elements in nums and b is the value of b which indicate the
                           base
        - auxiliary space complexity: O(n+b), where n is the number of elements in nums and b is the value of b which
                                      indicate the base
    References: Referred to the lecture recording https://youtu.be/Ww0kYGWij58
    """
    # initialize count array with size b
    count_array = [None] * b
    for i in range(len(count_array)):
        count_array[i] = []
    # update count array, by inserting the elements into the specific position (based on their value at (col)th column)
    for item in nums:
        converted_item = (item // (b ** col)) % b
        count_array[converted_item].append(item)
    # update input list, by copying all the elements in count_array into input list in that order
    index = 0
    for i in range(len(count_array)):
        item = count_array[i]
        frequency = len(count_array[i])
        for j in range(frequency):
            nums[index] = item[j]
            index += 1
    return nums


########################
#####  Question 2  #####
########################


def base_timer(num_list, base_list):
    """
    Purpose: This function is use to help us to investigate the relationship between the base and the runtime
    Argument: num_list is a list that contains non-negative integers, base_list is a list that contains integers that
              is >=2 and it is sorted in ascending order
    Return: a list that contains number. In this list, the element at index i represents the time taken to run my
            num_rad_sort by passing num_list and the element at index i in base_list as arguments
    Complexity:
        - time complexity: O(a*(n+b)*log(b)M), where a is the number of elements in base_list, n is the number of
                           element in num_list, b is the largest element in base_list and M is the M is the numerical
                           value of the maximum elements in nums
        - auxiliary space complexity: O(n+b), where n is the number of elements in nums and b is the largest element in
                                      base_list
    """
    # create a new list that use to store the time taken to run my radix sort function from Task 1 with different b
    output_list = []
    for i in range(len(base_list)):
        starttime = timeit.default_timer()  # start the timer
        num_rad_sort(num_list, base_list[i])
        endtime = timeit.default_timer()  # end the timer
        time = (endtime - starttime)  # find the time taken by subtracting endtime from starttime
        output_list.append(time)  # append the result to the output_list
    return output_list


########################
#####  Question 3  #####
########################


def interest_groups(data):
    """
    Purpose: Group people's name with the exactly the same interests into a list and sort each list in ascending
             alphabetical order.
    Argument: data is a list, where each of the element in data is a tuple with 2 elements. The first element in the
              tuple is the people's name and the second element is the interest list. The first element in the tuple
              should be a non-empty string of lowercase a-z with no spaces or punctuation, whereas the second element
              contains a number of strings that represent the person's interest and each of the string consists of
              lowercase a-z and also spaces but no other characters.
    Return: a list that contains sublist(s), and for each distinct set of liked things, there would be a sublist(s) that
            contains all the people's name who like exactly those things, and for each sublist, the name are sorted in
            ascending alphabetical order.
    Complexity:
        - time complexity: O(NM), where N is the number of elements in data, M os the maximum number of characters
                           among all sets of liked things.
        - auxiliary space complexity: O(N+X), where N is the number of elements in data and X is the total elements
                                      in all the list that belongs to the second element in all tuples.
                            For example, data = [("a",["birds","napping"]),("b",["birds"]),("c",["birds","napping"])]
                            X would be 5 since 2 elements in second element of first tuple, 1 element in second element
                            of second tuple, 2 element in second element of third tuple, hence 2 + 1 + 2 = 5
    """
    # if there is no element in data, just return data
    if len(data) == 0:
        return data
    # sort each sublist by calling the str_rad_sort function as the helper function
    for i in range(len(data)):
        sorted_list = str_rad_sort(data[i][1])
        # copy all the elements from sorted_list into the original interest list
        for j in range(len(data[i][1])):
            data[i][1][j] = sorted_list[j]
    # sort all the tuples in data so that similar elements would be placed together
    # first, convert all the elements in the interest list to a single string and append it to a new list
    # and continue doing this for all tuples
    interest_list = []
    for k in range(len(data)):
        item = data[k][1]
        item = "$".join(item)  # $ as separator
        interest_list.append(item)
    # next, use the helper function to sort the tuples while sorting the interest_list, since I am now sorting the
    # tuples, I would call tup_rad_sort function
    data = tup_rad_sort(data, interest_list)
    # now tuples are sorted, I would then group people with similar interest together into output list with O(N)
    output_list = []
    for a in range(len(data)):
        if a == 0:  # if data[a] is the first element in data, create an empty list with the person's name
            new_list = [data[a][0]]
            output_list.append(new_list)
        elif data[a][1] == data[a - 1][1]:  # if the person's interest is same as the previous element, put the person
            # name together with the previous person name in the same sublist
            output_list[len(output_list) - 1].append(data[a][0])
        else:
            new_list = [data[a][0]]  # else, create a new sublist and append it to the output_list
            output_list.append(new_list)
    # now, output_list should be a list of lists and each list in the output_list would contains all the names of the
    # people who like exactly those things, but the names still not yet sorted in ascending alphabetical order
    # hence, I sort the names within each sublist alphabetical order using the helper function
    for m in range(len(output_list)):
        sorted_name = str_rad_sort(output_list[m])
        for n in range(len(output_list[m])):
            output_list[m][n] = sorted_name[n]
    return output_list


def str_rad_sort(str_list):
    """
    Purpose: sort the str_list so that all the elements in str_list should be in ascending alphabetical order
    Argument: str_list is a list that contains strings
    Return: a sorted str_list such that all the elements in str_list are in ascending alphabetical order
    Complexity:
        - time complexity: O(BM), where B is the number of elements in str_list and M is the maximum length of strings
                           among all the elements in the str_list
        - auxiliary space complexity: O(B), where B is the number of elements in str_list
    References: Referred to the lecture recording https://youtu.be/Zw5IxI_ccGY
    """
    # if the list is empty, it is already sorted
    if len(str_list) == 0:
        return str_list
    # find the maximum length among the elements in str_list and the value indicates the number of columns
    col = len(str_list[0])
    for i in range(len(str_list)):
        if len(str_list[i]) > col:
            col = len(str_list[i])
    # call counting_sort_string for col times ( in order to let this function to sort the elements in ascending
    # alphabetical order, I purposely assign j to col and decrement by 1 after each iteration, in other words, elements
    # would sort from their right most character to the left most character , thus they could be sort in ascending
    # alphabetical order )
    for j in range(col, -1, -1):
        str_list = counting_sort_string(str_list, j)
    return str_list


def tup_rad_sort(data, interest_list):
    """
    Purpose: sort the tuples in the data such that people with the exact same interest would now be next to each
             other ( ascending alphabetical order is not necessary )
    Argument: data is a list that contains tuples as elements, col is an integer that >= 0, and interest_list is a
              list of strings
    Return: a sorted data such that all the elements with the exact same interest would now be next to each other
    Complexity:
        - time complexity: O(NM), where N is the number of elements in data and M is the maximum length of strings
                           among all the elements in the interest_list ( It is important to know that the length of data
                           and the length of interest_list would be exactly the same (due to my implementation in
                            interest_groups function))
        - auxiliary space complexity: O(N), where N is the number of elements in interest_list
    References: Referred to the lecture recording https://youtu.be/Zw5IxI_ccGY
        """
    # if the list is empty, it is already sorted
    if len(data) == 0 and len(interest_list) == 0:
        return []
    # find the maximum length among the elements in str_list and the value indicates the number of columns
    col = len(interest_list[0])
    for i in range(len(interest_list)):
        if len(interest_list[i]) > col:
            col = len(interest_list[i])
    # call counting_sort_string for col times ( since the purpose of this function is not to sort the tuples in
    # ascending alphabetical order (just want to make sure similar items are now next to each other), I could just
    # simply assign j initially to be 0 (unlike str_rad_sort) )
    for j in range(col):
        data, interest_list = counting_sort_tuple(data, j, interest_list)
    return data


def counting_sort_string(str_list, col):
    """
    Purpose: Sort the strings in str_list in ascending alphabetical order according to their character at (col)th column
    Argument: str_list is a list that contains strings, and col is an integer that >= 0
    Return: a sorted list that sort in ascending alphabetical order according to their character at (col)th column
    Complexity:
        - time complexity: O(B), where B is the number of elements in str_list
        - auxiliary space complexity: O(B), where B is the number of elements in the str_list
    Referred to the lecture recording https://youtu.be/Ww0kYGWij58
    """
    # initialize count array
    count_array = [None] * 26
    for i in range(len(count_array)):
        count_array[i] = []
    # update count array
    for j in range(len(str_list)):
        if len(str_list[j]) <= col or str_list[j][col] == " ":
            count_array[0].append(str_list[j])
        else:
            item = str_list[j][col]
            item = ord(item) - 97
            count_array[item].append(str_list[j])
    # update input list
    index = 0
    for k in range(len(count_array)):
        sublist = count_array[k]
        frequency = len(count_array[k])
        for m in range(frequency):
            str_list[index] = sublist[m]
            index += 1
    return str_list


def counting_sort_tuple(data, col, interest_list):
    """
    Purpose: Sort the tuples in data in ascending alphabetical order according to character at (col)th column
             in interest_list. Besides that, it is important to know that the element with index i in interest_list
             is corresponding to the element with index i in data, hence, this function would sort the two list
    Argument: data is a list that contains tuples as elements, col is an integer that >= 0, and interest_list is a list
              of strings
    Return: a sorted data list where all the tuples are sorted in ascending alphabetical order according to the
            character at (col)th column for each element in interest_list
    Complexity:
        - time complexity: O(N), where N is the number of elements in interest_list ( It is important to know that the
                           length of data and the length of interest_list would be exactly the same (due to my
                           implementation in interest_groups function))
        - auxiliary space complexity: O(N), where N is the number of elements in the interest_list
    Referred to the lecture recording https://youtu.be/Ww0kYGWij58
    """
    # initialize count array
    count_array = [None] * (26 + 1)
    for i in range(len(count_array)):
        count_array[i] = []
    # update the count array
    for i in range(len(interest_list)):
        if len(interest_list[i]) <= col or interest_list[i][col] == " ":
            count_array[0].append((data[i], interest_list[i]))
        elif interest_list[i][col] == "$":
            count_array[26].append((data[i], interest_list[i]))
        else:
            item = interest_list[i][col]
            item = ord(item) - 97
            count_array[item].append((data[i], interest_list[i]))
    # update the data
    index = 0
    for j in range(len(count_array)):
        sublist = count_array[j]
        frequency = len(count_array[j])
        for k in range(frequency):
            data[index] = sublist[k][0]
            index += 1
    # update the interest_list
    index1 = 0
    for m in range(len(count_array)):
        sublist = count_array[m]
        frequency = len(count_array[m])
        for n in range(frequency):
            interest_list[index1] = sublist[n][1]
            index1 += 1
    return data, interest_list


if __name__ == '__main__':
    """
    random.seed("FIT2004S22021")
    data1 = [random.randint(0, 2 ** 25) for _ in range(2 ** 15)]
    data2 = [random.randint(0, 2 ** 25) for _ in range(2 ** 16)]
    bases1 = [2 ** i for i in range(1, 23)]
    bases2 = [2 * 10 ** 6 + (5 * 10 ** 5) * i for i in range(1, 10)]
    y1 = base_timer(data1, bases1)
    y2 = base_timer(data2, bases1)
    y3 = base_timer(data1, bases2)
    y4 = base_timer(data2, bases2)
    
    plt.xscale('log')
    plt.plot(bases1, y1, label="line for y1")
    plt.plot(bases1, y2, label="line for y2")
    plt.xlabel("Bases (x-axis in logarithmic scale)")
    plt.ylabel("Runtimes")
    plt.title("Graph 1")
    plt.legend()
    plt.show()
    
    plt.xscale('linear')
    plt.plot(bases2, y3, label="line for y3")
    plt.plot(bases2, y4, label="line for y4")
    plt.xlabel("Bases (x-axis in linear scale)")
    plt.ylabel("Runtimes")
    plt.title("Graph 2")
    plt.legend()
    plt.show()
    """
