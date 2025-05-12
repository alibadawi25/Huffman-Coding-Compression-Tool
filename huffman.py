import heapq
import customtkinter as ctk
import time


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
    popup = None
    tree = []
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)

        merged_freq = lo[0] + hi[0]
        merged_node = Node(None, merged_freq)
        merged_node.left = lo[1]
        merged_node.right = hi[1]
        tree.append(merged_node.left)
        tree.append(merged_node.right)
        tree.append(merged_node)
        print(f"{merged_freq}")
        print(
            f"|\n|_ {lo[1].freq} [{lo[1].char}]"
            if lo[1].char is not None
            else f"|\n|_ {lo[1].freq} <Node>"
        )
        print(
            f"|\n|_ {hi[1].freq} [{hi[1].char}]"
            if hi[1].char is not None
            else f"|\n|_ {hi[1].freq} <Node>"
        )
        print("\n------------------------------------------------------------")

        heapq.heappush(heap, [merged_freq, merged_node])

        if not popup:
            popup = draw_tree_popup(merged_node, popup, tree)
        else:
            draw_tree_popup(merged_node, popup, tree)

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


def create_canvas():
    pass


def draw_tree_popup(tree_root, old_popup, tree):
    popup = old_popup
    if not popup:
        popup = ctk.CTkToplevel()
        popup.title("Huffman Tree")
        popup.geometry("1000x700")
        popup.grab_set()

    canvas = ctk.CTkCanvas(popup, bg="white")
    canvas.place(relwidth=1, relheight=1)

    radius = 15
    x_spacing = 30
    y_spacing = 60
    positions = {}
    current_x = [0]

    # Step 1: Traverse and calculate positions
    def set_positions(node, depth=0):
        if node is None:
            return
        set_positions(node.left, depth + 1)
        x = current_x[0]
        y = depth * y_spacing
        positions[node] = (x * x_spacing + 50, y + 50)
        current_x[0] += 1
        set_positions(node.right, depth + 1)

    set_positions(tree_root)

    # def collect_tree(node):
    #     if node is None:
    #         return
    #     tree.append(node)
    #     collect_tree(node.left)
    #     collect_tree(node.right)

    # collect_tree(tree_root)

    # # Step 3: Sort by frequency (least to greatest)
    # tree.sort(key=lambda node: node.freq)

    # Step 4: Draw nodes
    timer = 0
    for node in tree:
        canvas.after(timer * 500, lambda n=node: draw_node(n))
        timer += 1

    def draw_node(node):
        x, y = positions[node]
        label = node.char if node.char is not None else f"{node.freq}"
        canvas.create_oval(
            x - radius, y - radius, x + radius, y + radius, fill="skyblue"
        )
        canvas.create_text(x, y, text=label)
        if node.left:
            x_left, y_left = positions[node.left]
            canvas.create_line(x, y + radius, x_left, y_left - radius)
        if node.right:
            x_right, y_right = positions[node.right]
            canvas.create_line(x, y + radius, x_right, y_right - radius)

    return popup
