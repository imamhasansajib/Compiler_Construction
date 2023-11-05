# Remove comments from c file
import os
import re

inputfile = input("Enter file name: ")
if os.path.exists(inputfile):
    with open(inputfile, 'r') as inputfile:
        data = inputfile.read()
        data = re.sub(r'//.*', '', data)
        data = re.sub(r'/\*(.*?)\*/', '', data, flags=re.DOTALL)
    with open('output.txt', 'w') as outputfile:
        outputfile.write(data)
else:
    print("File does not exists!")
