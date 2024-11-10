import ast

class ComparisonAgainstBooleanLiterals(ast.NodeVisitor):
    def __init__(self):
        self.comparison_with_bool = []

    def visit_Compare(self, node):
        for comparator in node.comparators:
            if isinstance(comparator, ast.Constant) and comparator.value in (True, False):
                self.comparison_with_bool.append((comparator.value, node.lineno))
        self.generic_visit(node)

    def report(self):
        return self.comparison_with_bool

if __name__ == "__main__":
    # Example code to check
    code = """
foo = 10
if foo == True:
    print(foo)
if foo != False:
    print("Not false")
    """

    tree = ast.parse(code)
    checker = ComparisonAgainstBooleanLiterals()
    checker.visit(tree)
    comparison_with_bool = checker.report()
    
    for value, lineno in comparison_with_bool:
        print(f" - Comparison with '{value}' found at line {lineno}")
    
    
