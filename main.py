from tokenizer import *
from parser import *

def main():
   # Install standard binary operators.
   # 1 is lowest possible precedence. 40 is the highest.
   operator_precedence = {
       '<': 10,
       '+': 20,
       '-': 20,
       '*': 40
   }

   # Run the main "interpreter loop".
   while True:
      print 'ready>',
      try:
         raw = raw_input()
      except KeyboardInterrupt:
         return

      parser = Parser(Tokenize(raw), operator_precedence)
      while True:
         # top ::= definition | external | expression | EOF
         if isinstance(parser.current, EOFToken):
            break
         if isinstance(parser.current, DefToken):
            parser.HandleDefinition()
         elif isinstance(parser.current, ExternToken):
            parser.HandleExtern()
         else:
            parser.HandleTopLevelExpression()

if __name__ == '__main__':
   main()