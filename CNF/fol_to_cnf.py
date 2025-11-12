import itertools

# ----------------------------------------------------------
# Use ASCII strings as operator names
# ----------------------------------------------------------
FORALL = 'FORALL'       # ∀
EXISTS = 'EXISTS'       # ∃
NOT = 'NOT'             # ¬
AND = 'AND'             # ∧
OR = 'OR'               # ∨
IMPLIES = 'IMPLIES'     # →
IFF = 'IFF'             # ↔
ATOM = 'ATOM'

# ----------------------------------------------------------
# Unicode symbols for pretty printing only
# ----------------------------------------------------------
unicode_symbols = {
    FORALL: '∀',
    EXISTS: '∃',
    NOT: '¬',
    AND: '∧',
    OR: '∨',
    IMPLIES: '→',
    IFF: '↔'
}

# ----------------------------------------------------------
# Utility counters for skolem and variables
# ----------------------------------------------------------
_skolem_counter = itertools.count(1)
_var_counter = itertools.count(1)

def new_skolem_name():
    return f"SK{next(_skolem_counter)}"

def new_var_name():
    return f"X{next(_var_counter)}"

# ----------------------------------------------------------
# STEP 1: Eliminate ↔ and →
# ----------------------------------------------------------
def eliminate_implications(F):
    if F is None:
        return None

    op = F['op']

    if op == ATOM:
        return F
    elif op == IMPLIES:
        # (α → β) ≡ (¬α ∨ β)
        return {'op': OR,
                'left': {'op': NOT, 'body': eliminate_implications(F['left'])},
                'right': eliminate_implications(F['right'])}
    elif op == IFF:
        # (α ↔ β) ≡ (α → β) ∧ (β → α)
        p = eliminate_implications(F['left'])
        q = eliminate_implications(F['right'])
        return {'op': AND,
                'left': {'op': OR, 'left': {'op': NOT, 'body': p}, 'right': q},
                'right': {'op': OR, 'left': {'op': NOT, 'body': q}, 'right': p}}
    elif op == NOT:
        return {'op': NOT, 'body': eliminate_implications(F['body'])}
    elif op in (AND, OR):
        return {'op': op,
                'left': eliminate_implications(F['left']),
                'right': eliminate_implications(F['right'])}
    elif op in (FORALL, EXISTS):
        return {'op': op, 'var': F['var'], 'body': eliminate_implications(F['body'])}
    return F

# ----------------------------------------------------------
# STEP 2: Move negations inward
# ----------------------------------------------------------
def move_negations_inward(F):
    if F['op'] == ATOM:
        return F
    elif F['op'] == NOT:
        sub = F['body']
        if sub['op'] == ATOM:
            return F
        elif sub['op'] == NOT:
            return move_negations_inward(sub['body'])
        elif sub['op'] == AND:
            return {'op': OR,
                    'left': move_negations_inward({'op': NOT, 'body': sub['left']}),
                    'right': move_negations_inward({'op': NOT, 'body': sub['right']})}
        elif sub['op'] == OR:
            return {'op': AND,
                    'left': move_negations_inward({'op': NOT, 'body': sub['left']}),
                    'right': move_negations_inward({'op': NOT, 'body': sub['right']})}
        elif sub['op'] == FORALL:
            return {'op': EXISTS, 'var': sub['var'],
                    'body': move_negations_inward({'op': NOT, 'body': sub['body']})}
        elif sub['op'] == EXISTS:
            return {'op': FORALL, 'var': sub['var'],
                    'body': move_negations_inward({'op': NOT, 'body': sub['body']})}
    elif F['op'] in (AND, OR):
        return {'op': F['op'],
                'left': move_negations_inward(F['left']),
                'right': move_negations_inward(F['right'])}
    elif F['op'] in (FORALL, EXISTS):
        return {**F, 'body': move_negations_inward(F['body'])}
    return F

# ----------------------------------------------------------
# STEP 3: Standardize variables
# ----------------------------------------------------------
def standardize_variables(F, mapping=None):
    if mapping is None:
        mapping = {}
    if F['op'] == ATOM:
        args = [mapping.get(a, a) for a in F['args']]
        return {'op': ATOM, 'pred': F['pred'], 'args': args}
    elif F['op'] in (AND, OR):
        return {'op': F['op'],
                'left': standardize_variables(F['left'], mapping),
                'right': standardize_variables(F['right'], mapping)}
    elif F['op'] == NOT:
        return {'op': NOT, 'body': standardize_variables(F['body'], mapping)}
    elif F['op'] in (FORALL, EXISTS):
        new_var = new_var_name()
        mapping2 = mapping.copy()
        mapping2[F['var']] = new_var
        return {'op': F['op'], 'var': new_var, 'body': standardize_variables(F['body'], mapping2)}
    return F

