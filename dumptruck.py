import tkinter as tk

import sys

window = tk.Tk()
window.title("Dump Truck")

if len(sys.argv) <= 1:
    print("usage: dumptruck [filename]")
    exit()

if sys.argv[1][-6:len(sys.argv[1])+6] != ".class":
    print("Please use .class files")
    exit()
    
textFrame = tk.Frame()
buttonFrame = tk.Frame()

file = open(sys.argv[1], "rb")
file = file.read()

text_box = tk.Text()
text_box.pack()

stack = []

for i in range(0, len(file)):
    hexValue = hex(file[len(file)-i-1])[2:4]
    if len(hexValue) == 1:
        hexValue = "0" + hexValue
    stack.append(hexValue)

text_box.insert(tk.END, "Magic Number: " + stack.pop() + stack.pop() + stack.pop() + stack.pop()+ "\n")
text_box.insert(tk.END, "Minor Version: " + stack.pop() + stack.pop() + "\n")
text_box.insert(tk.END, "Major Version: " + stack.pop() + stack.pop() + "\n")
constant_pool_count = stack.pop() + stack.pop()
text_box.insert(tk.END, "Constant Pool Count: " + constant_pool_count + "\n")

constant_pool = {
    1: "Utf8",
    3: "Integer",
    4: "Float",
    5: "Long",
    6: "Double",
    7: "Class",
    8: "String",
    9: "Fieldref",
    10: "Methodref",
    11: "InterfaceMethodref",
    12: "NameAndType",
    15: "MethodHandle",
    16: "MethodType",
    18: "InvokeDynamic"
}

constant_pool_args = {
    1: [2],
    3: [4],
    4: [4],
    5: [4, 4],
    6: [4, 4],
    7: [2],
    8: [2],
    9: [2, 2],
    10: [2, 2],
    11: [2, 2],
    12: [2, 2],
    15: [1, 2],
    16: [2],
    18: [2, 2]
}

for i in range(0, int("0x" + constant_pool_count, 16)-1):
    constant_pool_arg = int("0x" + stack.pop(), 16)
    for value in constant_pool_args:
        text_box.insert(tk.END, "#" + str(i) + "    " + constant_pool[constant_pool_arg]+"\n")
    
    
window.mainloop()
