# Copy c file to another file
import os.path

filename = input("Enter c file name: ")

if os.path.exists(filename):
    file1 = open(filename, "r")
    data = file1.read()
    file1.close()

    file2 = open("1609_output.txt", "w")
    file2.write(data)
    file2.close()
else:
    print("File does not exist!")



