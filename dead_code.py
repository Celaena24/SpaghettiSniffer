import ast

class DeadCodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.unreachable_code = []

    def _visit_helper(self, node, terminating_statements):
        has_terminating_statement = False
        for statement in node.body:
            if has_terminating_statement:
                self.unreachable_code.append({
                    'line': statement.lineno,
                    'message': 'unreachable code detected'
                })
            if(isinstance(statement, terminating_statements)):
                has_terminating_statement = True

        # Continue traversing
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """
        Checks for unreachable code within a function by looking for any
        statements after a terminating statement in the same block.
        """
        self._visit_helper(node, (ast.Return, ast.Raise))

    def visit_If(self, node):
        self._visit_helper(node, (ast.Return, ast.Raise))

    def visit_For(self, node):
        self._visit_helper(node, (ast.Break, ast.Continue))

    def visit_While(self, node):
        self._visit_helper(node, (ast.Break, ast.Continue))


with open('test_dead_code.py') as f:
    source_code = f.read()

def get_dead_code(source_code):
    tree = ast.parse(source_code)
    visitor = DeadCodeVisitor()
    visitor.visit(tree)

    # Output the results
    return visitor.unreachable_code

