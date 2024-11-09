import ast

class CyclomaticComplexityVisitor(ast.NodeVisitor):
    def __init__(self):
        self.complexities = []  # Stores complexity data for each function

    def visit_FunctionDef(self, node):
        """
        Calculate the cyclomatic complexity for a function.
        """
        self.current_complexity = 1  # Start with base complexity of 1
        self.generic_visit(node)     # Visit all nodes within this function
        self.complexities.append({
            'function': node.name,
            'line': node.lineno,
            'complexity': self.current_complexity
        })

    def visit_If(self, node):
        self.current_complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.current_complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.current_complexity += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        self.current_complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.current_complexity += 1
        self.generic_visit(node)

    def visit_With(self, node):
        self.current_complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        # Increase complexity for each `and/or` in Boolean expressions
        self.current_complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_Compare(self, node):
        # Increment for each comparison (e.g., `a < b < c`)
        self.current_complexity += len(node.ops) - 1
        self.generic_visit(node)

# Example usage
source_code = '''
def simple_function():
    pass

def complex_function(x):
    if x > 0:
        for i in range(x):
            while i < 10:
                if i % 2 == 0:
                    print(i)
    else:
        try:
            with open("file.txt") as f:
                data = f.read()
        except Exception as e:
            print("Error")

def another_function(y):
    return y and (y > 0 or y < 10)
'''

# Parse and analyze the code
tree = ast.parse(source_code)
visitor = CyclomaticComplexityVisitor()
visitor.visit(tree)

# Output the cyclomatic complexities
for complexity in visitor.complexities:
    print(f"Function '{complexity['function']}' at line {complexity['line']}: Cyclomatic Complexity = {complexity['complexity']}")

