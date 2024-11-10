import ast
from collections import defaultdict

class VariableUsageChecker(ast.NodeVisitor):
    def __init__(self):
        self.assignments = defaultdict(list)
        self.usages = defaultdict(list)
        self.multiple_assignments = []
        

    def visit_Assign(self, node):
        if isinstance(node.targets[0], ast.Name):
            var_name = node.targets[0].id
            self.assignments[var_name].append(node.lineno)
        self.generic_visit(node)
        
    def visit_Name(self, node):
        if isinstance(node.ctx, ast.Load):  # Check if the variable is being used (read)
            self.usages[node.id].append(node.lineno)
        self.generic_visit(node)

    def check_variables(self):
        for var_name, occurrences in self.assignments.items():
            if len(occurrences) > 1:
                cur_ass = 1
                cur_use = 0
                mult_ass = []
                
                usages = self.usages.get(var_name, [])
                while(cur_ass < len(occurrences) and cur_use < len(usages)):
                    if(usages[cur_use] > occurrences[cur_ass]): 
                        # mult_ass.append(occurrences[cur_ass-1])
                        mult_ass.append(occurrences[cur_ass])
                    cur_ass += 1
                    cur_use += 1
                    
                mult_ass += occurrences[cur_ass: ]
                if mult_ass:
                    self.multiple_assignments.append((var_name, set(mult_ass)))
                

    def report(self):
        return self.multiple_assignments

# if __name__ == "__main__":
#     # Example code to check
#     code = """
# def example():
#     x = 10
#     x = 20
#     x = 30
#     y = 30
#     z = x + 1
#     a = 50
#     t = a*5
#     a = 5
#     a = 7
#     a = x+10
#     return z
#     """
    
#     tree = ast.parse(code)
#     checker = VariableUsageChecker()
#     checker.visit(tree)
#     checker.check_variables()
#     multiple_assignments = checker.report()
    
#     bad_var_lines = []
#     for var_name, occurrences in multiple_assignments:
# #                 # print(f" - Variable assigned multiple times before usage. Variable '{var_name}' assigned at:")
#         for lineno in occurrences:
#             bad_var_lines.append(lineno)
#                 # print(f"   Line {lineno}")
#     print(bad_var_lines)
    
    

def get_bad_variable_usage(code):
    bad_var_lines = []
    tree = ast.parse(code)
    checker = VariableUsageChecker()
    checker.visit(tree)
    checker.check_variables()
    multiple_assignments = checker.report()
    
    for var_name, occurrences in multiple_assignments:
                # print(f" - Variable assigned multiple times before usage. Variable '{var_name}' assigned at:")
        for lineno in occurrences:
            bad_var_lines.append(lineno)
                # print(f"   Line {lineno}")
    return bad_var_lines
    
    
    
