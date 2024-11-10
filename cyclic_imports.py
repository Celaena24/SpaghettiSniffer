import ast
import networkx as nx

class ImportDependencyAnalyzer:
    def __init__(self, files):
        self.files = files  # Dictionary with filename as key and code as value
        self.import_graph = nx.DiGraph()  # Directed graph for dependencies
        self.import_locations = {}  # Stores import statements with line numbers

    def build_import_graph(self):
        """
        Parse each file to extract imports and build the import dependency graph.
        """
        for file, code in self.files.items():
            filename = file.split('.')[0]
            self.import_locations[filename] = []
            tree = ast.parse(code)
            self.extract_imports(filename, tree)

    def extract_imports(self, filename, tree):
        """
        Extract imports from a parsed AST tree and add to the import graph.
        """
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported_module = alias.name.split('.')[0]  # Get the top-level module
                    self.add_import(filename, imported_module, node.lineno)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported_module = node.module.split('.')[0]
                    self.add_import(filename, imported_module, node.lineno)

    def add_import(self, source, target, lineno):
        """
        Add an edge in the import graph and record the location of the import.
        """
        if source not in self.import_graph:
            self.import_graph.add_node(source)
        if target not in self.import_graph:
            self.import_graph.add_node(target)
        
        self.import_graph.add_edge(source, target)
        self.import_locations[source].append((target, lineno))

    def find_circular_imports(self):
        """
        Detect cycles in the import graph and return details of circular imports.
        """
        cycles = list(nx.simple_cycles(self.import_graph))
        circular_imports = []
        seen = set()

        for cycle in cycles:
            cycle_imports = []
            for i, file in enumerate(cycle):
                next_file = cycle[(i + 1) % len(cycle)]
                for target, lineno in self.import_locations[file]:
                    if target == next_file and (file, target) not in seen:
                        cycle_imports.append({
                            'file': file,
                            'imports': target,
                            'line': lineno
                        })
                        seen.add((file, target))
                        break
            circular_imports.extend(cycle_imports)

        return circular_imports

# Example usage
# files = {
#     'file_a.py': '''
# import file_c\n
# import file_d as dd\n
#     ''',
#     'file_b.py': '''
# import file_c\n
# import file_a\n
#     ''',
#     'file_c.py': 'import file_d\n',
#     'file_d.py': 'import file_b\n'
# }

def get_cyclic(files):
    structure = {}
    analyzer = ImportDependencyAnalyzer(files)
    analyzer.build_import_graph()
    circular_imports = analyzer.find_circular_imports()
    # Output the circular imports with filenames and line numbers

    for imp in circular_imports:
        if imp['file'] in structure:
            structure[imp['file']].append(imp['line'])
        else:
            structure[imp['file']] = [imp['line']]
    return structure
        # print(f"File '{imp['file']}' has a circular import of '{imp['imports']}' at line {imp['line']}")
