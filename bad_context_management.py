import ast

class BadContextVisitor(ast.NodeVisitor):
    def __init__(self):
        self.bad_context_usage = []

    def visit_Call(self, node):
        # Check if this is a call to 'open'
        if isinstance(node.func, ast.Name) and node.func.id == 'open':
            # Check if it's inside a `with` statement
            if not self.is_with_context(node):
                # Record the line number if `open` is not in a `with` statement
                self.bad_context_usage.append({
                    'line': node.lineno,
                    'column': node.col_offset,
                    'message': "'open' used outside of a 'with' statement"
                })

        # Continue traversing child nodes
        self.generic_visit(node)

    def is_with_context(self, node):
        """
        Helper method to check if a node is within a `with` context manager.
        """
        current = node
        while current:
            if isinstance(current, ast.With):
                return True
            current = getattr(current, 'parent', None)
        return False

    def generic_visit(self, node):
        # Set the `parent` attribute for each child node to track context
        for child in ast.iter_child_nodes(node):
            child.parent = node
        super().generic_visit(node)

# Example usage
with open('test_bad_context_management.py') as f:
    source_code = f.read()
tree = ast.parse(source_code)
visitor = BadContextVisitor()
visitor.visit(tree)

print(visitor.bad_context_usage)

