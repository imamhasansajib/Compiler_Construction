def parse_grammar(input_lines):
    productions = {}

    for line in input_lines:
        line = line.strip()
        if not line:
            break

        nonterminal, production = line.split('->')
        nonterminal = nonterminal.strip()
        production = [p.strip() for p in production.split('|')]

        if nonterminal in productions:
            productions[nonterminal].extend(production)
        else:
            productions[nonterminal] = production

    return productions

def has_left_recursion(productions, nonterminal):
    if nonterminal not in productions:
        return False

    for production in productions[nonterminal]:
        if production.startswith(nonterminal):
            return True
    return False

def eliminate_left_recursion(cfg, nonterminal):
    if nonterminal not in cfg:
        return

    new_productions = []
    recursive_productions = []
    nonrecursive_productions = []

    for production in cfg[nonterminal]:
        if production.startswith(nonterminal):
            recursive_productions.append(production[len(nonterminal):])
        else:
            nonrecursive_productions.append(production)

    if len(recursive_productions) > 0:
        new_nonterminal = nonterminal + "'"
        if production in nonrecursive_productions:
            for production in nonrecursive_productions:
                new_productions.append(production + new_nonterminal)
        else:
            new_productions.append(new_nonterminal)
        cfg[nonterminal] = new_productions

        for production in recursive_productions:
            cfg.setdefault(new_nonterminal, []).append(production + new_nonterminal)
        cfg.setdefault(new_nonterminal, []).append("ε")

        eliminate_left_recursion(cfg, new_nonterminal)
    else:
        return

def print_grammar(productions):
    primed_versions = set()  # To store the primed versions that have already been printed

    # Print the productions for nonterminals and their primed versions
    for nonterminal, production in productions.items():
        if nonterminal not in primed_versions:
            print(f"{nonterminal} -> {' | '.join(production)}")

            # Check if there is a primed version of the current nonterminal and print its productions
            primed_version = nonterminal + "'"
            if primed_version in productions and primed_version not in primed_versions:
                print(f"{primed_version} -> {' | '.join(productions[primed_version])}")
                primed_versions.add(primed_version)

print("Enter the context-free grammar: ")
input_lines = []
while True:
    line = input()
    if not line:
        break
    input_lines.append(line)

productions = parse_grammar(input_lines)
nonterminals = list(productions.keys())

left_recursion_found = False
for nonterminal in nonterminals:
    if has_left_recursion(productions, nonterminal):
        left_recursion_found = True
        break

if left_recursion_found:
    print("Left recursion found in CFG, eliminating it.")
    for nonterminal in nonterminals:
        eliminate_left_recursion(productions, nonterminal)
    print("Modified Grammar:")
    print_grammar(productions)
else:
    print("No left recursion in CFG.")
