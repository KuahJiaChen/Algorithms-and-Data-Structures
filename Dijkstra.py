import math
from ctypes import py_object
from typing import TypeVar, Generic
from typing import Generic


class WordGraph:
    def __init__(self, words):
        """
        Purpose: initialise the attributes of an instance of WordGraph and also represents all the words as a graph
        Argument: self is an instance of WordGraph, words is a list of strings
        Return: None
        Complexity:
            - time complexity: O(W^2 * M), where W is the number of strings in words and M is the length of the string
                               in words
            - auxiliary space complexity: O(W + E), where W is the number of strings in words and E is the number of
                                          edges created in this WordGraph
        References: Referred to the lecture recording https://youtu.be/XF4IRYeIdPU
        """
        self.n = len(words)  # self.n is the number of words exists in the WordGraph
        self.no_of_edges = 0

        # initialize the array to store vertices for weighted
        # however, this array also could be use for question 1 as the vertex instance in the array still tells which
        # vertex has an edge to this particular edges
        self.vertices_weighted = [None] * self.n
        for i in range(len(words)):
            # use the index of array as id
            self.vertices_weighted[i] = Vertex(words[i])

        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                if self.one_word_difference(words[i], words[j]):
                    self.no_of_edges += 1
                    weight = self.find_alphabetic_distance(words[i], words[j])
                    current_edge = Edge(i, j, weight)
                    current_vertex = self.vertices_weighted[i]
                    current_vertex.add_edges(current_edge)

                    current_edge = Edge(j, i, weight)
                    current_vertex = self.vertices_weighted[j]
                    current_vertex.add_edges(current_edge)

    def find_alphabetic_distance(self, str1, str2):
        """
        Purpose: find the alphabetic distance between two strings
        Argument: self is an instance of WordGraph, str1 and str2 are strings with the same length
        Return: the alphabetic distance between two strings
        Complexity:
            - time complexity: O(M), where M is the length of the str1
            - auxiliary space complexity: O(1)
        """
        distance = 0
        for i in range(len(str1)):
            distance += abs(ord(str1[i]) - ord(str2[i]))
        return distance

    def one_word_difference(self, str1, str2):
        """
        Purpose: check if str1 and str2 only have one word difference
        Argument: self is an instance of WordGraph, str1 and str2 are strings with the same length
        Return: return True is there is only one word difference between str1 and str2, else False
        Complexity:
            - time complexity: O(M), where M is the length of the str1
            - auxiliary space complexity: O(1)
        """
        count = 0
        for i in range(len(str1)):
            if str1[i] != str2[i]:
                count += 1
        return count == 1

    def best_start_word(self, target_words):
        """
        Purpose: find the start word for which finding word ladders to all the target in a most easy way
        Argument: self is an instance of WordGraph, target_words is a list of indices of words in the WordGraph
        Return: return an integer that indicates the index of the word in the WordGraph which able to produce the
                overall shortest word ladders to reach all the words mentioned in target_words, if there is no such word
                exists, then it would return -1
        Complexity:
            - time complexity: O(W^3), where W is the number of words in the instance of WordGraph
            - auxiliary space complexity: O(W^2), where W is the number of words in the instance of WordGraph
        """
        matrix = [None] * self.n
        for i in range(self.n):
            matrix[i] = [math.inf] * self.n

        # initialize the diagonal
        for i in range(self.n):
            matrix[i][i] = 0

        for i in range(self.n):
            current_vertex_edges = self.vertices_weighted[i].edges
            for edge in current_vertex_edges:
                # since for this question, the graph is unweighted, hence each edge has a weight of 1
                matrix[edge.u][edge.v] = 1

        for k in range(self.n):
            for i in range(self.n):
                for j in range(self.n):
                    matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])

        ans = -1
        current_min = math.inf
        for i in range(self.n):
            sublist = []
            for j in range(len(target_words)):
                sublist.append(matrix[i][target_words[j]])
            current = max(sublist)
            if current < current_min:
                current_min = current
                ans = i

        return ans

    def dijkstra(self, source):
        """
        Purpose: find the shortest path to reach all the vertices in WordGraph from the source
        Argument: self is an instance of WordGraph, source is an integer that represents the index of vertex
        Return: this function would return two list, the element with index i in the first list represents the shortest
                distance to reach this vertex. The element with index i in the second list represents the index of
                previous vertex to reach this current vertex (i.e., which vertex is used to reach this current vertex)
        Complexity:
            - time complexity: O(D log W + W log W), where D is the number of pairs of words in WordGraph that only have
                               one word difference and W is the number of words in the instance of WordGraph
            - auxiliary space complexity: O(D + W), where D is the number of pairs of words in WordGraph that only have
                                          one word difference and W is the number of words in the instance of WordGraph
        References: Referred to the lecture recording https://youtu.be/XF4IRYeIdPU
        """
        # reset all the attributes of the vertex before performing the following dijkstra algorithm
        self.reset()

        # create MinHeap with size D where D is the number of edges
        discovered = MinHeap(self.no_of_edges)
        discovered.add((source, 0))
        source = self.vertices_weighted[source]
        source.distance = 0

        while len(discovered) > 0:
            u = discovered.get_min()  # the overall time complexity for this line of code would be O(D * log (W^2)),
            # however, it could write as O(D * 2 * log(W), hence it is also O(D log W)
            index_previous = u[0]
            u = self.vertices_weighted[u[0]]  # vertex

            # the following piece of code would only execute for maximum of W times due to the if condition
            if not u.visited:  # if it is visited, not need to check anymore
                u.visited = True
                for edge in u.edges:
                    index = edge.v  # the index of vertex v
                    v = self.vertices_weighted[index]  # vertex
                    if not v.visited:
                        if not v.discovered:  # v.discovered == False
                            v.discovered = True
                            v.distance = u.distance + edge.w
                            v.previous = index_previous
                            discovered.add((index, v.distance))
                        else:
                            if v.distance > u.distance + edge.w:
                                v.distance = u.distance + edge.w
                                v.previous = index_previous
                                discovered.add((index, v.distance))
                                v.discovered = True

        # element with index i in lst would contain the distance to reach vertex i from the source
        lst = []
        for i in range(self.n):
            lst.append(self.vertices_weighted[i].distance)

        # element with index i in lst2 would contain the previous vertex to reach vertex i
        lst2 = []
        for i in range(self.n):
            lst2.append(self.vertices_weighted[i].previous)
        return lst, lst2

    def constrained_ladder(self, start, target, constraint_words):
        """
        Purpose: find the word ladder that would minimise the alphabetic distance and used one of a set of particular
                 words in constraint_word
        Argument: self is an instance of WordGraph, start and target are indices of vertices. start is the index of the
                  word where the word ladder would start and target is the index of the word where the word ladder would
                  end, constraint_words is a list of indices, at least one of the word in constraint_words must appear
                  in the word ladder
        Return: return a list of indices of vertices that is in order corresponding to the words representing the word
                ladder where it would starts with start, ends with end and it would contain at least one of the word
                in constraint_words and has the minimum alphabetic distance out of the all possible word ladder
        Complexity:
            - time complexity: O(D log W + W log W), where D is the number of pairs of words in WordGraph that only have
                               one word difference and W is the number of words in the instance of WordGraph
            - auxiliary space complexity: O(D + W), where D is the number of pairs of words in WordGraph that only have
                                          one word difference and W is the number of words in the instance of WordGraph
        References: Referred to the tutorial recording https://youtu.be/ZA0Parhv34I
        """
        distance_from_start, path_to_start = self.dijkstra(start)
        distance_from_target, path_to_target = self.dijkstra(target)
        index = -1
        min = math.inf
        for i in range(len(constraint_words)):
            if distance_from_start[constraint_words[i]] + distance_from_target[constraint_words[i]] < min:
                min = distance_from_start[constraint_words[i]] + distance_from_target[constraint_words[i]]
                index = constraint_words[i]

        if index == -1:
            return None

        lst = []
        current = path_to_start[index]

        # the time complexity for this while loop would be O(W) as it would loop roughly W times in the worst case
        while current != start and current is not None:  # if current is not connected with any vertex
            lst.append(current)
            current = path_to_start[current]

        if current is not None:
            lst.append(current)

        lst2 = []
        current = path_to_target[index]

        # the time complexity for this while loop would be O(W) as it would loop roughly W times in the worst case
        while current != target and current is not None:
            lst2.append(current)
            current = path_to_target[current]

        if current is not None:
            lst2.append(current)

        ans = []

        for i in range(len(lst) - 1, -1, -1):
            ans.append(lst[i])

        ans.append(index)

        for i in range(len(lst2)):
            ans.append(lst2[i])

        return ans

    def reset(self):
        """
        Purpose: reset all the attributes of all the vertices in WordGraph
        Argument: self is an instance of WordGraph
        Return: None
        Complexity:
            - time complexity: O(W), where W is the number of words in the instance of WordGraph
            - auxiliary space complexity: O(1)
        References: Referred to the tutorial recording https://youtu.be/ZA0Parhv34I
        """
        for i in range(self.n):
            current_vertex = self.vertices_weighted[i]
            current_vertex.discovered = False
            current_vertex.visited = False
            current_vertex.previous = None
            current_vertex.distance = math.inf


