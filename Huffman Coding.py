import sys
import heapq


class BinaryTreeNode(object):

    def __init__(self, value=None, frequency=None, left=None, right=None, bit=0):
        self.value = value
        self.frequency = frequency
        self.left = left
        self.right = right
        self.bit = bit

    def get_frequency(self):
        return self.frequency

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def set_left(self, left):
        self.left = left

    def set_right(self, right):
        self.right = right

    def get_left(self):
        return self.left

    def get_right(self):
        return self.right

    def has_left(self):
        return self.left is not None

    def has_right(self):
        return self.right is not None

    def set_bit(self):
        self.bit = 1

    def get_bit(self):
        return self.bit


class BinaryTree:

    def __init__(self):
        self.root = BinaryTreeNode()

    def get_root(self):
        return self.root

    def set_root(self, value):
        self.root = value


def get_frequencies(string):    # <-- 1 loop through the input string, O(n). Inserts and checks in a dict are O(1)
    frequencies = dict()
    dictionary_length = 0
    for character in string:

        if character in frequencies:
            frequencies[character] += 1
        else:
            frequencies[character] = 1
            dictionary_length += 1

    return frequencies


def generate_heap(string):

    frequencies = get_frequencies(string)
    priority_queue = []

    entry_count = 0
    for item in frequencies:
        node = BinaryTreeNode(value=item, frequency=frequencies[item])
        heap_entry = [node.frequency, entry_count, node]
        heapq.heappush(priority_queue, heap_entry)
        entry_count += 1

    return priority_queue, entry_count


def build_huffman_tree(string):

    heap = generate_heap(string)     # <-- this is in the form (priority_queue, entry_count)

    priority_queue = heap[0]    # <--[frequency, entry_count, node]
    num_entries = heap[1]    # <-- this will the entry_count (ie. the total number of entries in the queue)
    entry_count = heap[1]    # <-- same as num_entries, but will increment whilst num_entries will decrease
    huffman_tree = BinaryTree()

    if num_entries == 1:    # <-- deal with the edge case that the input string contains 1 or only 1 repeated character
        node = BinaryTreeNode(value=priority_queue[0][0])
        node.set_left(priority_queue[0][2])
        huffman_tree.set_root(value=node)

    else:
        while num_entries > 1:

            # pop the 2 smallest nodes (by frequency) to be merged to create a tree
            smallest = heapq.heappop(priority_queue)
            next_smallest = heapq.heappop(priority_queue)
            sum_frequencies = smallest[0] + next_smallest[0]     # <-- value of root node of the tree

            new_node = BinaryTreeNode(value=sum_frequencies)
            new_node.set_left(smallest[2])
            new_node.set_right(next_smallest[2])
            new_node.get_right().set_bit()

            huffman_tree.set_root(new_node)

            heap_entry = [sum_frequencies, entry_count, new_node]

            heapq.heappush(priority_queue, heap_entry)

            num_entries -= 1
            entry_count += 1

    return huffman_tree


def huffman_encoding(data):

    def dfs_in_order(tree):
        character_codes = dict()

        def traverse(node, code):
            if node:
                # traverse left subtree
                traverse(node.get_left(), code + "0")

                # visit node
                if node.get_frequency():#
                    character_codes[node.get_value()] = code[1:]

                # traverse right sub-tree
                traverse(node.get_right(), code + "1")

        traverse(tree.get_root(), str(tree.get_root().get_bit()))

        return character_codes


    huffman_tree = build_huffman_tree(str(data))
    character_codes = dfs_in_order(huffman_tree)
    huffman_code = ""

    for character in data:
        huffman_code = huffman_code + character_codes[character]

    return huffman_code, huffman_tree

def huffman_decoding(data,tree):

    decoded_string = ""
    node = tree.get_root()

    for bit in data:

        if bit == "1":
            node = node.get_right()
        else:
            node = node.get_left()

        if not node.has_left() and not node.get_right():
            decoded_string = decoded_string + node.get_value()
            node = tree.get_root()

    return decoded_string

def huffman_coding(a_great_sentence):

    if a_great_sentence== "":
        raise ValueError("The input cannot be an empty string")

    print("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
    print("The content of the data is: {}\n".format(a_great_sentence))

    encoded_data, tree = huffman_encoding(str(a_great_sentence))

    print("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print("The content of the decoded data is: {}\n".format(decoded_data))
    print(f"Input is equal to output: {str(a_great_sentence) == decoded_data}")

    return

if __name__ == "__main__":

    # string = str(input("Enter string to be encoded:" )) <-- use this line and the one below to enter custom inputs
    # huffman_coding(string)

    # Test Case 1
    string1 = " " # <-- raise ValueError: Input cannot be an empty string
    huffman_coding(string1)

    # Test Case 2
    string2 = "a"
    huffman_coding(string2)

    # Test Case 3
    string3 = "aaaa"
    huffman_coding(string3)

    # Test Case 4
    string4 = "abcd ef. Hello, my name is: John Smith"
    huffman_coding(string4)

    # Test Case 5
    string5 = 5.0 # <-- fine because the non-string is converted into a string using str()
    huffman_coding(string5)

    # Test Case 6
    string2 = " " #<-- no issues since the string is not empty
    huffman_coding(string2)






