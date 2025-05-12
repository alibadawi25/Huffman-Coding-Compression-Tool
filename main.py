import customtkinter as ctk
from tkinter import filedialog
from huffman import huffmanCoding, huffmanDecoding, Node
import os
import time

def encode_file_popup():
    encoding_window = ctk.CTkToplevel(window)
    encoding_window.title("Encode File")
    encoding_window.geometry("420x200")
    encoding_window.grab_set()

    ctk.CTkLabel(encoding_window, text="Selected file to encode:").pack(pady=(10, 5))

    path_entry = ctk.CTkEntry(encoding_window, width=380)
    path_entry.pack(pady=5)

    status_label = None
    output_label = None
    output_textbox = None
    draw_button = None
    tree = None

    def browse_file():
        file_path = filedialog.askopenfilename(
            title="Select a file",
            initialdir=".",
            filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            path_entry.delete(0, "end")
            path_entry.insert(0, file_path)

    def confirm_and_encode():
        nonlocal output_label, output_textbox, status_label, draw_button, tree

        file_path = path_entry.get()
        if os.path.exists(file_path):
            tree, binStr = encode_file(file_path)
            if output_label:
                output_label.destroy()
            if output_textbox:
                output_textbox.destroy()
            if status_label:
                status_label.destroy()
            if draw_button:
                draw_button.destroy()
            output_label = ctk.CTkLabel(encoding_window, text="Encoded Output:")
            output_label.pack()
            encoding_window.geometry("420x400")

            output_textbox = ctk.CTkTextbox(encoding_window, width=380, height=100)
            output_textbox.pack(pady=5)
            output_textbox.configure(state="normal")
            output_textbox.delete(1.0, "end")
            output_textbox.insert("end", binStr)
            output_textbox.configure(state="disabled")
            status_label = ctk.CTkLabel(encoding_window, text="✅ Encoding completed!", text_color="green")
            status_label.pack(pady=(5, 0))

            draw_button = ctk.CTkButton(encoding_window, text="Show Tree", command=lambda: draw_tree_popup(tree))
            draw_button.pack(pady=10)
        else:
            if status_label:
                status_label.destroy()
            status_label = ctk.CTkLabel(encoding_window, text="❌ Invalid file path.", text_color="red")
            status_label.pack(pady=(5, 0))

    ctk.CTkButton(encoding_window, text="Browse File", command=browse_file).pack(pady=5)
    ctk.CTkButton(encoding_window, text="Encode", command=confirm_and_encode).pack(pady=10)


def encode_file(file_path):
    if file_path:
        with open(file_path, "r") as file:
            file_content = file.read()

        huffmanCode, tree = huffmanCoding(file_content)
        binStr = "".join(huffmanCode[i] for i in file_content)

        binary_file_path = os.path.splitext(file_path)[0] + ".bin"
        with open(binary_file_path, "wb") as bin_file:
            bin_file.write(int(binStr, 2).to_bytes((len(binStr) + 7) // 8, byteorder='big'))

        huffman_dict_file = os.path.splitext(file_path)[0] + "_huffman_dict.txt"
        with open(huffman_dict_file, "w") as dict_file:
            for char, code in huffmanCode.items():
                dict_file.write(f"{char}: {code}\n")
        return tree, binStr




def decode_file_popup():
    decoding_window = ctk.CTkToplevel(window)
    decoding_window.title("Decode File")
    decoding_window.geometry("520x480")
    decoding_window.grab_set()

    output_label = None
    output_textbox = None
    status_label = None

    ctk.CTkLabel(decoding_window, text="Selected file to decode:").pack(pady=(10, 5))

    bin_path_entry = ctk.CTkEntry(decoding_window, width=380)
    bin_path_entry.pack(pady=5)

    def browse_bin_file():
        file_path = filedialog.askopenfilename(
            title="Select a file",
            initialdir=".",
            filetypes=[("Bin Files", "*.bin")]
        )
        if file_path:
            bin_path_entry.delete(0, "end")
            bin_path_entry.insert(0, file_path)

    ctk.CTkButton(decoding_window, text="Browse Binary File", command=browse_bin_file).pack(pady=5)

    ctk.CTkLabel(decoding_window, text="Selected dictionary file to decode upon:").pack(pady=(10, 5))

    dict_path_entry = ctk.CTkEntry(decoding_window, width=380)
    dict_path_entry.pack(pady=5)

    def browse_dict_file():
        file_path = filedialog.askopenfilename(
            title="Select a file",
            initialdir=".",
            filetypes=[("Text Files", "*dict.txt")]
        )
        if file_path:
            dict_path_entry.delete(0, "end")
            dict_path_entry.insert(0, file_path)

    ctk.CTkButton(decoding_window, text="Browse Dictionary Text File", command=browse_dict_file).pack(pady=5)

    def confirm_and_decode():
        nonlocal output_label, output_textbox, status_label

        bin_file_path = bin_path_entry.get()
        dict_file_path = dict_path_entry.get()

        if os.path.exists(bin_file_path) and os.path.exists(dict_file_path):
            decoded_string = decode_file(bin_file_path, dict_file_path)
            if decoded_string:
                if output_label:
                    output_label.destroy()
                if output_textbox:
                    output_textbox.destroy()
                if status_label:
                    status_label.destroy()

                output_label = ctk.CTkLabel(decoding_window, text="Decoded Output:")
                output_label.pack()

                output_textbox = ctk.CTkTextbox(decoding_window, width=380, height=100)
                output_textbox.pack(pady=5)
                output_textbox.configure(state="normal")
                output_textbox.delete(1.0, "end")
                output_textbox.insert("end", decoded_string)
                output_textbox.configure(state="disabled")

                status_label = ctk.CTkLabel(decoding_window, text="✅ Decoding completed!", text_color="green")
                status_label.pack(pady=(5, 0))
        else:
            if status_label:
                status_label.destroy()
            status_label = ctk.CTkLabel(decoding_window, text="❌ Invalid file path.", text_color="red")
            status_label.pack(pady=(5, 0))

    ctk.CTkButton(decoding_window, text="Decode", command=confirm_and_decode).pack(pady=20)


def decode_file(bin_file_path, dict_file_path):
    if bin_file_path and dict_file_path:
        with open(bin_file_path, "rb") as file:
            bin_file_content = file.read()
            bit_string = ''.join(f'{byte:08b}' for byte in bin_file_content)

        with open(dict_file_path, "r") as file:
            dict_file_content = file.read()
        return huffmanDecoding(bit_string, parse_huffman_dict(dict_file_content))


def parse_huffman_dict(mapping_str):
    huffman_dict = {}
    lines = mapping_str.splitlines()
    for line in lines:
        if ": " in line:
            char, code = line.split(": ", 1)
            if char == "":
                if line.startswith(": "):
                    huffman_dict["\n"] = code
            elif char == " ":
                huffman_dict[" "] = code
            else:
                huffman_dict[char] = code
    return huffman_dict


def draw_tree_popup(tree_root):
    popup = ctk.CTkToplevel(window)
    popup.title("Huffman Tree")
    popup.geometry("1000x700")
    popup.grab_set()

    # Create a canvas inside the popup window without scrollbars
    canvas = ctk.CTkCanvas(popup, bg="white")
    canvas.pack(fill="both", expand=True)

    radius = 15
    x_spacing = 30
    y_spacing = 60
    positions = {}
    current_x = [0]  # mutable wrapper

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

    # Step 2: Draw nodes
    def draw_node(node):
        if node is None:
            return

        x, y = positions[node]
        label = node.char if node.char is not None else f"{node.freq}"
        canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="skyblue")
        canvas.create_text(x, y, text=label)
        if node.left:
            x_left, y_left = positions[node.left]
            canvas.create_line(x, y + radius, x_left, y_left - radius)
            draw_node(node.left)
        if node.right:
            x_right, y_right = positions[node.right]
            canvas.create_line(x, y + radius, x_right, y_right - radius)
            draw_node(node.right)

    draw_node(tree_root)



window = ctk.CTk()
window.title("Huffman Coding Compression Tool")
window.geometry("400x300")

ctk.CTkLabel(window, text="Choose whether to encode or decode!").pack(pady=20)

ctk.CTkButton(window, text="Encode File", command=encode_file_popup).pack(pady=10)
ctk.CTkButton(window, text="Decode File", command=decode_file_popup).pack(pady=10)

window.mainloop()
