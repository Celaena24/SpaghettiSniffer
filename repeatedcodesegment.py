import ast
import hashlib
from collections import defaultdict

class RepeatedFunctionDetector(ast.NodeVisitor):
    def __init__(self):
        self.function_hashes = defaultdict(list)
        self.repeated_functions = []

    def visit_FunctionDef(self, node):
        # Compute a hash for the function's body
        function_body_hash = self.hash_function_body(node)
        self.function_hashes[function_body_hash].append(node)
        if len(self.function_hashes[function_body_hash]) > 1:
            self.repeated_functions.append(node)
        self.generic_visit(node)

    def hash_function_body(self, node):
        # We are only interested in the function's body, so we dump the body of the function
        function_body_str = ''.join([ast.dump(stmt) for stmt in node.body])
        return hashlib.md5(function_body_str.encode('utf-8')).hexdigest()

    def find_repeated_functions(self):
        return [nodes for nodes in self.function_hashes.values() if len(nodes) > 1]

def get_function_start_end_lines(node):
    start_line = node.lineno
    end_line = node.body[-1].end_lineno if hasattr(node.body[-1], 'end_lineno') else node.body[-1].lineno
    return start_line, end_line

def detect_repeated_functions_with_lines(code):
    tree = ast.parse(code)
    detector = RepeatedFunctionDetector()
    detector.visit(tree)
    repeated_functions = detector.find_repeated_functions()
    repeated_with_lines = []
    for func_group in repeated_functions:
        func_info = []
        for func in func_group:
            start_line, end_line = get_function_start_end_lines(func)
            func_info.append((start_line, end_line, func.name))
        repeated_with_lines.append(func_info)
    return repeated_with_lines

