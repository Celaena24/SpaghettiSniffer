import ast

class BadVariableNameChecker(ast.NodeVisitor):
    def __init__(self):
        self.bad_name_instances = []

    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Store):
            if len(node.id) < 2 or "temp" in node.id:
                self.bad_name_instances.append((node.id, node.lineno, node.col_offset))
        self.generic_visit(node)

    def report(self):
        if not self.bad_name_instances:
            print("No bad variable names found.")
        else:
            print("Bad variable names detected:")
            for var_name, lineno, col_offset in self.bad_name_instances:
                print(f" - Variable '{var_name}' found at line {lineno}, column {col_offset}")

if __name__ == "__main__":
    # Example code to check
    code = """
foo = 10
t = 5
temp_var = 30
good_var = 42
    """

    tree = ast.parse(code)
    checker = BadVariableNameChecker()
    checker.visit(tree)
    checker.report()
