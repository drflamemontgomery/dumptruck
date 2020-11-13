import tkinter as tk
import re
import sys

window = tk.Tk()
window.title("Dump Truck")

if len(sys.argv) <= 1:
    print("usage: dumptruck [filename]")
    exit()

if sys.argv[1][-6:] != ".class":
    print("Please use .class files")
    exit()
   
textFrame = tk.Frame()
buttonFrame = tk.Frame()

file = open(sys.argv[1], "rb")
file = file.read()

text_box = tk.Text(textFrame)
text_box.configure(height=26, width=82)
text_box.pack(expand=True)
textFrame.pack(expand=True)

save_button = tk.Button(buttonFrame, text="Save")
save_button.pack()

buttonFrame.pack(expand=False)
def dissemble():
    stack = []

    for i in range(0, len(file)):

        hexValue = 0
        if type(file[0]) == int:
            hexValue = hex(file[-(i+1)])[2:4]
            if len(hexValue) == 1:
                hexValue = "0" + hexValue
        elif type(file[0]) == str:
            hexValue = hex(file[-(i+1)])[2:4]
            if len(hexValue) == 1:
                hexValue = "0" + hexValue
        stack.append(hexValue)

    text_box.insert(tk.END, "Magic Number: " + stack.pop() + stack.pop() + stack.pop() + stack.pop()+ "\n")
    text_box.insert(tk.END, "Minor Version: " + str(int("0x" + stack.pop() + stack.pop(), 16)) + "\n")
    text_box.insert(tk.END, "Major Version: " + str(int("0x" + stack.pop() + stack.pop(), 16)) + "\n")
    
    constant_pool_count = str(int("0x" + stack.pop() + stack.pop(), 16))
    #text_box.insert(tk.END, "Constant Pool Count: " + constant_pool_count + "\n")
    text_box.insert(tk.END, "#START_CONSTANT_POOL" + "\n")

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
        18: "InvokeDynamic",
        19: "Module",
        20: "Package"
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
        18: [2, 2],
        19: [2],
        20: [2]
    }

    #i_plus = 0;
    i = 1
    while(i < int(constant_pool_count)):
    #for i in range(1, int(constant_pool_count)):
        constant_pool_arg = int("0x" + stack.pop(), 16)

        #i += i_plus

        #Utf8
        if constant_pool_arg == 1:
            length = int("0x" + stack.pop() + stack.pop(), 16)
            #print(length)
            printString = '"'
            for char in range(0, length):
                printString += chr(int("0x" + stack.pop(), 16))
            printString += '"'

            text_box.insert(tk.END, "#" + str(i) + "    " + constant_pool[constant_pool_arg] + "    " + printString + "\n")

            #Integer of Float
        elif constant_pool_arg == 3 or constant_pool_arg == 4:
            printString = ''
            for value in range(0, 4):
                printString += str(stack.pop())
            printString = str(int("0x" + printString, 16))
            text_box.insert(tk.END, "#" + str(i) + "    " + constant_pool[constant_pool_arg] + "    " + printString + "\n")

            #Long or Double
        elif constant_pool_arg == 5 or constant_pool_arg == 6:

            printString = ""

            for value in range(0, 4):
                printString += str(stack.pop())
            printString = str(int("0x" + printString, 16))
            printString += "."

            tempString = ""
        
            for value in range(0, 4):
                tempString += str(stack.pop())
            printString += str(int("0x" + tempString, 16))
            text_box.insert(tk.END, "#" + str(i) + "    " + constant_pool[constant_pool_arg] + "    " + printString + "\n")


        #Class
        elif constant_pool_arg == 7 or constant_pool_arg == 8 or constant_pool_arg == 16 or constant_pool_arg == 19 or constant_pool_arg == 20:
            printString = ""

            for value in range(0, 2):
                printString += str(stack.pop())
            printString = "#" + str(int( "0x" + printString, 16))
            text_box.insert(tk.END, "#" + str(i) + "    " + constant_pool[constant_pool_arg] + "    " + printString + "\n")


        #Fieldref or Methodref or InterfaceMethodref
        elif constant_pool_arg == 9 or constant_pool_arg == 10 or constant_pool_arg == 11 or constant_pool_arg == 12 or constant_pool_arg == 18:
            printString = ""

            for value in range(0, 2):
                printString += str(stack.pop())
            printString = "#" + str(int("0x" + printString, 16))
            printString += "."

            tempString = ""
            for value in range(0, 2):
                tempString += str(stack.pop())
            printString += "#" + str(int("0x" + tempString, 16))
            text_box.insert(tk.END, "#" + str(i) + "    " + constant_pool[constant_pool_arg] + "    " + printString + "\n")

        #MethodHandle
        elif constant_pool_arg == 15:
            printString = str(int("0x" + stack.pop(), 16)) + ":"

            tempString = ""
            for value in range(0, 2):
                tempString += str(stack.pop())
            printString += "#" + str(int("0x" + tempString, 16))
            text_box.insert(tk.END, "#" + str(i) + "    " + constant_pool[constant_pool_arg] + "    " + printString + "\n")

    #Everything else
    #elif constant_pool_arg in constant_pool_args:
     #   text_box.insert(tk.END, "#" + str(i) + "    " + constant_pool[constant_pool_arg] + "\n")
      #  for value in constant_pool_args[constant_pool_arg]:
       #     for byte in range(value):
        #        stack.pop()
   
        if constant_pool_arg == 6:
            i += 1
        i += 1
    text_box.insert(tk.END, "#END_CONSTANT_POOL" + "\n")

