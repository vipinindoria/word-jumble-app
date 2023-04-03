import argparse
from itertools import product


class IOUtils:
    """
    Utility class for I/O operations
    """
    def __init__(self, args):
        """
        Constructor
        :param args:
        """
        self.args = args

    def read_from_file(self):
        """
        Reads the input file and returns the startWord, endWord and list of dictionary words
        :return: startWord: String,
                 endWord: String,
                 list of dictionary words: List of Strings
        """
        begin_word = self.args.inputfile.readline().split("=")[1].strip().strip('"').strip("'")
        end_word = self.args.inputfile.readline().split("=")[1].strip().strip('"').strip("'")
        dict_list = self.args.inputfile.readline().split("=")[1].strip().split(",")
        dict_list = [word.strip().strip('"').strip("'") for word in dict_list]
        args.inputfile.close()
        return begin_word, end_word, dict_list

    def write_to_file(self, sts_length, st):
        """
        Writes the output to the output file
        :param sts_length: Integer, length of the shortest path
        :param st: String, shortest path
        :return: None
        """
        output_file = self.args.outputfile if args.outputfile else args.inputfile.name.replace('input', 'output')
        with open(output_file, 'w') as f:
            f.write(f'Length of shortest  transformation sequence : {sts_length}\n')
            f.write(f'The shortest transformation is: {st}\n')
        f.close()


class HashTable:
    """
    Hash table class
    """
    def __init__(self, size):
        """
        Constructor
        :param size: Integer, size of the hash table
        """
        self.size = size
        self.table = [[] for _ in range(size)]

    def hash(self, key):
        """
        Hashing function
        :param key: String, key to be hashed
        :return: Integer, Hash value
        """
        return sum(ord(c) for c in key) % self.size

    def insert(self, key, value):
        """
        Inserts the key-value pair in the hash table
        :param key: String, key to be inserted
        :param value: String, value to be inserted
        :return: List of tuples, list of key-value pairs
        """
        index = self.hash(key)
        if self.table[index] is not None:
            for kvp in self.table[index]:
                if kvp[0] == key:
                    if value not in kvp[1]:
                        kvp[1].append(value)
                    break
            else:
                self.table[index].append([key, [value]])
        else:
            self.table[index].append((key, [value]))

    def get(self, key):
        """
        Returns the value corresponding to the key
        :param key: String, key to be searched
        :return: Any, value corresponding to the key
        """
        index = self.hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        return None

    def __getitem__(self, key):
        """
        Returns the value corresponding to the key
        :param key: String, key to be searched
        :return: Value corresponding to the key
        """
        return self.get(key)

    def __setitem__(self, key, value):
        """
        Inserts the key-value pair in the hash table
        :param key: key to be inserted
        :param value: value to be inserted
        :return: key-value pair
        """
        self.insert(key, value)


class GraphUtils:
    """
    Graph utility class
    """
    def __init__(self, vertices):
        """
        Constructor
        :param vertices: List, list of vertices
        """
        self.buckets = HashTable(10)
        self.graph = HashTable(10)
        self.vertices = vertices

    def build_graph(self):
        """
        Builds the graph
        :return: graph
        """
        for vertex in self.vertices:
            init = False
            for i in range(len(vertex)):
                bucket1 = '{}_{}'.format(vertex[:i], vertex[i:])
                bucket2 = '{}_{}'.format(vertex[:i], vertex[i + 1:])
                self.buckets.insert(bucket1, vertex)
                self.buckets.insert(bucket2, vertex)
                if not init:
                    self.buckets.insert(f"_{vertex}", vertex)
                    self.buckets.insert(f"{vertex}_", vertex)
                    init = True

        for table_row in self.buckets.table:
            for elm in table_row:
                mutual_neighbors = elm[1]
                for vertex1, vertex2 in product(mutual_neighbors, repeat=2):
                    if vertex1 != vertex2:
                        self.graph.insert(vertex1, vertex2)
                        self.graph.insert(vertex2, vertex1)
        return self.graph


class ShortestTransformationSequence:
    """
    Shortest Transformation Sequence class
    """
    def __init__(self, s, t, words):
        """
        Constructor
        :param s: starting word
        :param t: ending word
        :param words: list of words
        """
        self.s = s
        self.t = t
        self.words = words

    def get_shortest_transformation_sequence(self, graph):
        """
        Returns the shortest transformation sequence
        :param graph: graph
        :return: vertex, vertex sequence
        """
        visited = set()
        queue = [[self.s]]
        while queue:
            path = queue.pop(0)
            vertex = path[-1]
            yield vertex, path
            if graph.get(vertex) is not None:
                for neighbor in set(graph.get(vertex)) - visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])

    def solve(self):
        """
        Creates the graph and finds the shortest transformation sequence using Breadth First Search
        :return: no of transformations, vertex sequence
        """
        if self.s == self.t:
            return 0, "Start and end words are same."

        self.words.append(self.s)
        graph = GraphUtils(self.words).build_graph()
        for vertex, path in self.get_shortest_transformation_sequence(graph):
            if vertex == self.t:
                return len(path), ' -> '.join(path)
        return -1, "No transformation sequence found."


if __name__ == '__main__':
    """
    Driver code
    """
    # Get Arguments
    parser = argparse.ArgumentParser(description="Application to Find the Shortest Transformation Sequence"
                                                 " to Reach a Target String from Source String.")
    parser.add_argument('-i', '--inputfile', type=argparse.FileType('r'), help='Input File Path', required=True)
    parser.add_argument('-o', '--outputfile', type=argparse.FileType('w'), help='Output File Path')
    args = parser.parse_args()

    # Read Input
    io_obj = IOUtils(args)
    begin_word, end_word, dict_list = io_obj.read_from_file()

    # Solve
    sts_length, st = ShortestTransformationSequence(begin_word, end_word, dict_list).solve()

    # Write Output
    io_obj.write_to_file(sts_length, st)
