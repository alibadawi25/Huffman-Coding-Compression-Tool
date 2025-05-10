import customtkinter as ctk
from tkinter import filedialog
from huffman import huffmanCoding, huffmanDecoding
import os


def encode_file_popup():
    encoding_window = ctk.CTkToplevel(window)
    encoding_window.title("Encode File")
    encoding_window.geometry("420x200")
    encoding_window.grab_set()

    ctk.CTkLabel(encoding_window, text="Selected file to encode:").pack(pady=(10, 5))

    path_entry = ctk.CTkEntry(encoding_window, width=380)
    path_entry.pack(pady=5)

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
        file_path = path_entry.get()
        if os.path.exists(file_path):
            encode_file(file_path)
            ctk.CTkLabel(encoding_window, text="✅ Encoding completed!", text_color="green").pack(pady=(5, 0))
        else:
            ctk.CTkLabel(encoding_window, text="❌ Invalid file path.", text_color="red").pack(pady=(5, 0))

    browse_button = ctk.CTkButton(encoding_window, text="Browse File", command=browse_file)
    browse_button.pack(pady=5)

    confirm_button = ctk.CTkButton(encoding_window, text="Encode", command=confirm_and_encode)
    confirm_button.pack(pady=10)


def encode_file(file_path):
    if file_path:
        with open(file_path, "r") as file:
            file_content = file.read()  
        
        huffmanCode = huffmanCoding(file_content)
        print(huffmanCode)
        
        binStr = ""
        for i in file_content:
            binStr += huffmanCode[i]
        
        binary_file_path = os.path.splitext(file_path)[0] + ".bin"
        
        with open(binary_file_path, "wb") as bin_file:
            bin_file.write(int(binStr, 2).to_bytes((len(binStr) + 7) // 8, byteorder='big'))
        
        huffman_dict_file = os.path.splitext(file_path)[0] + "_huffman_dict.txt"
        with open(huffman_dict_file, "w") as dict_file:
            for char, code in huffmanCode.items():
                dict_file.write(f"{char}: {code}\n")


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

    browse_button = ctk.CTkButton(decoding_window, text="Browse Binary File", command=browse_bin_file)
    browse_button.pack(pady=5)

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

    browse_dict_button = ctk.CTkButton(decoding_window, text="Browse Dictionary Text File", command=browse_dict_file)
    browse_dict_button.pack(pady=5)

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

    confirm_button = ctk.CTkButton(decoding_window, text="Decode", command=confirm_and_decode)
    confirm_button.pack(pady=20)


def decode_file(bin_file_path, dict_file_path):
    if bin_file_path and dict_file_path:
        with open(bin_file_path, "rb") as file:
            bin_file_content = file.read()
            bit_string = ''.join(f'{byte:08b}' for byte in bin_file_content)

        with open(dict_file_path, "r") as file:
            dict_file_content = file.read() 
        return huffmanDecoding(bit_string,parse_huffman_dict(dict_file_content))

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



window = ctk.CTk()

window.title("Huffman Coding Compression Tool")
window.geometry("400x300")

label = ctk.CTkLabel(window, text="Select a file to encode!")
label.pack(pady=20)

upload_button = ctk.CTkButton(window, text="Encode File", command=encode_file_popup)
upload_button.pack(pady=10)

decode_button = ctk.CTkButton(window, text="Decode File", command=decode_file_popup)
decode_button.pack(pady=10)

window.mainloop()
