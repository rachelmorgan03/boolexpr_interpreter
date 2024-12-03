from BoolExprADT import *
import repl
import boolexpr1

# Function to compile a BoolExpr expression into a C++ code string
def compile_expr(expr: BoolExpr, env: dict = None) -> None:

    if env is None:
        env = {}

    # Reset global state for translation
    boolexpr1.true_vars = set()
    boolexpr1.false_vars = set()
    repl.translated_string = ""

    def traverse(expr):

        if isinstance(expr, Literal):
            # Handle literal values
            return "true" if expr.value else "false"
        elif isinstance(expr, Variable):
            # Handle variables
            if expr.name in env:
                if env[expr.name]:
                    boolexpr1.true_vars.add(expr.name)
                else:
                    boolexpr1.false_vars.add(expr.name)
            return expr.name
        elif isinstance(expr, Operator):
            # Handle operators: AND, OR, NOT
            if expr.operator == '~':
                operand = traverse(expr.operands[0])
                return f"!({operand})"
            elif expr.operator == '&':
                left = traverse(expr.operands[0])
                right = traverse(expr.operands[1])
                return f"({left} && {right})"
            elif expr.operator == '|':
                left = traverse(expr.operands[0])
                right = traverse(expr.operands[1])
                return f"({left} || {right})"
        raise ValueError(f"Unknown expression type: {expr}")

    # Translate the expression to C++ code
    repl.translated_string = traverse(expr)

# Writes compiled string translated_string to a file <lineno>.cpp
def write_cpp_output(lineno: int) -> None:
    #global translated_string, true_vars, false_vars
    with open(f"{lineno}.cpp", "w") as file:
        file.write("#include <iostream>\n")
        file.write("using namespace std;\n\n")
        file.write("int main() {\n")
        
        print("the true vars: ", boolexpr1.true_vars)
        print("the false vars: ", boolexp1.false_vars)
        

        for var in boolexpr1.true_vars:
            file.write(f"    bool {var} = true;\n")
        for var in boolexpr1.false_vars:
            file.write(f"    bool {var} = false;\n")

        file.write(f"    bool result = {repl.translated_string};\n")
        file.write("    cout << (result ? \"true\" : \"false\") << endl;\n")
        file.write("    return 0;\n")
        file.write("}\n")
"""
from BoolExprADT import *
import repl
import boolexpr1

# Function to compile a BoolExpr expression into a C++ code string
def compile_expr(expr: BoolExpr, env: dict = None) -> None:
    global repl, boolexpr1

    # This will store the translated expression in C++ format
    translated_expr = ""

    # Recursive case for Literals
    if isinstance(expr, Literal):
        translated_expr = "true" if expr.value else "false"
    
    # Recursive case for Variables
    elif isinstance(expr, Variable):
        translated_expr = expr.name
        if expr.name not in boolexpr1.true_vars and expr.name not in boolexpr1.false_vars:
            if env and env.get(expr.name) is True:
                boolexpr1.true_vars.append(expr.name)
            elif env and env.get(expr.name) is False:
                boolexpr1.false_vars.append(expr.name)

    # Recursive case for Operators
    elif isinstance(expr, Operator):
        operator = expr.operator
        operands = [compile_expr(operand, env) for operand in expr.operands]
        
        if operator == '~':
            # Handle NOT (~) operator
            translated_expr = f"(!{operands[0]})"
        elif operator == '&':
            # Handle AND (&) operator
            translated_expr = f"({operands[0]} && {operands[1]})"
        elif operator == '|':
            # Handle OR (|) operator
            translated_expr = f"({operands[0]} || {operands[1]})"

    # Save the translated expression to the global variable repl.translated_string
    repl.translated_string = translated_expr

# Writes compiled string translated_string to a file <lineno>.cpp
def write_cpp_output(lineno: int) -> None:
    #global translated_string, true_vars, false_vars
    with open(f"{lineno}.cpp", "w") as file:
        file.write("#include <iostream>\n")
        file.write("using namespace std;\n\n")
        file.write("int main() {\n")

        for var in boolexpr1.true_vars:
            file.write(f"    bool {var} = true;\n")
        for var in boolexpr1.false_vars:
            file.write(f"    bool {var} = false;\n")

        file.write(f"    bool result = {repl.translated_string};\n")
        file.write("    cout << (result ? \"true\" : \"false\") << endl;\n")
        file.write("    return 0;\n")
        file.write("}\n")
"""
