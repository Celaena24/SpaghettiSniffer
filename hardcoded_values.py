# IGNORE IF THERE IS A COMMENT IMMEDATELY ABOVE OR INLINE
import ast

class HardcodedValueVisitor(ast.NodeVisitor):
    def __init__(self):
        self.hardcoded_values = []

    def visit_Constant(self, node):
        # Check if the constant is a string or number that seems hardcoded
        if isinstance(node.value, (str, int, float)) and not self.is_safe_hardcoded(node):
            # Record the line and value
            self.hardcoded_values.append({
                'line': node.lineno,
                'value': node.value,
                'message': f"Potential hardcoded value: {node.value!r}"
            })
        self.generic_visit(node)

    def visit_List(self, node):
        # Check for lists with hardcoded values
        if all(isinstance(elt, ast.Constant) for elt in node.elts):
            values = [elt.value for elt in node.elts]
            self.hardcoded_values.append({
                'line': node.lineno,
                'value': values,
                'message': f"Potential hardcoded list: {values}"
            })
        self.generic_visit(node)

    def is_safe_hardcoded(self, node):
        """
        Helper method to determine if a hardcoded value is safe to ignore.
        For example, we might want to ignore common small integers or empty strings.
        """
        # Example conditions to ignore:
        if isinstance(node.value, int) and node.value in {0, 1, -1}:  # common integers
            return True
        if isinstance(node.value, str) and node.value == "":  # empty string
            return True
        return False

with open('test_hardcoded_values.py') as f:
    source_code = f.read()

tree = ast.parse(source_code)
visitor = HardcodedValueVisitor()
visitor.visit(tree)

# Output the results
for issue in visitor.hardcoded_values:
    print(f"Line {issue['line']}: {issue['message']}")

