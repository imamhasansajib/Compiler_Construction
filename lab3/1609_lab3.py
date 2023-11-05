#Count the number of keywords
import re
from collections import Counter
import os
def count_keywords(file):
    pattern = r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while)\b'
    matches = re.findall(pattern, file)
    return matches

file = input("Enter file name: ")
if os.path.exists(file):
    with open(file, 'r') as inputfile:
        data = inputfile.read()
        data = re.sub(r'(/\*.*?\*/)|//.*', '', data)
        data = re.sub(r'".*?"', '', data)
    keyword_count = Counter(count_keywords(data))
    for keyword, count in keyword_count.items():
        print(f"{keyword} : {count}")
else:
    print("File does not exist!")