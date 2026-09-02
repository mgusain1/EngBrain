import ast

def extract_python_symbols(file_path:str, content:str):
    symbols = []
    
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print("AST PARSE FAILED:", file_path, str(e))
        return symbols
    imports = extract_imports(tree,file_path)
    symbols.extend(imports)
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            class_symbol = {
                "file_path": file_path,
                "symbol_type": "class",
                "symbol_name": node.name,
                "parent_name": None,
                "start_line": getattr(node, "lineno", None),
                "end_line": getattr(node, "end_lineno", None),
                "docstring": ast.get_docstring(node)
            }
            symbols.append(class_symbol)
            for child in node.body:
                if isinstance(child, ast.FunctionDef):
                    method_symbol = {
                        "file_path": file_path,
                        "symbol_type": "method",
                        "symbol_name": child.name,
                        "parent_name": node.name,
                        "start_line": getattr(child, "lineno", None),
                        "end_line": getattr(child, "end_lineno", None),
                        "docstring": ast.get_docstring(child)
                    }
                    symbols.append(method_symbol)
        if isinstance(node, ast.FunctionDef):
            function_symbol = {
                "file_path": file_path,
                "symbol_type": "function",
                "symbol_name": node.name,
                "parent_name": None,
                "start_line": getattr(node, "lineno", None),
                "end_line": getattr(node, "end_lineno", None),
                "docstring": ast.get_docstring(node)
            }

            symbols.append(function_symbol)
    return symbols
    
    
def extract_imports(tree, file_path:str):
    imports = []

    for node in tree.body:
        if isinstance(node, ast.Import):
            for name in node.names:
                imports.append({
                    "file_path": file_path,
                    "symbol_type": "import",
                    "symbol_name": name.name,
                    "parent_name": None,
                    "start_line": getattr(node, "lineno", None),
                    "end_line": getattr(node, "end_lineno", None),
                    "docstring": None
                })

        if isinstance(node, ast.ImportFrom):
            module_name = node.module

            if module_name is None:
                module_name = ""

            for name in node.names:
                full_name = module_name + "." + name.name

                imports.append({
                    "file_path": file_path,
                    "symbol_type": "import",
                    "symbol_name": full_name,
                    "parent_name": None,
                    "start_line": getattr(node, "lineno", None),
                    "end_line": getattr(node, "end_lineno", None),
                    "docstring": None
                })

    return imports