class Vertex:
    def __init__(self, vertex_id):
        """
        Purpose: initialise the attributes of an instance of vertex
        Argument: self is an instance of Vertex, vertex_id could be anything that differentiate each other
        Return: None
        Complexity:
            - time complexity: O(1)
            - auxiliary space complexity: O(1)
        References: Referred to the lecture recording https://youtu.be/XF4IRYeIdPU
        """
        self.vertex_id = vertex_id
        self.edges = []
        self.discovered = False
        self.visited = False
        self.previous = None
        self.distance = math.inf

    def add_edges(self, edge):
        """
        Purpose: add the edge to the edges list for this vertex instance
        Argument: self is an instance of Vertex, edge is a tuple contains three integers, u ,v and w
        Return: None
        Complexity:
            - time complexity: O(1)
            - auxiliary space complexity: O(1)
        References: Referred to the lecture recording https://youtu.be/XF4IRYeIdPU
        """
        self.edges.append(edge)


class Edge:
    def __init__(self, u, v, w):
        """
        Purpose: initialise the attributes of an instance of edge
        Argument: self is an instance of Edge, u, v and w are integers
        Return: None
        Complexity:
            - time complexity: O(1)
            - auxiliary space complexity: O(1)
        References: Referred to the lecture recording https://youtu.be/XF4IRYeIdPU
        """
        self.u = u
        self.v = v
        self.w = w