def assemble(event):

    writeFile = open(sys.argv[1] + ".exported", "wb")
    
    stack = []
    magicNumber = text_box.get("1.0", "2.0")[-9:-1]
    stack.append(int("0x" + magicNumber[0:2], 16))
    stack.append(int("0x" + magicNumber[2:4], 16))
    stack.append(int("0x" + magicNumber[4:6], 16))
    stack.append(int("0x" + magicNumber[6:8], 16))

    minorVersion = int(re.sub("[^0-9]", "", text_box.get("2.0", "3.0")[-6:-1]))
    minorVersion = format(minorVersion, '04x')

    stack.append(int("0x" + minorVersion[0:2], 16))
    stack.append(int("0x" + minorVersion[2:4], 16))

    majorVersion = int(re.sub("[^0-9]", "", text_box.get("3.0", "4.0")[-6:-1]))
    majorVersion = format(majorVersion, '04x')

    stack.append(int("0x" + majorVersion[0:2], 16))
    stack.append(int("0x" + majorVersion[2:4], 16))

    cp_count = 1
    line = 5

    cp = []
    
    while True:
        value = text_box.get(str(line) + ".0", str((line+1)) + ".0")
        if value == "#END_CONSTANT_POOL\n":
            break
        if "Utf8" in value.split()[:2]:
            cp.append(1)
            utf8_string = ""
            for string in value.split('"')[1:-1]:
                utf8_string += string + '"'
            utf8_string = utf8_string[:-1]
            #print(utf8_string)
            utf8_length = format(len(utf8_string), '04x')
            cp.append(int("0x" + utf8_length[0:2], 16))
            cp.append(int("0x" + utf8_length[2:4], 16))
            
            for char in utf8_string:
                cp.append(ord(char))
        elif "Integer" in value.split()[:2]:
            cp.append(3)
            integer = format(int(value.split()[2]), '08x')

            cp.append(int("0x" + integer[0:2], 16))
            cp.append(int("0x" + integer[2:4], 16))
            cp.append(int("0x" + integer[4:6], 16))
            cp.append(int("0x" + integer[6:8], 16))
        elif "Float" in value.split()[:2]:
            cp.append(4)
            integer = format(int(value.split()[2]), '08x')

            cp.append(int("0x" + integer[0:2], 16))
            cp.append(int("0x" + integer[2:4], 16))
            cp.append(int("0x" + integer[4:6], 16))
            cp.append(int("0x" + integer[6:8], 16))
        elif "Long" in value.split()[:2]:
            cp.append(5)
            high_value = format(int(value.split()[2].split(".")[0]), '08x')
            low_value = format(int(value.split()[2].split(".")[1]), '08x')

            cp.append(int("0x" + high_value[0:2], 16))
            cp.append(int("0x" + high_value[2:4], 16))
            cp.append(int("0x" + high_value[4:6], 16))
            cp.append(int("0x" + high_value[6:8], 16))

            cp.append(int("0x" + low_value[0:2], 16))
            cp.append(int("0x" + low_value[2:4], 16))
            cp.append(int("0x" + low_value[4:6], 16))
            cp.append(int("0x" + low_value[6:8], 16))

            
        elif "Double" in value.split()[:2]:
            cp_count += 1
            
            cp.append(6)
            high_value = format(int(value.split()[2].split(".")[0]), '08x')
            low_value = format(int(value.split()[2].split(".")[1]), '08x')

            cp.append(int("0x" + high_value[0:2], 16))
            cp.append(int("0x" + high_value[2:4], 16))
            cp.append(int("0x" + high_value[4:6], 16))
            cp.append(int("0x" + high_value[6:8], 16))

            cp.append(int("0x" + low_value[0:2], 16))
            cp.append(int("0x" + low_value[2:4], 16))
            cp.append(int("0x" + low_value[4:6], 16))
            cp.append(int("0x" + low_value[6:8], 16))
        elif "Class" in value.split()[:2]:
            cp.append(7)

            name_index = format(int(value.split()[2][1:]), '04x')
            cp.append(int('0x' + name_index[0:2], 16))
            cp.append(int('0x' + name_index[2:4], 16))
        elif "String" in value.split()[:2]:
            cp.append(8)
            
            string_index = format(int(value.split()[2][1:]), '04x')
            cp.append(int('0x' + string_index[0:2], 16))
            cp.append(int('0x' + string_index[2:4], 16))
        elif "Fieldref" in value.split()[:2]:
            cp.append(9)

            class_index = format(int(value.split()[2].split(".")[0][1:]), '04x')
            name_index = format(int(value.split()[2].split(".")[1][1:]), '04x')

            cp.append(int('0x' + class_index[0:2], 16))
            cp.append(int('0x' + class_index[2:4], 16))

            cp.append(int('0x' + name_index[0:2], 16))
            cp.append(int('0x' + name_index[2:4], 16))
        elif "Methodref" in value.split()[:2]:
            cp.append(10)

            class_index = format(int(value.split()[2].split(".")[0][1:]), '04x')
            name_index = format(int(value.split()[2].split(".")[1][1:]), '04x')

            cp.append(int('0x' + class_index[0:2], 16))
            cp.append(int('0x' + class_index[2:4], 16))

            cp.append(int('0x' + name_index[0:2], 16))
            cp.append(int('0x' + name_index[2:4], 16))
        elif "InterfaceMethodref" in value.split()[:2]:
            cp.append(11)

            class_index = format(int(value.split()[2].split(".")[0][1:]), '04x')
            name_index = format(int(value.split()[2].split(".")[1][1:]), '04x')

            cp.append(int('0x' + class_index[0:2], 16))
            cp.append(int('0x' + class_index[2:4], 16))

            cp.append(int('0x' + name_index[0:2], 16))
            cp.append(int('0x' + name_index[2:4], 16))

        elif "NameAndType" in value.split()[:2]:
            cp.append(12)

            name_index = format(int(value.split()[2].split(".")[0][1:]), '04x')
            descriptor_index = format(int(value.split()[2].split(".")[1][1:]), '04x')

            cp.append(int('0x' + name_index[0:2], 16))
            cp.append(int('0x' + name_index[2:4], 16))

            cp.append(int('0x' + descriptor_index[0:2], 16))
            cp.append(int('0x' + descriptor_index[2:4], 16))
        elif "MethodHandle" in value.split()[:2]:
            cp.append(15)

            reference_kind = format(int(value.split()[2].split(":")[0]), '02x')
            reference_index = format(int(value.split()[2].split(":")[1][1:]), '04x')
            
            cp.append(int('0x' + reference_kind, 16))

            cp.append(int('0x' + reference_index[0:2], 16))
            cp.append(int('0x' + reference_index[2:4], 16))
        elif "MethodType" in value.split()[:2]:
            cp.append(16)

            descriptor_index = format(int(value.split()[2][1:]), '04x')
            cp.append(int('0x' + descriptor_index[0:2], 16))
            cp.append(int('0x' + descriptor_index[2:4], 16))
        elif "InvokeDynamic" in value.split()[:2]:
            cp.append(18)

            bootstrap_method_attr_index = format(int(value.split()[2].split(".")[0][1:]), '04x')
            name_and_type_index = format(int(value.split()[2].split(".")[1][1:]), '04x')

            cp.append(int('0x' + bootstrap_method_attr_index[0:2], 16))
            cp.append(int('0x' + bootstrap_method_attr_index[2:4], 16))

            cp.append(int('0x' + name_and_type_index[0:2], 16))
            cp.append(int('0x' + name_and_type_index[2:4], 16))
            
        line += 1
        cp_count += 1

    cp_count = format(cp_count, '04x')

    stack.append(int("0x" + cp_count[0:2], 16))
    stack.append(int("0x" + cp_count[2:4], 16))

    for value in cp:
        stack.append(value)
    
    print(cp_count)
    print(cp)
    
    writeFile.write(bytearray(stack))
    
dissemble()
save_button.bind("<Button-1>", assemble)

window.mainloop()
