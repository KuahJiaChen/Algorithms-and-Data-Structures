########################
#####  Question 1  #####
########################

def count_encounters(target_difficulty, monster_list):
    """
    Purpose: find the number of possible encounters there are which sum up to the value of target_difficulty
             based on the difficulty rating of each monster
    Argument: target_difficulty is a non-negative integer and monster_list is a list of tuples, where each tuple
              represents a single monster. The first element of each tuple is the monster's type name and the second
              element is monster's difficulty
    Return: an integer, where this integer represents the number of different sets of monster that their difficulties
            can be sum up to target_difficulty
    Complexity:
        - time complexity: O(DM), where D is the value of target_difficulty and M is the total length of monster_list
        - auxiliary space complexity: O(DM), where D is the value of target_difficulty and M is the total length of
                                             monster_list
    References: Referred to the lecture recording https://youtu.be/s7gpf0Q1i_8,
                tutorial recording https://youtu.be/ZD0sr5i_s9Y,
                https://stackoverflow.com/questions/28838791/dynamic-programing-to-generate-combinations
    """
    memo = []
    if target_difficulty == 0:
        # if target_difficulty is 0, there is only one encounter which is {} no matter what is the target_difficulty
        return 1
    if len(monster_list) == 0:
        # no monster in monster list, hence there is only no encounter no matter what is the target_difficulty
        return 0
    # initialize memo
    for i in range(len(monster_list)):
        sublist = []
        for j in range(target_difficulty + 1):
            sublist.append(0)
        memo.append(sublist)
    # initialize base case
    for k in range(len(monster_list)):
        memo[k][0] = 1  # base case
    for row in range(len(monster_list)):
        for col in range(1, target_difficulty + 1):
            # if it is not the first row
            if row >= 1:
                if monster_list[row][1] > col:
                    memo[row][col] = memo[row - 1][col]
                else:
                    memo[row][col] = memo[row][col - monster_list[row][1]] + memo[row - 1][col]
            # if it is the first row
            else:
                if monster_list[row][1] > col:
                    memo[row][col] = 0
                else:
                    memo[row][col] = memo[row][col - monster_list[row][1]]
    # return the number of possible combinations
    return memo[len(monster_list) - 1][target_difficulty]


########################
#####  Question 2  #####
########################

def best_lamp_allocation(num_p, num_l, probs):
    """
    Purpose: calculate the maximum probability that each plant will be ready by the day of the party by using
             a maximum number of lamps, num_l or lesser than that
    Argument: num_p is a positive integer which represents the number of plants, num_l is a positive integer which
              represents the number of lamps, probs is a list of lists, where probs[i][j] represents the probability
              for plant i to be ready by the day of party if j lamps is allocated to it. The values in probs are all
              between 0 to 1 inclusive
    Return: return a float number, which is the highest probability of all plants being read by the day of party by
            allocating the lamps to each plants in an optimal way
    Complexity:
        - time complexity: O(PL^2), where P is the value of num_p and L is the value of num_l
        - auxiliary space complexity: O(PL), where P is the value of num_p and L is the value of num_l
    References: Referred to the lecture recording https://youtu.be/s7gpf0Q1i_8,
    """
    memo = []
    # initialize memo
    for i in range(num_p + 1):
        sublist = []
        for j in range(num_l + 1):
            sublist.append(0)
        memo.append(sublist)
    # initialize base case
    for i in range(num_l + 1):
        memo[0][i] = 1
    for row in range(1, num_p + 1):
        for col in range(num_l + 1):
            current_max = 0
            for k in range(col + 1):
                balance = abs(col - k)
                if row > len(probs):  # no probability for plant i no matter how many lamp is allocated to it
                    current_prob = memo[row - 1][balance] * 0
                elif k >= len(probs[row - 1]):  # no probability for plant i - 1 when it is allocated with k lamps
                    current_prob = memo[row - 1][balance] * 0
                else:
                    current_prob = memo[row - 1][balance] * probs[row - 1][k]
                if current_prob > current_max:
                    current_max = current_prob
            memo[row][col] = current_max
    # return the highest probability by allocating the lamps in the optimal way
    return memo[num_p][num_l]
