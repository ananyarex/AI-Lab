import re

def getAttributes(expression):
    """
    Extracts the arguments/attributes from a predicate expression (e.g., P(a,b) -> ['a', 'b']).
    Note: This simplified version will struggle with nested functions like P(f(x), y).
    """
    expression = expression.split("(")[1:]
    expression = "(".join(expression)
    expression = expression.split(")")[:-1]
    expression = ")".join(expression)
    attributes = expression.split(',')
    return attributes

def getInitialPredicate(expression):
    """
    Extracts the predicate symbol (e.g., P(a,b) -> P).
    """
    return expression.split("(")[0]

def isConstant(char):
    """
    Checks if a string is a constant (single uppercase letter).
    """
    return char.isupper() and len(char) == 1

def isVariable(char):
    """
    Checks if a string is a variable (single lowercase letter).
    """
    return char.islower() and len(char) == 1

def replaceAttributes(exp, old, new):
    """
    Applies a single substitution (old -> new) to the attributes of an expression.
    """
    attributes = getAttributes(exp)
    predicate = getInitialPredicate(exp)
    for index, val in enumerate(attributes):
        if val == old:
            attributes[index] = new
    return predicate + "(" + ",".join(attributes) + ")"

def apply(exp, substitutions):
    """
    Applies a list of substitutions sequentially to an expression.
    """
    for new, old in substitutions:
        exp = replaceAttributes(exp, old, new)
    return exp

def checkOccurs(var, exp):
    """
    Performs the Occurs Check: returns True if 'var' is found in 'exp'.
    """
    if exp.find(var) == -1:
        return False
    return True

def getFirstPart(expression):
    """
    Gets the first argument of the predicate.
    """
    attributes = getAttributes(expression)
    return attributes[0]

def getRemainingPart(expression):
    """
    Returns the predicate with all arguments EXCEPT the first one.
    """
    predicate = getInitialPredicate(expression)
    attributes = getAttributes(expression)
    newExpression = predicate + "(" + ",".join(attributes[1:]) + ")"
    return newExpression

def unify(exp1, exp2):
    """
    The main Unification Algorithm (recursive).
    """
    # Step 1: Base Case - Identical
    if exp1 == exp2:
        return []

    # Step 1: Base Case - Constants
    if isConstant(exp1) and isConstant(exp2):
        if exp1 != exp2:
            print(f"{exp1} and {exp2} are constants. Cannot be unified")
        return []
        
    # Step 1: Base Case - One is a Constant, One is a Variable/Term
    # (The original code handles simple constants, but this block is incomplete
    # and likely intended for constant-term/variable unification.)
    if isConstant(exp1):
        # NOTE: This assumes exp2 is a variable or constant, but if exp2 is complex, this fails.
        return [(exp1, exp2)]
    if isConstant(exp2):
        # NOTE: This assumes exp1 is a variable or constant, but if exp1 is complex, this fails.
        return [(exp2, exp1)]

    # Step 1: Variable Check (W1 is a variable)
    if isVariable(exp1):
        # returns [(exp2, exp1)] on success, or [] on failure (Occurs Check)
        return [(exp2, exp1)] if not checkOccurs(exp1, exp2) else []

    # Step 1: Variable Check (W2 is a variable)
    if isVariable(exp2):
        # returns [(exp1, exp2)] on success, or [] on failure (Occurs Check)
        return [(exp1, exp2)] if not checkOccurs(exp2, exp1) else []
        
    # Step 2: Predicate Check
    if getInitialPredicate(exp1) != getInitialPredicate(exp2):
        print("Cannot be unified as the predicates do not match!")
        return []
        
    # Step 3: Arity Check
    attributeCount1 = len(getAttributes(exp1))
    attributeCount2 = len(getAttributes(exp2))
    if attributeCount1 != attributeCount2:
        print(f"Length of attributes {attributeCount1} and {attributeCount2} do not match. Cannot be unified")
        return []

    # Steps 5 & 6: Recursive Unification
    
    # Unify the first parts (heads)
    head1 = getFirstPart(exp1)
    head2 = getFirstPart(exp2)
    initialSubstitution = unify(head1, head2)
    
    if not initialSubstitution and (head1 != head2): # Note: Added head1!=head2 check for clarity
        return []
        
    # If only one attribute remains, we're done
    if attributeCount1 == 1:
        return initialSubstitution
        
    # Prepare the remaining parts (tails)
    tail1 = getRemainingPart(exp1)
    tail2 = getRemainingPart(exp2)
    
    # Apply substitution to the remaining parts (Crucial step for consistency)
    if initialSubstitution:
        tail1 = apply(tail1, initialSubstitution)
        tail2 = apply(tail2, initialSubstitution)
        
    # Recursively unify the remaining parts
    remainingSubstitution = unify(tail1, tail2)
    
    if remainingSubstitution is False: # Check if remaining unification failed
        return []
        
    # Compose the substitutions
    return initialSubstitution + remainingSubstitution

if __name__ == "__main__":
    print("Unification Algorithm (Simple String-based)")
    print("-" * 35)
    print("Enter the first expression (e.g., P(x,f(y)))")
    e1 = input()

    print("Enter the second expression (e.g., P(g(z),f(a)))")
    e2 = input()
    
    # Note: This implementation has limitations with complex nested terms due to simple string parsing.
    substitutions = unify(e1, e2)
    
    print("-" * 35)
    print("The substitutions (MGU) are:")
    if substitutions is False or substitutions == []:
        print("Unification Failed or No Substitutions Needed.")
    else:
        # Reformat the output for clarity (e.g., ('g(z)', 'x') -> g(z) / x)
        print([f"{new} / {old}" for new, old in substitutions])
