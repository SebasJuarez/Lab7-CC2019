import re
import itertools

# Define a function to load grammar from file
def load_grammar(file_path):
    grammar = {}
    # Modified regex to support Unicode characters and match the provided grammar pattern
    pattern = re.compile(r"^[A-Z𝐴-𝑍𝑎-𝑧] → ([0-9A-Z𝐴-𝑍𝑎-𝑧]+(\|[0-9A-Z𝐴-𝑍𝑎-𝑧]+)*)|ε$")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                match = pattern.match(line)
                if not match:
                    raise ValueError(f"Invalid grammar line: {line}")
                head, productions = line.split(' → ')
                grammar[head] = [prod.strip() for prod in productions.split('|')]
    except Exception as e:
        print(f"Error reading grammar: {e}")
        return None
    return grammar

# Define a function to find nullable symbols
def find_nullable_symbols(grammar):
    nullable = set()
    updated = True
    while updated:
        updated = False
        for head, productions in grammar.items():
            for prod in productions:
                if prod == "ε" or all(symbol in nullable for symbol in prod if symbol.isupper() or symbol in '𝐴𝐵𝐶𝐷𝐸𝐹𝐺𝐻𝐼𝐽𝐾𝐿𝐌𝐍𝐎𝐏𝐐𝐑𝐒𝐓𝐔𝐕𝐖𝐗𝐘𝐙'):
                    if head not in nullable:
                        nullable.add(head)
                        updated = True
    return nullable

# Define a function to eliminate epsilon productions
def eliminate_epsilon_productions(grammar):
    nullable = find_nullable_symbols(grammar)
    new_grammar = {}

    for head, productions in grammar.items():
        new_productions = set()
        for prod in productions:
            if prod != "ε":
                symbols = [nullable_symbol for nullable_symbol in prod if nullable_symbol in nullable]
                power_set = list(itertools.chain.from_iterable(itertools.combinations(symbols, r) for r in range(len(symbols) + 1)))
                for subset in power_set:
                    new_prod = list(prod)
                    for symbol in subset:
                        new_prod.remove(symbol)
                    new_productions.add("".join(new_prod))
        new_grammar[head] = list(new_productions)

    # Remove epsilon productions from the final grammar
    for head, productions in new_grammar.items():
        new_grammar[head] = [prod for prod in productions if prod and prod != "𝜀"]

    return new_grammar

# Function to print grammar
def print_grammar(grammar):
    for head, productions in grammar.items():
        print(f"{head} → {' | '.join(productions)}")

if __name__ == "__main__":
    file_1 = "grammar1.txt"
    file_2 = "grammar2.txt"

    grammar_1 = load_grammar(file_1)
    if grammar_1:
        print("\nOriginal Grammar 1:")
        print_grammar(grammar_1)

        simplified_grammar_1 = eliminate_epsilon_productions(grammar_1)
        print("\nSimplified Grammar 1 (without epsilon productions):")
        print_grammar(simplified_grammar_1)

    grammar_2 = load_grammar(file_2)
    if grammar_2:
        print("\nOriginal Grammar 2:")
        print_grammar(grammar_2)

        simplified_grammar_2 = eliminate_epsilon_productions(grammar_2)
        print("\nSimplified Grammar 2 (without epsilon productions):")
        print_grammar(simplified_grammar_2)