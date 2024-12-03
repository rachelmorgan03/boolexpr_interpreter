from dataclasses import dataclass, field
from typing import Union, List

# EBNF grammar
# <program>      : ( <declarations> , <expr> )
# <declarations> : [ ]
# <declarations> : [ <varlist> ]
# <varlist>      : <var>
# <varlist>      : <var> , <varlist>
# <expr>         : <expr> & <expr>
# <expr>         : <expr> | <expr>
# <expr>         : ~ <expr>
# <expr>         : <literal>
# <expr>         : <var>
# <literal>      : t
# <literal>      : f
# <var>          : a...z     but not t or f obviously

@dataclass
class Literal:
   value: bool  # Represents a boolean literal (e.g., True/False)

   def __str__(self):
      return 't' if self.value else 'f'

@dataclass
class Variable:
   name: str  # Represents a variable; should be a single character
    
   def __post_init__(self):
      if len(self.name) != 1:
         raise ValueError("Variable name must be a single character.")

   def __str__(self):
       return self.name

@dataclass
class Operator:
   # Operator type, e.g., '&', '|', '~'; should be a single character
   operator: str
   # Recursively holds BoolExp Nodes
   operands: List['BoolExp'] = field(default_factory=list)
    
   def __post_init__(self):
      if len(self.operator) != 1:
         raise ValueError("Operator must be a single character.")

   def __str__(self):
      if self.operator == '~':  # Unary operator
         return f"{self.operator}{self.operands[0]}"
      else:  # Binary operators
         return f"({f' {self.operator} '.join(map(str, self.operands))})"

# BoolExprNodeType is defined as a union of the possible node types
BoolExpr = Union[Literal, Variable, Operator]

# The function to convert abstract syntax tree to concrete expression
def abstract2concrete(expr: BoolExpr) -> str:
   return str(expr)