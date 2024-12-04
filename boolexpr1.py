from repl import *
import ply.lex as lex
import ply.yacc as yacc
from BoolExprADT import *
from interpreter import eval1

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

#################### BEGIN Lexer/Scanner Specification ####################

# Token list
tokens = (
   'VAR',
   'T', 'F',
   'AND', 'OR', 'NOT',
   'LPAREN', 'RPAREN',
   'LBRACK', 'RBRACK',
   'COMMA'
)

# Token regex definitions
t_T = r't'
t_F = r'f'
t_VAR = r'[a-eg-su-z]'
t_AND = r'\&'
t_OR = r'\|'
t_NOT = r'~'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_COMMA = r','

# Ignore spaces and tabs
t_ignore = ' \t'

# Error handling for lexer
def t_error(t):
   raise SyntaxError(f"Illegal character/lexeme '{t.value[0]}'")
   #print(f"Illegal character/lexeme '{t.value[0]}'")
   t.lexer.skip(1)

#################### END Lexer/Scanner Specification ####################

# Build the lexer
lexer = lex.lex()

precedence = (
   ('left', 'OR'),
   ('left', 'AND'),
   ('right', 'NOT'),
)

true_vars = {}
false_vars = {}

#################### BEGIN Grammar Pattern-Action Rules ####################

global_ast = ""

# Grammar rules
def p_sentence(p):
    '''sentence : LPAREN declarations COMMA expr RPAREN'''
    global global_ast
    global_ast = p[4]  # Set the global AST to the parsed expression
    p[0] = global_ast

def p_declarations_empty(p):
    '''declarations : LBRACK RBRACK'''
    global true_vars
    p[0] = []

def p_declarations_varlist(p):
    '''declarations : LBRACK varlist RBRACK'''
    global true_vars
    p[0] = p[2]  # The list of variables is passed forward

def p_varlist_single(p):
    '''varlist : VAR'''
    global true_vars
    true_vars[p[1]] = True  # Add the variable as true
    p[0] = [Variable(p[1])]

def p_varlist_multiple(p):
    '''varlist : VAR COMMA varlist'''
    global true_vars
    true_vars[p[1]] = True  # Add the variable as true
    p[0] = [Variable(p[1])] + p[3]

def p_expr_literal(p):
    '''expr : T
            | F'''
    p[0] = Literal(p[1] == 't')

def p_expr_not(p):
    '''expr : NOT expr'''
    p[0] = Operator('~', [p[2]])

def p_expr_and(p):
    '''expr : expr AND expr'''
    p[0] = Operator('&', [p[1], p[3]])

def p_expr_or(p):
    '''expr : expr OR expr'''
    p[0] = Operator('|', [p[1], p[3]])

def p_expr_var(p):
    '''expr : VAR'''
    global true_vars, false_vars
    p[0] = Variable(p[1])
        
# Error rule for syntax errors
def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error at '{p.value}'")
    else:
        raise SyntaxError("Syntax error at EOF")

#################### END Grammar Pattern-Action Rules ####################

# Build the parser
parser = yacc.yacc()

# Function for checking if a variable is false
def false_var(var: str) -> bool:
   return var not in true_vars

# main entry point
if __name__ == "__main__":
   main()
