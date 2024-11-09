# COME UP WITH TEST CASE WITH SAME VARIABLE NAMES
import ast
import hashlib

class CodeDuplicationVisitor(ast.NodeVisitor):
    def __init__(self):
        self.blocks = {}  # Stores hashed blocks and their occurrences
        self.duplicates = []

    def generic_visit(self, node):
        """
        Visit each node in the AST and analyze blocks of code wherever they appear.
        """
        # Process code blocks for any node with a body attribute (e.g., modules, functions, loops, conditionals)
        if hasattr(node, 'body'):
            for block in self.extract_code_blocks(node.body):
                block_hash = self.hash_code_block(block)
                # Track block occurrences
                if block_hash in self.blocks:
                    self.blocks[block_hash]['count'] += 1
                    self.blocks[block_hash]['lines'].append(getattr(node, 'lineno', 1))
                else:
                    self.blocks[block_hash] = {
                        'count': 1,
                        'lines': [getattr(node, 'lineno', 1)],
                        'code': [ast.dump(line) for line in block]  # Store for reference
                    }

        # Continue with the normal traversal of child nodes
        super().generic_visit(node)

    def extract_code_blocks(self, body):
        """
        Extracts code blocks from a list of statements.
        Each sequence of statements is treated as a separate block.
        """
        blocks = []
        current_block = []
        
        for stmt in body:
            if isinstance(stmt, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                # Save the current block if it has statements
                if current_block:
                    blocks.append(current_block)
                    current_block = []
                # Add the control structure's body as its own block
                blocks.append([stmt])
            else:
                current_block.append(stmt)
        
        # Add the final block if it has statements
        if current_block:
            blocks.append(current_block)
        
        return blocks

    def hash_code_block(self, block):
        """
        Generates a hash for a code block based on its AST structure.
        """
        # Serialize the block to an AST dump and hash it
        block_str = ''.join(ast.dump(stmt) for stmt in block)
        return hashlib.md5(block_str.encode()).hexdigest()

    def find_duplicates(self):
        """
        Collects duplicated blocks from `self.blocks`.
        """
        for block_hash, data in self.blocks.items():
            if data['count'] > 1:
                self.duplicates.append({
                    'count': data['count'],
                    'lines': data['lines'],
                    'code': data['code']
                })

# Example usage
source_code = '''
x = 10
y = 20
if x > y:
    print(x)
else:
    print(y)

def function2():
    x = 10
    y = 20
    if x > y:
        print(x)
    else:
        print(y)

def function3():
    x = 10
    y = 20
    if x > y:
        print(x)
    else:
        print(y)
'''

# Parse and analyze the code
tree = ast.parse(source_code)
visitor = CodeDuplicationVisitor()
visitor.visit(tree)
visitor.find_duplicates()

# Output duplicated code blocks
for duplicate in visitor.duplicates:
    print(f"Duplicated block found {duplicate['count']} times at lines {duplicate['lines']}")
    print("Code structure:", duplicate['code'])
    print()