T = TypeVar('T')


class ArrayR(Generic[T]):
    def __init__(self, length: int) -> None:
        """
        Purpose: creates an array of references to objects of the given length
        Argument: self is an instance of ArrayR, length is an integer that is greater than 0, length is the length of
                  array that need to be created
        Return: a sorted nums list in ascending numerical order
        Complexity:
            - time complexity: O(n), where n is the value of length
            - auxiliary space complexity: O(n), where n is the value of length
        References: Referred to the week 12 lecture code from FIT1008
        """
        if length <= 0:
            raise ValueError("Array length should be larger than 0.")
        self.array = (length * py_object)()  # initialises the space
        self.array[:] = [None for _ in range(length)]

    def __len__(self) -> int:
        """
        Purpose: returns the length of the array
        Argument: self is an instance of ArrayR
        Return: the length of the array
        Complexity:
            - time complexity: O(1)
            - auxiliary space complexity: O(1)
        References: Referred to the week 12 lecture code from FIT1008
        """
        return len(self.array)

    def __getitem__(self, index: int) -> T:
        """
        Purpose: returns the object in position index
        Argument: self is an instance of ArrayR, index is an integer that indicates the index of an element in the array
                  is in between 0 and length - self.array[] checks it
        Return: the object in position index
        Complexity:
            - time complexity: O(1)
            - auxiliary space complexity: O(1)
        References: Referred to the week 12 lecture code from FIT1008
        """
        return self.array[index]

    def __setitem__(self, index: int, value: T) -> None:
        """
        Purpose: sets the object in position index to value
        Argument: self is an instance of ArrayR, index is an integer that indicates the index of an element in the array
                  is in between 0 and length - self.array[] checks it, and value is the tuple that need to be added at index index
        Return: None
        Complexity:
            - time complexity: O(1)
            - auxiliary space complexity: O(1)
        References: Referred to the week 12 lecture code from FIT1008
        """
        self.array[index] = value


