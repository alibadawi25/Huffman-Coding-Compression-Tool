import customtkinter as ctk
from tkinter import filedialog
from huffman import huffmanCoding
import os

def encode_file():
    file_path = filedialog.askopenfilename(
        title="Select a file",
        initialdir=".",
        filetypes=[("Text Files", "*.txt")]
    )
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

window = ctk.CTk()

window.title("Huffman Coding Compression Tool")
window.geometry("400x300")

label = ctk.CTkLabel(window, text="Select a file to encode!")
label.pack(pady=20)

upload_button = ctk.CTkButton(window, text="Upload File", command=encode_file)
upload_button.pack(pady=10)

window.mainloop()
