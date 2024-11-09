import ast

class BadExceptionHandlerChecker(ast.NodeVisitor):
    def __init__(self):
        self.bad_handlers = []

    def visit_ExceptHandler(self, node):
        # Check if the exception handler has no type specified (i.e., it's a bare except)
        if node.type is None:
            self.bad_handlers.append(node.lineno)
        self.generic_visit(node)

def find_bad_exception_handling(code):
    tree = ast.parse(code)
    checker = BadExceptionHandlerChecker()
    checker.visit(tree)
    return checker.bad_handlers


