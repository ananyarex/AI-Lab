import itertools

def evaluate_expr(expr, values):
    """Evaluate a propositional expression using a dictionary of values."""
    for symbol, value in values.items():
        expr = expr.replace(symbol, str(value))
    return eval(expr)

def generate_truth_table(symbols):
    """Generate all possible truth assignments for a list of symbols."""
    return list(itertools.product([True, False], repeat=len(symbols)))

def build_kb():
    """Set up the knowledge base clauses."""
    kb = {
        'Q_implies_P': 'not Q or P',           # Q → P
        'P_implies_not_Q': 'not P or not Q',   # P → ¬Q
        'Q_or_R': 'Q or R'                     # Q ∨ R
    }
    return kb

def print_full_truth_table(kb, symbols):
    truth_table = generate_truth_table(symbols)

    print(f"{'P':^5} {'Q':^5} {'R':^5} ", end='')
    for clause in kb.keys():
        print(f"{clause:^15} ", end='')
    print(f"{'KB True?':^10}")
    print("-" * (5*3 + 16*len(kb) + 11))

    kb_true_rows = []

    for row in truth_table:
        values = dict(zip(symbols, row))
        kb_values = [evaluate_expr(expr, values) for expr in kb.values()]
        kb_true = all(kb_values)
        def tf(x): return 'T' if x else 'F'
        print(f"{tf(values['P']):^5} {tf(values['Q']):^5} {tf(values['R']):^5} ", end='')
        for val in kb_values:
            print(f"{tf(val):^15} ", end='')
        print(f"{tf(kb_true):^10}")

        if kb_true:
            kb_true_rows.append(values)
    return kb_true_rows

def check_entailment(kb_true_rows, expr):
    entails = True
    for values in kb_true_rows:
        if not evaluate_expr(expr, values):
            entails = False
            break
    return entails

def main():
    kb = build_kb()
    symbols = ['P', 'Q', 'R']

    print("Knowledge Base clauses:")
    for name, clause in kb.items():
        print(f"  {name}: {clause}")

    print("\nFull Truth Table:")
    kb_true_rows = print_full_truth_table(kb, symbols)

    # Predefined additional sentences to check entailment on
    additional_sentences = {
        'R': 'R',
        'R_implies_P': 'not R or P',
        'Q_implies_R': 'not Q or R',
    }

    print("\nEntailment checks for predefined sentences:")
    for name, expr in additional_sentences.items():
        entails = check_entailment(kb_true_rows, expr)
        print(f"Does KB entail '{name}'? {'Yes' if entails else 'No'}")

    # Now interactively ask user for a sentence to check entailment
    alpha = input("\nEnter a propositional sentence to check entailment (use P, Q, R and 'and', 'or', 'not'):\n> ")

    # Check entailment on user sentence for KB-true rows only
    print("\nModels where KB is True and value of your sentence:")
    print(f"{'P':^5} {'Q':^5} {'R':^5} {'Sentence':^10}")
    print("-" * 30)

    results = []
    for values in kb_true_rows:
        alpha_val = evaluate_expr(alpha, values)
        results.append((values, alpha_val))
        def tf(x): return 'T' if x else 'F'
        print(f"{tf(values['P']):^5} {tf(values['Q']):^5} {tf(values['R']):^5} {tf(alpha_val):^10}")

    entailment = all(val for _, val in results)
    print(f"\nDoes the KB entail your sentence? {'Yes' if entailment else 'No'}")

if __name__ == "__main__":
    main()
