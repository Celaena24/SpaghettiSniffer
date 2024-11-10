import os,sys
from flask import Flask, request, jsonify
import lang
# current_file_name = os.path.basename(__file__)
# #print("file name: ",current_file_name)
import unusedimport,longfunctions,badexception,bad_context_management,dead_code, cyclomatic_complexity, hardcoded_values, deep_nesting, too_many_params, multiple_files_duplicate_code, cyclic_imports, bad_variable_name, bad_variable_name, comparing_against_bool_literals, print_statements, unnecessary_return_checks
app = Flask(__name__)
folder_insights_store = {}
file_contents = {}
cycle_data_global = {}

@app.route('/process', methods=['POST'])
def process_file_and_folder():
    data = request.get_json()
    file_content = data.get('fileContent', "")
    folder_content = data.get('folderContent', {})
    current_file = data.get('current_fileName')
    current_file = current_file.split("\\")[-1]

    # Process the active file content
    highlights = process_file_content(file_content,folder_content,current_file)

    # Process the folder content recursively
    folder_insights = analyze_folder_contents(folder_content,current_file)
    # folder_insights = []
    #print("folder insightsss: ", folder_insights)
    # Return the processed results
    return jsonify({
        "highlights": highlights,
        "folderInsights": folder_insights
    })

def process_file_content(file_content,folder_content,current_file):
    """
    Analyzes the file content for keywords and generates line-based suggestions.
    """
    highlights = []

    #print(file_content)
    unused_vars, unused_imports = unusedimport.find_unused_variables_and_imports(file_content)
    #print("Unused variables:", unused_vars)
    #print("Unused imports:", unused_imports)

    for imports in unused_imports.keys():
            ##print(imports,unused_imports.get(imports))
            highlights.append({
                "line": unused_imports.get(imports),
                "suggestion": lang.get_comment("unused imports" + imports),
                "tag": "unused"
            })
    
    for imports in unused_vars.keys():
            ##print(imports,unused_imports.get(imports))
            highlights.append({
                "line": unused_vars.get(imports),
                "suggestion": lang.get_comment("unused variables" + imports),
                "tag": "unused"
            })

    max_length = 50
    long_functions = longfunctions.find_long_functions(file_content, max_length)
    for func_name, start_line, end_line, length in long_functions:
         highlights.append({
                "start_line": start_line,
                "end_line": end_line,
                "suggestion": lang.get_comment("too long function" + func_name),
                "tag": "long"
            })
    
    bad_handlers = badexception.find_bad_exception_handling(file_content)
    for lineno in bad_handlers:
        # #print(f"Bad exception: Bad exception handling found on line {lineno}")
        highlights.append({
                "line": lineno,
                "suggestion": lang.get_comment("bad exception handling"),
                "tag": "exception"
            })
        
    bad_context = bad_context_management.get_bad_context(file_content)
    for context in bad_context:
        highlights.append({
                    "line": context['line'],
                    "suggestion": lang.get_comment("nah nah open file properly hehe"),
                    "tag": "bad_context"
                })
    
    dead_context = dead_code.get_dead_code(file_content)
    for context in dead_context:
        highlights.append({
                    "line": context['line'],
                    "suggestion": lang.get_comment("dead code"),
                    "tag": "dead_context"
                })
        
    cyclomatic_complex = cyclomatic_complexity.get_cyclomatic_complexity(file_content)
    for complexity in cyclomatic_complex:
        if complexity['complexity'] > 5:
            highlights.append({
                        "line": complexity['line'],
                        "suggestion": lang.get_comment("cyclomatic complexity too high"),
                        "tag": "cyclomatic_complex"
                    })
        # #print(f"Function '{complexity['function']}' at line {complexity['line']}: Cyclomatic Complexity = {complexity['complexity']}")

    
    hardcoded = hardcoded_values.get_hardcoded(file_content)
    for value in hardcoded:
        highlights.append({
                        "line": value['line'],
                        "suggestion": lang.get_comment("no explanation for hardcoded value"),
                        "tag": "hardcoded"
                    })
    deep_nest = deep_nesting.get_deep_nesting(file_content)
    for nest in deep_nest:
        highlights.append({
                        "line": value['line'],
                        "suggestion": lang.get_comment("Nesting is too deep. Can't do"),
                        "tag": "deep_nesting"
                    })
    
    too_many = too_many_params.get_too_many_params(file_content)
    for line in too_many:
        highlights.append({
                        "line": line['line'],
                        "suggestion": lang.get_comment("too many params"),
                        "tag": "too_many_params"
                    })
    bad_variables = bad_variable_name.get_bad_variable_name(file_content)
    for line in bad_variables:
        highlights.append({
                        "line": line,
                        "suggestion": "bad variable name",
                        "tag": "bad_variable_name"
                    })
    
    bad_var_usage = bad_variable_name.get_bad_variable_name(file_content)
    for line in bad_var_usage:
        highlights.append({
                        "line": line,
                        "suggestion": "bad variable usage",
                        "tag": "bad_variable_usage"
                    })
        
    bad_comparison = comparing_against_bool_literals.get_bad_bool_comparisons(file_content)
    for line in bad_comparison:
        highlights.append({
                        "line": line,
                        "suggestion": "bad boolean comparison",
                        "tag": "bad_bool_comparison"
                    })
    statements = print_statements.get_print_statements(file_content)
    for line in statements:
        highlights.append({
                        "line": line,
                        "suggestion": "print statement",
                        "tag": "print_statement"
                    })
        
    unnecessary_checks = unnecessary_return_checks.get_unnecessary_checks(file_content)
    for line in unnecessary_checks:
        highlights.append({
                        "line": line,
                        "suggestion": "unnecessary return check",
                        "tag": "unnecessary_return_check"
                    })

    # folder_insights = analyze_folder_contents(folder_content,current_file)
    analyze_folder_contents(folder_content,current_file)
    print("cycle data global", cycle_data_global)
    # print("current_file_name: ",current_file)
    # print("\n\nfolder_insights: ",folder_insights[current_file])
    # print("folder insights: ",folder_insights_store.keys())
    if current_file in folder_insights_store:
        for line in folder_insights_store[current_file]:
            highlights.append(line)
    print("\n\nhighlights: ",highlights)

    for data in cycle_data_global[current_file.split('.')[0]]:
        highlights.append({
                        "line": data,
                        "suggestion": "cyclic import!!!",
                        "tag": "cyclic_import"
                    })


    



    return highlights

    # # Split content by lines and look for keywords
    # lines = file_content.splitlines()
    # for index, line in enumerate(lines):
    #     if "TODO" in line:
    #         highlights.append({
    #             "line": index,
    #             "suggestion": "Complete this TODO item."
    #         })
    #     elif "FIXME" in line:
    #         highlights.append({
    #             "line": index,
    #             "suggestion": "Check and fix this issue."
    #         })

    # return highlights

