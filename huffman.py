import heapq

class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def huffmanCoding(inputString):
    charFreq = {}
    for i in inputString:
        charFreq[i] = charFreq.get(i, 0) + 1

    heap = [[freq, Node(char, freq)] for char, freq in charFreq.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        tree = ""
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)

        merged_freq = lo[0] + hi[0]
        merged_node = Node(None, merged_freq)
        merged_node.left = lo[1]
        merged_node.right = hi[1]
        print(f"{merged_freq}")
        print(f"|\n|_ {lo[1].freq} [{lo[1].char}]" if lo[1].char is not None else f"|\n|_ {lo[1].freq} <Node>")
        print(f"|\n|_ {hi[1].freq} [{hi[1].char}]" if hi[1].char is not None else f"|\n|_ {hi[1].freq} <Node>")
        print("\n------------------------------------------------------------")

        heapq.heappush(heap, [merged_freq, merged_node])

    root = heap[0][1]

    huffmanCode = {}

    def generate_codes(node, current_code=""):
        if node is None:
            return
        if node.char is not None:
            huffmanCode[node.char] = current_code
        generate_codes(node.left, current_code + "0")
        generate_codes(node.right, current_code + "1")

    generate_codes(root)

    return huffmanCode, root


def huffmanDecoding(encodedStr, huffmanCode):
    reverse_huffman_code = {v: k for k, v in huffmanCode.items()}
    decodedStr = ""
    current_code = ""

    for bit in encodedStr:
        current_code += bit
        if current_code in reverse_huffman_code:
            decodedStr += reverse_huffman_code[current_code]
            current_code = ""

    return decodedStr
