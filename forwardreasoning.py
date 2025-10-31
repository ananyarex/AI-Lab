import re

def isVariable(x):
    """
    Heuristically checks if a string is a variable (single, lowercase, alphabetic).
    """
    return len(x) == 1 and x.islower() and x.isalpha()

def getAttributes(string):
    """
    Extracts the parenthesized attribute strings. (e.g., 'P(a,b)' -> ['(a,b)'])
    Note: This uses simple regex and will struggle with nested functions.
    """
    expr = r'\([^)]+\)'
    matches = re.findall(expr, string)
    return matches

def getPredicates(string):
    """
    Extracts the predicate symbol. (e.g., 'P(a,b)' -> ['P'])
    """
    expr = r'([a-z~]+)\([^&|]+\)'
    return re.findall(expr, string)

class Fact:
    """
    Represents a single fact in the KB (e.g., 'Mother(a,b)').
    """
    def __init__(self, expression):
        self.expression = expression
        predicate, params = self.splitExpression(expression)
        self.predicate = predicate
        self.params = params
        # result is true if the fact contains at least one constant
        self.result = any(self.getConstants()) 

    def splitExpression(self, expression):
        """
        Splits the expression into predicate and parameters.
        """
        predicate = getPredicates(expression)[0]
        params = getAttributes(expression)[0].strip('()').split(',')
        return [predicate, params]

    def getResult(self):
        """
        Returns True if the fact has at least one constant.
        (Usage seems specific to this simplified inference process).
        """
        return self.result

    def getConstants(self):
        """
        Returns a list of constants (or None for variables).
        """
        return [None if isVariable(c) else c for c in self.params]

    def getVariables(self):
        """
        Returns a list of variables (or None for constants).
        """
        return [v if isVariable(v) else None for v in self.params]

    def substitute(self, constants):
        """
        Applies a substitution (constants) to create a new grounded Fact.
        (Seems unused in the evaluate method, but provided here.)
        """
        c = constants.copy()
        f = f"{self.predicate}({','.join([constants.pop(0) if isVariable(p) else p for p in self.params])})"
        return Fact(f)

class Implication:
    """
    Represents an implication rule (e.g., 'Mother(x,y)&Father(y,z) => Grandparent(x,z)').
    """
    def __init__(self, expression):
        self.expression = expression
        l = expression.split('=>')
        # LHS is a list of Facts connected by '&'
        self.lhs = [Fact(f) for f in l[0].split('&')]
        self.rhs = Fact(l[1])

    def evaluate(self, facts):
        """
        Attempts to apply the rule (forward chaining) using existing facts.
        This simplified version finds constants by position matching.
        """
        constants = {}
        new_lhs = [] # Facts that successfully matched LHS predicates

        for fact in facts:
            for val in self.lhs:
                if val.predicate == fact.predicate:
                    # Collect constants based on variable positions
                    for i, v in enumerate(val.getVariables()):
                        if v:
                            constants[v] = fact.getConstants()[i]
                    new_lhs.append(fact)

        # Check if we matched all LHS facts and if all matched facts are "true" (have constants)
        if len(new_lhs) == len(self.lhs) and all([f.getResult() for f in new_lhs]):
            # Construct the RHS fact by applying the collected constants
            predicate, attributes = getPredicates(self.rhs.expression)[0], str(getAttributes(self.rhs.expression)[0])
            for key in constants:
                if constants[key]:
                    # Simple string replacement for substitution
                    attributes = attributes.replace(key, constants[key])

            expr = f'{predicate}{attributes}'
            return Fact(expr)
        
        return None

class KB:
    """
    The Knowledge Base containing facts and implications.
    """
    def __init__(self):
        self.facts = set()
        self.implications = set()

    def tell(self, e):
        """
        Adds a new fact or implication to the KB and performs inference.
        """
        if '=>' in e:
            self.implications.add(Implication(e))
        else:
            self.facts.add(Fact(e))
            
        # Run forward chaining (simple form: only one pass)
        for i in self.implications:
            res = i.evaluate(self.facts)
            if res:
                self.facts.add(res)

    def ask(self, e):
        """
        Searches the current facts for facts matching the query's predicate.
        """
        facts = set([f.expression for f in self.facts])
        i = 1
        print(f'Querying {e}:')
        for f in facts:
            if Fact(f).predicate == Fact(e).predicate:
                print(f'\t{i}. {f}')
                i += 1

    def display(self):
        """
        Prints all unique facts currently in the KB.
        """
        print("All facts: ")
        for i, f in enumerate(set([f.expression for f in self.facts])):
            print(f'\t{i+1}. {f}')

def main():
    """
    Main execution function to run the KB system.
    """
    kb = KB()
    print("Enter the number of FOL expressions present in KB:")
    # Example input: 2
    n = int(input()) 
    
    print("Enter the expressions:")
    # Example inputs: 
    # Mother(ANN,BOB)
    # Mother(x,y)&Father(y,z) => Grandparent(x,z)
    for i in range(n):
        fact = input()
        kb.tell(fact)
        
    print("Enter the query:")
    # Example input: Grandparent(ANN,z)
    query = input()
    
    kb.ask(query)
    kb.display()

if __name__ == "__main__":
    main()
