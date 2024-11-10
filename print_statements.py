import ast

class PrintStatementChecker(ast.NodeVisitor):
    def __init__(self):
        self.print_statements = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == 'print':
            self.print_statements.append(node.lineno)
        self.generic_visit(node)

    def report(self):
        return self.print_statements

if __name__ == "__main__":
    # Example code to check
    code = """
foo = 10
print(foo)
t = 5
print("Hello World")
    """

    tree = ast.parse(code)
    checker = PrintStatementChecker()
    checker.visit(tree)
    print_stmts = checker.report()
    
    for lineno in print_stmts:
        print(f" - Print statement found at line {lineno}")
