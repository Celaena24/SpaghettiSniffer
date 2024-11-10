import ast

class UnnecessaryReturnChecker(ast.NodeVisitor):
    def __init__(self):
        self.unnecessary_returns = []

    def visit_FunctionDef(self, node):
        for child in ast.walk(node):
            if isinstance(child, ast.If):
                # Check if the body of the if-statement only has a return statement returning a boolean
                if (len(child.body) == 1 and isinstance(child.body[0], ast.Return) and
                    isinstance(child.body[0].value, ast.Constant) and isinstance(child.body[0].value.value, bool)):
                    self.unnecessary_returns.append((child.lineno, child.lineno+1))
                
                # Check if the else part only has a return statement returning a boolean
                if (child.orelse and len(child.orelse) == 1 and isinstance(child.orelse[0], ast.Return) and
                    isinstance(child.orelse[0].value, ast.Constant) and isinstance(child.orelse[0].value.value, bool)):
                    self.unnecessary_returns.append((child.orelse[0].lineno - 1, child.orelse[0].lineno))
        
        self.generic_visit(node)

    def report(self):
        return self.unnecessary_returns

if __name__ == "__main__":
    # Example code to check
    code = """
def foo():
    if case1:
        return True
    else:
        return False

def bar():
    if foo():
        return True
        
def new():
    cat = 5
    dog = 7
    if(cat > 5):
        return dog == 7
    """

    tree = ast.parse(code)
    checker = UnnecessaryReturnChecker()
    checker.visit(tree)
    unnecessary_returns = checker.report()
    
    
    for lineno in unnecessary_returns:
        print(f" - Line {lineno} has unnecessary if else returning boolean. Consider simplifying")
