from flask import Flask, request, jsonify
import unusedimport,longfunctions,badexception,bad_context_management,dead_code, cyclomatic_complexity, hardcoded_values, deep_nesting, too_many_params
app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_file_and_folder():
    data = request.get_json()
    file_content = data.get('fileContent', "")
    folder_content = data.get('folderContent', {})

    # Process the active file content
    highlights = process_file_content(file_content)

    # Process the folder content recursively
    #folder_insights = analyze_folder_contents(folder_content)
    folder_insights = []

    # Return the processed results
    return jsonify({
        "highlights": highlights,
        "folderInsights": folder_insights
    })

def process_file_content(file_content):
    """
    Analyzes the file content for keywords and generates line-based suggestions.
    """
    highlights = []

    print(file_content)
    unused_vars, unused_imports = unusedimport.find_unused_variables_and_imports(file_content)
    print("Unused variables:", unused_vars)
    print("Unused imports:", unused_imports)

    for imports in unused_imports.keys():
            #print(imports,unused_imports.get(imports))
            highlights.append({
                "line": unused_imports.get(imports),
                "suggestion": imports + " library isnt used, do better!!",
                "tag": "unused"
            })
    
    for imports in unused_vars.keys():
            #print(imports,unused_imports.get(imports))
            highlights.append({
                "line": unused_vars.get(imports),
                "suggestion": imports + " variable isnt used, do better!!",
                "tag": "unused"
            })

    max_length = 50
    long_functions = longfunctions.find_long_functions(file_content, max_length)
    for func_name, start_line, end_line, length in long_functions:
         highlights.append({
                "start_line": start_line,
                "end_line": end_line,
                "suggestion": func_name + " too long!!!",
                "tag": "long"
            })
    
    bad_handlers = badexception.find_bad_exception_handling(file_content)
    for lineno in bad_handlers:
        # print(f"Bad exception: Bad exception handling found on line {lineno}")
        highlights.append({
                "line": lineno,
                "suggestion": "can do better exceptions hehe",
                "tag": "exception"
            })
        
    bad_context = bad_context_management.get_bad_context(file_content)
    for context in bad_context:
        highlights.append({
                    "line": context['line'],
                    "suggestion": "nah nah open file properly hehe",
                    "tag": "bad_context"
                })
    
    dead_context = dead_code.get_dead_code(file_content)
    for context in dead_context:
        highlights.append({
                    "line": context['line'],
                    "suggestion": "Do you really want this code here?",
                    "tag": "dead_context"
                })
        
    cyclomatic_complex = cyclomatic_complexity.get_cyclomatic_complexity(file_content)
    for complexity in cyclomatic_complex:
        if complexity['complexity'] > 5:
            highlights.append({
                        "line": complexity['line'],
                        "suggestion": "Nah Nah too complex for me",
                        "tag": "cyclomatic_complex"
                    })
        # print(f"Function '{complexity['function']}' at line {complexity['line']}: Cyclomatic Complexity = {complexity['complexity']}")

    
    hardcoded = hardcoded_values.get_hardcoded(file_content)
    for value in hardcoded:
        highlights.append({
                        "line": value['line'],
                        "suggestion": "do you have an explanation for that value?",
                        "tag": "hardcoded"
                    })
    deep_nest = deep_nesting.get_deep_nesting(file_content)
    for nest in deep_nest:
        highlights.append({
                        "line": value['line'],
                        "suggestion": "too deep cant do?",
                        "tag": "deep_nesting"
                    })
    
    too_many = too_many_params.get_too_many_params(file_content)
    for line in too_many:
        highlights.append({
                        "line": line['line'],
                        "suggestion": "the params are confusing",
                        "tag": "too_many_params"
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

    return highlights

def analyze_folder_contents(folder_content):
    """
    Analyzes the contents of the entire folder recursively for keywords.
    """
    folder_insights = {}

    for filename, content in folder_content.items():
        if isinstance(content, dict):
            # Recurse into subdirectories
            folder_insights[filename] = analyze_folder_contents(content)
        else:
            # Check for keywords in file content
            insights = []
            if "TODO" in content:
                insights.append("This file contains TODO items.")
            if "FIXME" in content:
                insights.append("This file contains FIXME items.")
            folder_insights[filename] = insights if insights else ["No issues found."]

    return folder_insights

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
