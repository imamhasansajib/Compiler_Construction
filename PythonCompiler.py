import re
from collections import Counter
import os

def count_keywords(file):
    with open(file, 'r') as inputfile:
        data = inputfile.read()
        data = re.sub(r'(/\*.*?\*/)|//.*', '', data)
        data = re.sub(r'".*?"', '', data)
        data = re.sub(r'/\*(.*?)\*/', '', data, flags=re.DOTALL)

    with open('output_PythonCompiler.txt', 'w') as outputfile:
        outputfile.write(data)

    pattern = r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while)\b'
    matches = re.findall(pattern, data)

    keyword_count = Counter(matches)
    print(f"Keywords found are: ")
    for keyword, count in keyword_count.items():
        print(f"{keyword} : {count}")


def detect_identifier(filename):
    identifiers = set()
    keyword_pattern = r'\b(int|float|double|char|void)\b'
    identifier_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'

    with open(filename, 'r') as file:
        for line in file:
            line = re.sub(r"\".*?\"|'.*?'", "", line)  # Remove string literals
            line = re.sub(r"\/\/.*|\/*[\s\S]*?\*\/", "", line)  # Remove comments
            keywords = re.findall(keyword_pattern, line)
            for keyword in keywords:
                statements = re.findall(rf'{keyword}(.*?)(?:;|\()', line)
                for statement in statements:
                    identifiers.update(re.findall(identifier_pattern, statement))

    total_identifiers = len(identifiers)
    print(f"\nTotal identifiers: {total_identifiers}")
    print(f"Identifiers found are: ")
    for identifier in identifiers:
        print(identifier)

file = input("Enter file name: ")
if os.path.exists(file):
    count_keywords(file)
    detect_identifier(file)
else:
    print("File does not exist!")