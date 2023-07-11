########################
#####  Question 1  #####
########################


import math
import random
import sys


def mod_exp(base, exponent, n):
    """
    Description: Used to perform computation to determine the remainder when calculating the modulus of an exponential
                 expression
    Written by: Kuah Jia Chen
    Input: base is an integer, exponent is an integer, n is an integer
    Return: the remainder when calculating the modulus of the exponential expression
    Time complexity (Worst case): O(a), where a represents the number of bits present in the binary form of exponent
    Space complexity:
        Input: O(1)
        Aux: O(a), where a represents the number of bits present in the binary form of exponent
    """
    previous = base % n
    ans = previous if exponent % 2 == 1 else 1
    exponent //= 2
    while exponent > 0:
        current = (previous * previous) % n
        previous = current
        if exponent % 2 == 1:
            ans = (ans * current) % n
        exponent //= 2
    return ans


def miller_rabin(n, k):
    """
    Description: Implements a probabilistic primality testing algorithm, which aids in evaluating the
                 likelihood of a given number being prime or composite.
    Written by: Kuah Jia Chen
    Input: n is an integer, k is an integer
    Return: True if n is a prime, else False
    Time complexity (Worst case): O(k * log(n)), where k is the number of tests to check and n is the input integer
    Space complexity:
        Input: O(1)
        Aux: O(1)
    """

    # check if the left most bit is one, if not, then n is an even number, then n is not a prime number
    if not n & 1 == 1:
        return False

    # if n is 2 or 3, then n is a prime number
    if n == 2 or n == 3:
        return True

    s, t = 0, n - 1
    # while t is an even number by using bit operator
    while not t & 1 == 1:
        s += 1
        t //= 2

    for _ in range(k):

        a = random.randint(2, n - 2)

        previous = mod_exp(a, t, n)

        for j in range(1, s + 1):

            # calculate the current
            current = (previous * previous) % n

            # if mod_exp(a, j, n) is congruent to 1 and mod_exp(a, j-1, n) is not congruent to 1 and
            # mod_exp(a, j-1, n) is not congruent to 1
            if current == 1 and previous != 1 and previous != n - 1:
                return False

            # once current == 1, for all the future iteration from j to s, the current will remain as 1, thus it is
            # redundant to continue the loop. Hence, we can just break
            elif current == 1:
                break

            # update the previous
            previous = current

        # if mod_exp(a, n-1, n) is not congruent to 1
        if current != 1:
            return False
    return True


def find_k(n):
    """
    Description: Return the value of int(math.log(n)) + 1
    Written by: Kuah Jia Chen
    Input: n is an integer
    Return: int(math.log(n)) + 1
    Time complexity (Worst case): O(1)
    Space complexity:
        Input: O(1)
        Aux: O(1)
    """
    return int(math.log(n)) + 1


def gcd(a, b):
    """
    Description: Calculates and returns the greatest common divisor (GCD) of two given numbers.
    Written by: Kuah Jia Chen
    Input: a is an integer, b is an integer
    Return: the gcd of a and b
    Time complexity (Worst case): O(log(min(a,b))), where a and b are the input values
    Space complexity:
        Input: O(1)
        Aux: O(1)
    """
    while b != 0:
        a, b = b, a % b
    return a


def my_key_gen(d):
    """
    Description: The purpose of this function is to generate two prime numbers, which are the smallest primes of the
                 form 2^x - 1, where x is equal to or greater than a specified value d. These prime numbers are used
                 to generate the values n and a randomly chosen e.
    Written by: Kuah Jia Chen
    Input: d is an integer
    Return: the two primes p and q, the product of p and q (which is n), and the exponent e
    Time complexity (Worst case): O(k * log(2^x)): where k is the number of tests and x is the power of the primes
    Space complexity:
        Input: O(1)
        Aux: O(1)
    """

    ans = []

    # based on the observation from Mersenne prime, I realized that the number with the form of
    # 2^d - 1 will only be prime if and only if the d is an odd number. As a result, if the input d
    # is an even number, I will + 1 to make sure it is an odd number. After that, inside the while loop
    # I will perform power_of_two <<= 2 for each iteration (i.e., power_of_two *= 4, which is also equivalent
    # to perform d += 2 in each iteration)

    if d % 2 == 0:
        d += 1

    power_of_two = 2 ** d

    # find the two prime numbers p and q
    while len(ans) < 2:

        # calculate the value in 2^x - 1 form
        current = power_of_two - 1

        # calculate the number of tests to perform in miller rabin
        k = find_k(current)

        # if it is prime, then append to the list
        if miller_rabin(current, k):
            ans.append(current)

        # equivalent to multiplies the number stores in power_of_two variable by 2 using bit shift
        power_of_two <<= 2

    # assign the values in list to p and q
    p, q = ans[0], ans[1]

    # calculate the modulus
    modulus = p * q

    # calculate the lambda value
    lambda_value = ((p - 1) * (q - 1)) // gcd(p - 1, q - 1)

    # find the exponent value
    exponent = None

    while exponent is None:
        current_value = random.randint(3, lambda_value - 1)

        # only assign current value to exponent if gcd(current_value, lambda_value) == 1
        if gcd(current_value, lambda_value) == 1:
            exponent = current_value

    return p, q, modulus, exponent


def write_output(ans):
    """
    Description: write the answer to the output file
    Written by: Kuah Jia Chen
    Input: the value of p, q, modulus and exponent
    Return: None
    """
    p, q, modulus, exponent = ans
    # Open output file with correct name
    output_file_1 = open("publickeyinfo.txt", "w")
    # write results to an output file
    output_file_1.write("# modulus (n)")
    output_file_1.write("\n")
    output_file_1.write(str(modulus))
    output_file_1.write("\n")
    output_file_1.write("# exponent (e)")
    output_file_1.write("\n")
    output_file_1.write(str(exponent))
    # Close output file
    output_file_1.close()

    # Open output file with correct name
    output_file_2 = open("secretprimes.txt", "w")
    # write results to an output file
    output_file_2.write("# p")
    output_file_2.write("\n")
    output_file_2.write(str(p))
    output_file_2.write("\n")
    output_file_2.write("# q")
    output_file_2.write("\n")
    output_file_2.write(str(q))
    # Close output file
    output_file_2.close()


if __name__ == '__main__':
    # retrieve the file paths from the commandline arguments
    _, d = sys.argv
    print("Number of arguments passed : ", len(sys.argv))
    # since we know the program takes one argument
    print("First argument : ", d)
    write_output(my_key_gen(int(d)))
