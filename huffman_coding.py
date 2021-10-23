# Author: Karthik Reddy Pagilla

import sys
import heapq
import math

class Tree:
    def __init__(self, freq, letter=None, left=None, right=None):
        self.letter = letter
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def letter_freq_finder(file_name):
    freq_dict = {}
    with open(file_name, 'r') as f:
        for line in f:
            for letter in line:
                if letter in freq_dict:
                    freq_dict[letter] += 1
                else:
                    freq_dict[letter] = 1
    
    return freq_dict

def assign_encoding(tree_node, current_path, bit_value, output):
    if tree_node:
        current_path += bit_value

        if tree_node.left:
            assign_encoding(tree_node.left, current_path, '0', output)
        if tree_node.right:
            assign_encoding(tree_node.right, current_path, '1', output)

        if not tree_node.left and not tree_node.right:
            output.append((tree_node.letter, tree_node.freq, current_path))

if __name__ == "__main__":
    file_name = sys.argv[1]
    freq_dict = letter_freq_finder(file_name)

tree_heap = []
heapq.heapify(tree_heap)

for key in freq_dict:
    letter = key
    freq = freq_dict[key]
    tree_node = Tree(freq, letter)
    heapq.heappush(tree_heap, tree_node)

while len(tree_heap) > 1:
    left_child = heapq.heappop(tree_heap)
    right_child = heapq.heappop(tree_heap)
    combined_freq = left_child.freq + right_child.freq
    parent_node = Tree(combined_freq, left=left_child, right=right_child)
    heapq.heappush(tree_heap, parent_node)

total_letters = sum(freq_dict.values())

out1 = []
assign_encoding(heapq.heappop(tree_heap), '', '', out1)

out1.sort(key= lambda x: x[0])
avg_code_length = 0
alphabet = 0
total_bits = 0

print("{:>10}".format("Character") + "{:>20}".format("Codeword") + "{:>20}".format("Codeword"))
for i in out1:
    a, b, c = i
    f = "{0:.4f}".format((b/total_letters) * 100)
    avg_code_length += len(str(c)) * (b/total_letters)
    alphabet += 1
    total_bits += len(str(c)) * b
    print("{:>5}".format(str(a)) + "{:>25}".format(str(c)) + "{:>20}".format(str(f) + "%"))

print("ASCII Codeword length: " + str(8))

print("Block Length Encoding Codeword Length: " + str(math.ceil(math.log(alphabet, 2))))

print("Average Codeword Length: " + str(avg_code_length))

print("Original File Size (ASCII bits): " + str(total_letters * 8))

print("Original File Size (Block Length Encoding): " + str(total_letters * math.ceil(math.log(alphabet, 2))))

print("Estimated Encoding Size (bytes): " + str("{:.4f}".format((avg_code_length * total_letters)/8)))

print("Actual Encoding Size (bytes): " + str(total_bits))

print("---------------------------------------------------------------")

print("Compression Ratios")

block_length = math.ceil(math.log(alphabet, 2))
print("Average Codeword Length Compression: " + str("{:.4f}".format(((block_length - avg_code_length)/block_length) * 100)) + "%")

compression = (total_bits/(total_letters * 8)) * 100
print("File Compression Ratio: " + str("{:.4f}".format(compression)) + "%")