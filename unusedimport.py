import ast

class UnusedVariableAndImportChecker(ast.NodeVisitor):
    def __init__(self):
        self.assigned_vars = {}
        self.used_vars = {}
        self.imported_names = {}
        self.used_imports = {}

    def visit_Assign(self, node):
        # Collect all assigned variable names with their line numbers
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.assigned_vars[target.id] = node.lineno
        self.generic_visit(node)
    
    def visit_Name(self, node):
        # Collect all used variable names with their line numbers
        if isinstance(node.ctx, ast.Load):
            self.used_vars[node.id] = node.lineno
        self.generic_visit(node)

    def visit_Import(self, node):
        # Collect all imported module names with their line numbers
        for alias in node.names:
            self.imported_names[alias.name] = node.lineno
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        # Collect all imported names from a module with their line numbers
        for alias in node.names:
            self.imported_names[alias.name] = node.lineno
        self.generic_visit(node)

    def report_unused(self):
        # Find unused variables and imports
        unused_vars = {var: lineno for var, lineno in self.assigned_vars.items() if var not in self.used_vars}
        unused_imports = {imp: lineno for imp, lineno in self.imported_names.items() if imp not in self.used_vars}
        return unused_vars, unused_imports

def find_unused_variables_and_imports(code):
    tree = ast.parse(code)
    checker = UnusedVariableAndImportChecker()
    checker.visit(tree)
    unused_vars, unused_imports = checker.report_unused()
    return unused_vars, unused_imports


