# REMOVE DUPLICATE LINE NUMBERS
# ONLY TAKE THE FIRST LINE IN A SET OF CONSECUTIVE LINES
import ast

class DeepNestingVisitor(ast.NodeVisitor):
    def __init__(self, max_depth=4):
        self.max_depth = max_depth
        self.current_depth = 0
        self.deeply_nested = []

    def check_nesting(self, node):
        """
        Recursively checks the nesting depth of the node and its children.
        """
        self.current_depth += 1
        if self.current_depth > self.max_depth:
            # Record deep nesting if it exceeds the max depth
            self.deeply_nested.append({
                'line': node.lineno,
                'message': f"Nesting level exceeds {self.max_depth} (current level: {self.current_depth})"
            })

        # Check child nodes for further nesting
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                self.check_nesting(child)

        # Backtrack on the nesting level after processing children
        self.current_depth -= 1

    def generic_visit(self, node):
        # Start checking for nesting depth on relevant control flow structures
        if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
            self.check_nesting(node)
        super().generic_visit(node)

with open('test_deep_nesting.py') as f:
    source_code = f.read()

def get_deep_nesting(source_code):
    tree = ast.parse(source_code)
    visitor = DeepNestingVisitor(max_depth=3)  # Set max depth threshold
    deepnest = visitor.visit(tree)
    lines_for_deepnest = []
    for issue in visitor.deeply_nested:
        lines_for_deepnest.append(issue['line'])
    for issue in visitor.deeply_nested:
        print(f"Line {issue['line']}: {issue['message']}")

    return lines_for_deepnest

    # Output the results
    for issue in visitor.deeply_nested:
        print(f"Line {issue['line']}: {issue['message']}")

