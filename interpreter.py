from BoolExprADT import *
import repl
import boolexpr1

def eval1(expr: BoolExpr, env: dict = None) -> bool:
    if isinstance(expr, Literal):
        return expr.value
    elif isinstance(expr, Variable):
        return env.get(expr.name, False)  # Default to False if undefined
    elif isinstance(expr, Operator):
        if expr.operator == '~':
            return not eval1(expr.operands[0], env)
        elif expr.operator == '&':
            return eval1(expr.operands[0], env) and eval1(expr.operands[1], env)
        elif expr.operator == '|':
            return eval1(expr.operands[0], env) or eval1(expr.operands[1], env)
