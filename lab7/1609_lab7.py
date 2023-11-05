def find_longest_prefix(alternatives):
    if len(alternatives) < 2:
        return None

    first_alternative = alternatives[0]
    max_prefix = ""

    for alt in alternatives[1:]:
        prefix = ""
        for i in range(min(len(first_alternative), len(alt))):
            if first_alternative[i] == alt[i]:
                prefix += first_alternative[i]
            else:
                break

        if len(prefix) > len(max_prefix):
            max_prefix = prefix

    return max_prefix

def remove_left_factoring(cfg):
    modified = True
    while modified:
        modified = False
        new_productions = []
        for nonterminal, alternatives in cfg.items():
            common_prefix = find_longest_prefix(alternatives)
            if common_prefix and common_prefix != 'ε':
                modified = True
                new_nonterminal = nonterminal + "'"
                new_alternatives = []
                non_common_alternatives = []
                for alt in alternatives:
                    if alt.startswith(common_prefix):
                        remaining_part = alt[len(common_prefix):]
                        if remaining_part:
                            new_alternatives.append(remaining_part)
                        else:
                            new_alternatives.append('ε')
                    else:
                        non_common_alternatives.append(alt)
                new_productions.append((nonterminal, common_prefix + new_nonterminal))
                if new_alternatives:
                    new_productions.append((new_nonterminal, '|'.join(new_alternatives)))
                if non_common_alternatives:
                    new_productions.append((nonterminal, '|'.join(non_common_alternatives)))
            else:
                new_productions.append((nonterminal, '|'.join(alternatives)))
        cfg.clear()
        for nonterminal, production in new_productions:
            cfg.setdefault(nonterminal, []).append(production)
    return cfg

cfg = {}
print("Enter the contect-free grammar: ")
while True:
    production = input()
    if production == '':
        break
    nonterminal, alternatives = production.split('->')
    cfg.setdefault(nonterminal, []).extend(alternatives.split('|'))

left_factoring_found = False
for nonterminal, alternatives in cfg.items():
    if find_longest_prefix(alternatives):
        left_factoring_found = True
        break

if left_factoring_found:
    print("Common prefix found, Left factroing cfg.")

    modified_cfg = remove_left_factoring(cfg)
    print("Modified CFG:")
    for nonterminal, alternatives in modified_cfg.items():
        print(f"{nonterminal} -> {' | '.join(alternatives)}")
else:
    print("No common prefix found")
