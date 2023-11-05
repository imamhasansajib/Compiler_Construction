import os
import re

def count_keywords(file_name):
    keyword_counts = {}
    keyword_pattern = r'\b(auto|break|case|char|const|continue|default|do|double|else|enum|extern|float|for|goto|if|int|long|register|return|short|signed|sizeof|static|struct|switch|typedef|union|unsigned|void|volatile|while)\b'
    string_literal_pattern = r'"(?:\\.|[^"\\])*"'

    with open(file_name, 'r') as file:
        content = file.read()

        content = re.sub(r'\n\s*\n', '\n', content) # Remove empty lines
        content = re.sub(r'//.*', '', content) # Remove single-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL) # Remove multi-line comments

        # Replace string literals with placeholders
        placeholders = []
        def replace(match):
            placeholders.append(match.group(0))
            return f'PLACEHOLDER_{len(placeholders)-1}'

        content = re.sub(string_literal_pattern, replace, content)
        keywords = re.findall(keyword_pattern, content) # Find keywords in the modified content

        # Restore placeholders to original string literals
        for i, placeholder in enumerate(placeholders):
            content = content.replace(f'PLACEHOLDER_{i}', placeholder)

        # Count the keywords
        for keyword in keywords:
            keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1

        # Copying data of C to .txt file
        with open('output_OPythonCompiler.txt', 'w') as outputfile:
            outputfile.write(content)

        print("Keywords and their occurrences:")
        for keyword, count in keyword_counts.items():
            print(f"{keyword}: {count}")

def regex_match():
    rexpression = input("Enter the regular expression: ")
    pattern = input("Enter the pattern to check: ")

    if re.fullmatch(rexpression, pattern):
        print("Pattern Matched\n")
    else:
        print("Pattern Not Matched\n")

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
#regex_match()
if os.path.exists(file):
    #count_keywords(file)
    detect_identifier(file)
else:
    print("File does not exist!")