from BoolExprADT import *
import repl
import boolexpr1
'''
def eval1(expr: BoolExpr, env: dict = None) -> bool:
    if env is None:
        env = {}
    if isinstance(expr, Literal):
        return expr.value
    elif isinstance(expr, Variable):
      # Look up the value of the variable in the environment
      if expr.name in env:
         return env[expr.name]
      else:
         raise ValueError(f"Variable '{expr.name}' is not defined.")
    elif isinstance(expr, Operator):
        if expr.operator == '~':
            return not eval1(expr.operands[0], env)
        elif expr.operator == '&':
            return eval1(expr.operands[0], env) and eval1(expr.operands[1], env)
        elif expr.operator == '|':
            return eval1(expr.operands[0], env) or eval1(expr.operands[1], env)
    raise ValueError(f"Unknown expression type: {expr}")
'''

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