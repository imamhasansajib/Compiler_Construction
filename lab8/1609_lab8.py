def calculate_FIRST(cfg):
    first_sets = {non_terminal: set() for non_terminal in cfg.keys()}

    def update_FIRST(non_terminal):
        if first_sets[non_terminal]:
            return

        for production in cfg[non_terminal]:
            for symbol in production:
                for index, symbol in enumerate(production):
                    next_index = index + 1
                    if next_index < len(production):
                        next_symbol = production[next_index]

                    if symbol in cfg:
                        update_FIRST(symbol)

                        if 'ε' not in first_sets[symbol]:
                            first_sets[non_terminal].update(first_sets[symbol])

                        elif 'ε' in first_sets[symbol] and len(first_sets[symbol]) > 1:

                            if next_symbol in cfg and index == len(production)-1:
                                first_sets[non_terminal].update(first_sets[symbol])
                            else:
                                temp = first_sets[symbol].copy()
                                temp.discard("ε")
                                first_sets[non_terminal].update(temp)
                        # Stop if the non-terminal doesn't derive epsilon
                        if 'ε' not in first_sets[symbol]:
                            break
                    else:
                        first_sets[non_terminal].add(symbol)
                        break

    for non_terminal in cfg.keys():
        update_FIRST(non_terminal)

    return first_sets

def calculate_follow(cfg, first_sets):
    follow_sets = {non_terminal: set() for non_terminal in cfg.keys()}
    follow_sets['S'].add('$')  # Adding '$' to the FOLLOW of the start symbol

    updated = True
    while updated:
        updated = False
        for non_terminal, productions in cfg.items():
            for production in productions:
                follow_added = False  # Initialize follow_added here
                for i, symbol in enumerate(production):
                    if symbol.isupper():  # Non-terminal
                        rest = production[i + 1:]

                        if i < len(production) - 1 and production[i + 1] == "'":
                            symbol += "'"
                            rest = production[i + 2:]

                        for j in range(len(rest)):
                            if rest[j].isupper():
                                follow_sets[symbol] |= (first_sets[rest[j]] - {'ε'})
                                if 'ε' not in first_sets[rest[j]]:
                                    break
                            else:
                                follow_sets[symbol].add(rest[j])
                                if j == len(rest) - 1 and not rest[j].isupper():
                                    follow_added = True
                                else:
                                    if rest[j] in cfg and 'ε' in cfg[rest[j]]:
                                        follow_sets[symbol] |= follow_sets[rest[j]]
                                    break

                        if not follow_added or all_non_terminals_have_epsilon(rest, cfg):
                            follow_sets[symbol] |= follow_sets[non_terminal]

    return follow_sets

def all_non_terminals_have_epsilon(symbols, cfg):
    if not symbols:
        return False
    return all(symbol in cfg and 'ε' in cfg[symbol] for symbol in symbols)

cfg = {}
print("Enter the context-free grammar: ")
while True:
    input_production = input()
    if input_production == '':
        break
    nonterminal, productions = input_production.split('->')
    cfg.setdefault(nonterminal, []).extend(productions.split('|'))

print("FIRST functions: ")
first_sets = calculate_FIRST(cfg)
for non_terminal, first_set in first_sets.items():
    print(f"FIRST({non_terminal}) = {first_set}")

print("\nFOLLOW functions: ")
follow_sets = calculate_follow(cfg, first_sets)
for non_terminal, follow_set in follow_sets.items():
    print(f"FOLLOW({non_terminal}) = {follow_set}")