def analyze_folder_contents(folder_content,current_file):
    """
    Analyzes the contents of the entire folder recursively for keywords.
    """

    # print(" in analyze_folder_contents")
    

    

    for filename, content in folder_content.items():
        
        # if filename == current_file:
        #     print("yessssss")
        if isinstance(content, dict):
            # print("in isinstanceeee")
            # Recurse into subdirectories
            analyze_folder_contents(content,current_file)
        else:
            # print("file name: ",filename)
            # print("not isinstanceeee")
            # Check for keywords in file content

            file_contents[filename] = content
            folder_insights_store[filename] = []
            cycle_data_global[filename.split('.')[0]] = []
    
    duplicate_multiple = multiple_files_duplicate_code.get_duplicate_multiple(file_contents)
    cycle = cyclic_imports.get_cyclic(file_contents)
    print("priting cycle", cycle)

    for value in cycle.items():
        current_file_name = current_file.split('.')[0]
        if value[0] == current_file_name:
            cycle_data_global[current_file_name] = value[1]


    for duplicate in duplicate_multiple:
        for value in duplicate['lines']:
            if value[0] == current_file:
                filename = value[0]
                # if not filename in folder_insights_store.keys():
                #     folder_insights_store[filename] = []
                # else:
                folder_insights_store[filename].append({
                    "start_line":value[1],
                    "end_line": value[2],
                    "suggestion": "repetitive code across files",
                    "tag": "multiple_duplicate"
                })

    # for filename, content in folder_content.items():
    #     insights = []
    #     # if "TODO" in content:
    #     #     insights.append("This file contains TODO items.")
    #     # if "FIXME" in content:
    #     #     insights.append("This file contains FIXME items.")
        
    #     for duplicate in duplicate_multiple:
    #         # print("duplicate: ",duplicate, file = sys.stderr)
    #         # print("duplicate: ",duplicate)
    #         for value in duplicate['lines']:
    #             print("value: ",value, current_file)
    #             if value[0] == current_file:
    #                 insights.append({
    #                         "start_line":value[1],
    #                         "end_line": value[2],
    #                         "suggestion": "repetitive code across files",
    #                         "tag": "multiple_duplicate"
    #                     })
    #                 if current_file == 'WordFrequency.py': print('look at me', len(insights))
    #     if current_file == 'WordFrequency.py':
    #         print("\n\ninsights: ",insights)
    #     folder_insights_store[filename] = insights if insights else ["No issues found."]
    #     # print("folder_insights: ",folder_insights_store.keys())

    #     # #print("folderrrr: ",folder_insights)
    #     # return folder_insights_store

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
