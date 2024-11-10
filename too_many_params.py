import ast

# with open('test_too_many_params.py') as f:
#     code = f.read()

class TooManyParametersDetector(ast.NodeVisitor):
    def __init__(self):
        self.guilty_functions = []

    def visit_FunctionDef(self, node):
        param_count = len([arg for arg in node.args.args if arg not in ['self', 'cls']])
        # print(param_count)
        if param_count > 5:
            self.guilty_functions.append({
                'function': node.name,
                'line': node.lineno,
                'column': node.col_offset,
                'parameters': param_count
            })


def get_too_many_params(code):
    tree = ast.parse(code)

    visitor = TooManyParametersDetector()
    visitor.visit(tree)

    return visitor.guilty_functions

# if __name__=='__main__':
#     main()