# ----------------------------------------------------------
# STEP 4: Skolemize (remove ∃)
# ----------------------------------------------------------
def skolemize(F, scope_vars=None):
    if scope_vars is None:
        scope_vars = []
    if F['op'] == ATOM:
        return F
    elif F['op'] == FORALL:
        return {'op': FORALL, 'var': F['var'], 'body': skolemize(F['body'], scope_vars + [F['var']])}
    elif F['op'] == EXISTS:
        skolem_name = new_skolem_name()
        skolem_term = skolem_name if not scope_vars else f"{skolem_name}({','.join(scope_vars)})"
        return skolemize(substitute(F['body'], F['var'], skolem_term), scope_vars)
    elif F['op'] in (AND, OR):
        return {'op': F['op'],
                'left': skolemize(F['left'], scope_vars),
                'right': skolemize(F['right'], scope_vars)}
    elif F['op'] == NOT:
        return {'op': NOT, 'body': skolemize(F['body'], scope_vars)}
    return F

def substitute(F, var, term):
    if F['op'] == ATOM:
        new_args = [term if a == var else a for a in F['args']]
        return {'op': ATOM, 'pred': F['pred'], 'args': new_args}
    elif F['op'] in (AND, OR):
        return {'op': F['op'],
                'left': substitute(F['left'], var, term),
                'right': substitute(F['right'], var, term)}
    elif F['op'] == NOT:
        return {'op': NOT, 'body': substitute(F['body'], var, term)}
    elif F['op'] in (FORALL, EXISTS):
        if F['var'] == var:
            return F
        return {**F, 'body': substitute(F['body'], var, term)}
    return F

# ----------------------------------------------------------
# STEP 5: Drop ∀ quantifiers
# ----------------------------------------------------------
def drop_universal_quantifiers(F):
    if F['op'] == FORALL:
        return drop_universal_quantifiers(F['body'])
    elif F['op'] in (AND, OR):
        return {'op': F['op'],
                'left': drop_universal_quantifiers(F['left']),
                'right': drop_universal_quantifiers(F['right'])}
    elif F['op'] == NOT:
        return {'op': NOT, 'body': drop_universal_quantifiers(F['body'])}
    return F

# ----------------------------------------------------------
# STEP 6: Distribute ∨ over ∧
# ----------------------------------------------------------
def distribute_or_over_and(F):
    if F['op'] == OR:
        A = distribute_or_over_and(F['left'])
        B = distribute_or_over_and(F['right'])
        if A['op'] == AND:
            return {'op': AND,
                    'left': distribute_or_over_and({'op': OR, 'left': A['left'], 'right': B}),
                    'right': distribute_or_over_and({'op': OR, 'left': A['right'], 'right': B})}
        elif B['op'] == AND:
            return {'op': AND,
                    'left': distribute_or_over_and({'op': OR, 'left': A, 'right': B['left']}),
                    'right': distribute_or_over_and({'op': OR, 'left': A, 'right': B['right']})}
        else:
            return {'op': OR, 'left': A, 'right': B}
    elif F['op'] == AND:
        return {'op': AND,
                'left': distribute_or_over_and(F['left']),
                'right': distribute_or_over_and(F['right'])}
    else:
        return F

# ----------------------------------------------------------
# PRETTY PRINTING (SYMBOLIC OUTPUT)
# ----------------------------------------------------------
def pretty(F):
    """Convert CNF structure to readable symbolic formula."""
    op = F['op']
    if op == ATOM:
        args = ",".join(F['args'])
        return f"{F['pred']}({args})"
    elif op == NOT:
        return f"¬{pretty(F['body'])}"
    elif op in (AND, OR):
        return f"({pretty(F['left'])} {unicode_symbols[op]} {pretty(F['right'])})"
    return str(F)

# ----------------------------------------------------------
# MAIN WRAPPER
# ----------------------------------------------------------
def to_CNF(F):
    F1 = eliminate_implications(F)
    F2 = move_negations_inward(F1)
    F3 = standardize_variables(F2)
    F4 = skolemize(F3)
    F5 = drop_universal_quantifiers(F4)
    F6 = distribute_or_over_and(F5)
    return F6

# ----------------------------------------------------------
# EXAMPLE
# ----------------------------------------------------------
if __name__ == "__main__":
    # ∀x ( P(x) → ∃y Q(y,x) )
    formula = {
        'op': FORALL, 'var': 'x',
        'body': {
            'op': IMPLIES,
            'left': {'op': ATOM, 'pred': 'P', 'args': ['x']},
            'right': {
                'op': EXISTS, 'var': 'y',
                'body': {'op': ATOM, 'pred': 'Q', 'args': ['y', 'x']}
            }
        }
    }

    cnf = to_CNF(formula)
    print("CNF Result (dictionary form):")
    print(cnf)
    print("\nCNF Result (symbolic form):")
    print(pretty(cnf))
