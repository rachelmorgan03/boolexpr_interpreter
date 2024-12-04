from BoolExprADT import *
import repl
import boolexpr1

# Function to compile a BoolExpr expression into a C++ code string
def compile_expr(expr: BoolExpr, env: dict = None) -> None:
    global repl, boolexpr1
    if env is None:
        env = {}
        
    repl.translated_string = ""

    # Translate the expression to C++ code
    if isinstance(expr, Literal):
        # Handle literal values
        repl.translated_string = "true" if expr.value else "false"

    elif isinstance(expr, Variable):
        if expr.name not in boolexpr1.true_vars and expr.name not in boolexpr1.false_vars:
            if env and env.get(expr.name) is True:
                boolexpr1.true_vars[expr.name] = True
            elif env and env.get(expr.name) is False:
                boolexpr1.false_vars[expr.name] = False
        repl.translated_string = expr.name

    elif isinstance(expr, Operator):
        # Handle operators: AND, OR, NOT
        if expr.operator == '~':
            operand = compile_expr(expr.operands[0], env)
            repl.translated_string = f"! {repl.translated_string}"
        elif expr.operator == '&':
            compile_expr(expr.operands[0], env)
            left_translated = repl.translated_string
            compile_expr(expr.operands[1], env)
            repl.translated_string = f"{left_translated} && {repl.translated_string}"
        elif expr.operator == '|':
            compile_expr(expr.operands[0], env)
            left_translated = repl.translated_string
            compile_expr(expr.operands[1], env)
            repl.translated_string = f"{left_translated} || {repl.translated_string}"
    else:
        raise ValueError(f"Unknown expression type: {expr}")

# Writes compiled string translated_string to a file <lineno>.cpp
def write_cpp_output(lineno: int) -> None:
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
