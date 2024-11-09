import ast

class LongFunctionDetector(ast.NodeVisitor):
    def __init__(self, max_length):
        self.max_length = max_length
        self.long_functions = []

    def visit_FunctionDef(self, node):
        start_line = node.lineno
        end_line = node.body[-1].lineno
        length = end_line - start_line + 1
        
        if length > self.max_length:
            self.long_functions.append((node.name, start_line, end_line, length))
        
        self.generic_visit(node)

def find_long_functions(code, max_length):
    tree = ast.parse(code)
    detector = LongFunctionDetector(max_length)
    detector.visit(tree)
    return detector.long_functions

