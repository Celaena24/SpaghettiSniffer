import ast

class BadVariableNameChecker(ast.NodeVisitor):
    def __init__(self):
        self.bad_name_instances = []

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name) and (len(target.id) < 2 or "temp" in target.id):
                self.bad_name_instances.append((target.id, target.lineno))
        self.generic_visit(node)

    def report(self):
        return self.bad_name_instances

# if __name__ == "__main__":
#     # Example code to check
#     code = """
# foo = 10
# t = 5
# temp_var = 30
# good_var = 42
# temp_var += 1
#     """
def get_bad_variable_name(code):
    tree = ast.parse(code)
    checker = BadVariableNameChecker()
    checker.visit(tree)
    bad_names = checker.report()
    
    line_nums = []
    for var_name, lineno in bad_names:
        line_nums.append(lineno)
        # print(f" - Variable '{var_name}' found at line {lineno}")
    return line_nums
