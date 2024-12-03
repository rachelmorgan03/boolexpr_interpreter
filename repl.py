import re
from BoolExprADT import *
import boolexpr1
from interpreter import eval1
from compiler import compile_expr, write_cpp_output

translated_string = ""

def concrete2abstract(s: str, parser) -> BoolExpr:
   pattern = re.compile("[^ \t]+")
   if pattern.search(s):
      try:
         parser.parse(s)
         return boolexpr1.global_ast
      except Exception as e:
         print ("Unknown Error occurred "
                "(this is normally caused by a syntax error)")
         raise e
   return None

def main():
   import sys
   global parser
   global translated_string
   cFlag = False
   iFlag = False
   args = sys.argv[1:]

   lineno = 0

   # Parse command-line arguments for -c or -i options
   for arg in args:
      if arg == '-c':
         cFlag = True
         boolexpr1.translated_string = ""
      elif arg == '-i':
         iFlag = True
      else:
         print(f"Invalid option: {arg}")
         sys.exit(1)

   if len(sys.argv) == 2 and sys.argv[1] == '-i':
      print('BoolExpr> ', flush=True, end='')

   for line in sys.stdin:
      line = line[:-1]   # remove trailing newline
      #line = line.strip()   # remove trailing newline
      try:
         ast = concrete2abstract(line,boolexpr1.parser)
         if ast:
            # for debugging purposes
            #print('"{}" is a program'.format(line))
            #print("AST:", ast)
            #print(abstract2concrete(ast))

            # for debugging purposes
            #if eval1(ast):
            #   print(" is true.")
            #else:
            #   print(" is false.")

            if not(cFlag):
               # Interpret the expression by default
               print(eval1(ast,boolexpr1.true_vars))

            # Compile the expression because -c flag is on
            else:
               lineno = lineno + 1
               compile_expr(ast,boolexpr1.true_vars)
               write_cpp_output(lineno)
            translated_string = ""
            boolexpr1.true_vars = {}
            boolexpr1.false_vars = {}
         else:
            print('"{}" is not a program'.format(line))

         if len(sys.argv) == 2 and sys.argv[1] == '-i':
            print('BoolExpr> ', flush=True, end='')
      except SyntaxError:
         print('"{}" contains lexical units which are not lexemes '
               'and, thus, is not a program.'.format(line))
      except EOFError:
         sys.exit(0)
      except Exception as e:
         print(e)
         sys.exit(-1)