class MinHeap(Generic[T]):
    MIN_CAPACITY = 1

    def __init__(self, max_size: int) -> None:
        """
        Purpose: initialize an instance of MinHeap, setting it's length to 0 and create an array with size max_size
        Argument: self is an instance of MinHeap, max_size is an integer that indicates the size of MinHeap
        Return: None
        Complexity:
            - time complexity: O(n), where n is the value of max_size
            - auxiliary space complexity: O(n), where n is the value of max_size
        References: Referred to the week 12 lecture code from FIT1008
        """
        self.length = 0
        self.the_array = ArrayR(max(self.MIN_CAPACITY, max_size) + 1)

    def __len__(self) -> int:
        """
        Purpose: returns the number of elements contain in the MinHeap
        Argument: self is an instance of MinHeap
        Return: the number of elements contain in the MinHeap
        Complexity:
            - time complexity: O(1)
            - auxiliary space complexity: O(1)
        References: Referred to the week 12 lecture code from FIT1008
        """
        return self.length

    def is_full(self) -> bool:
        """
        Purpose: check if the MinHeap is full
        Argument: self is an instance of MinHeap
        Return: True if the array for MinHeap is full, else False
        Complexity:
            - time complexity: O(1)
            - auxiliary space complexity: O(1)
        References: Referred to the week 12 lecture code from FIT1008
        """
        return self.length + 1 == len(self.the_array)

    def rise(self, k: int) -> None:
        """
        Purpose: rise element at index k to its correct position
        Argument: self is an instance of MinHeap, k is an integer that indicates the index of a element in array and
                  1 <= k <= self.length // 2
        Return: None
        Complexity:
            - time complexity: O(log n), where n is the number of elements in the MinHeap
            - auxiliary space complexity: O(log n), where n is the number of elements in the MinHeap
        References: Referred to the week 12 lecture code from FIT1008
        """
        item = self.the_array[k]
        while k > 1 and item[1] < self.the_array[k // 2][1]:
            self.the_array[k] = self.the_array[k // 2]
            k = k // 2
        self.the_array[k] = item

    def add(self, element: T) -> bool:
        """
        Purpose: add the element into MinHeap, and call the rise function to swap this element to the correct position
        Argument: self is an instance of MinHeap, element is the a tuple, where the first element is the index of vertex
                  in WordGraph and second element is an integer that indicates the distance to reach this vertex
        Return: None
        Complexity:
            - time complexity: O(log n), where n is the number of elements in the MinHeap
            - auxiliary space complexity: O(log n), where n is the number of elements in the MinHeap
        References: Referred to the week 12 lecture code from FIT1008
        """
        if self.is_full():
            raise IndexError

        self.length += 1
        self.the_array[self.length] = element
        self.rise(self.length)

    def get_min(self):
        """
        Purpose: removes the minimum element from the heap, returning it
        Argument: self is an instance of MinHeap
        Return: the element with minimum integer in the tuple with index 1
        Complexity:
            - time complexity: O(log n), where n is the number of elements in the MinHeap
            - auxiliary space complexity: O(log n), where n is the number of elements in the MinHeap
        References: Referred to the week 12 lecture code from FIT1008
        """
        if self.length == 0:
            raise IndexError
        min_elt = self.the_array[1]
        self.length -= 1
        if self.length > 0:
            self.the_array[1] = self.the_array[self.length + 1]
            self.sink(1)
        return min_elt

    def smallest_child(self, k: int) -> int:
        """
        Purpose: returns the index of the minimum child of k
        Argument: self is an instance of MinHeap, k is an integer that indicates the index of a element in array and
                  1 <= k <= self.length // 2
        Return: the child of k with minimum integer in the tuple with index 1
        Complexity:
            - time complexity: O(1)
            - auxiliary space complexity: O(1)
        References: Referred to the week 12 lecture code from FIT1008
        """
        if 2 * k == self.length or self.the_array[k * 2][1] < self.the_array[2 * k + 1][1]:
            return k * 2
        else:
            return 2 * k + 1

    def sink(self, k: int) -> None:
        """
        Purpose: make the element at index k sink to the correct position
        Argument: self is an instance of MinHeap, k is an integer that indicates the index of a element in array and
                  1 <= k <= self.length // 2
        Return: None
        Complexity:
            - time complexity: O(log n), where n is the number of elements in the MinHeap
            - auxiliary space complexity: O(log n), where n is the number of elements in the MinHeap
        References: Referred to the week 12 lecture code from FIT1008
        """
        item = self.the_array[k]
        while 2 * k <= self.length:
            smallchild = self.smallest_child(k)
            if self.the_array[smallchild][1] > item[1]:
                break
            self.the_array[k] = self.the_array[smallchild]
            k = smallchild
        self.the_array[k] = item


