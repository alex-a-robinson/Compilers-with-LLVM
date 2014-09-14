from ast import *
from tokenizer import *

class Parser(object):

   def __init__(self, tokens, binop_precedence):
      self.tokens = tokens
      self.binop_precedence = binop_precedence
      self.Next()

   # Provide a simple token buffer. Parser.current is the current token the
   # parser is looking at. Parser.Next() reads another token from the lexer and
   # updates Parser.current with its results.
   def Next(self):
      self.current = self.tokens.next()

   # Gets the precedence of the current token, or -1 if the token is not a binary
   # operator.
   def GetCurrentTokenPrecedence(self):
      if isinstance(self.current, CharacterToken):
         return self.binop_precedence.get(self.current.char, -1)
      else:
         return -1

   # identifierexpr ::= identifier | identifier '(' expression* ')'
   def ParseIdentifierExpr(self):
      identifier_name = self.current.name
      self.Next()  # eat identifier.


      if self.current != CharacterToken('('):  # Simple variable reference.
         return VariableExpressionNode(identifier_name)

      # Call.
      self.Next()  # eat '('.
      args = []
      if self.current != CharacterToken(')'):
         while True:
            args.append(self.ParseExpression())
            if self.current == CharacterToken(')'):
               break
            elif self.current != CharacterToken(','):
               raise RuntimeError('Expected ")" or "," in argument list.')
            self.Next()

      self.Next()  # eat ')'.
      return CallExpressionNode(identifier_name, args)

   # numberexpr ::= number
   def ParseNumberExpr(self):
      result = NumberExpressionNode(self.current.value)
      self.Next()  # consume the number.
      return result

   # parenexpr ::= '(' expression ')'
   def ParseParenExpr(self):
      self.Next()   # eat '('.

      contents = self.ParseExpression()

      if self.current != CharacterToken(')'):
         raise RuntimeError('Expected ")".')
      self.Next()  # eat ')'.

      return contents

   # primary ::= identifierexpr | numberexpr | parenexpr
   def ParsePrimary(self):
      if isinstance(self.current, IdentifierToken):
         return self.ParseIdentifierExpr()
      elif isinstance(self.current, NumberToken):
         return self.ParseNumberExpr()
      elif self.current == CharacterToken('('):
         return self.ParseParenExpr()
      else:
         raise RuntimeError('Unknown token when expecting an expression.')

   # binoprhs ::= (operator primary)*
   def ParseBinOpRHS(self, left, left_precedence):
      # If this is a binary operator, find its precedence.
      while True:
         precedence = self.GetCurrentTokenPrecedence()


         # If this is a binary operator that binds at least as tightly as the
         # current one, consume it; otherwise we are done.
         if precedence < left_precedence:
            return left

         binary_operator = self.current.char
         self.Next()  # eat the operator.

         # Parse the primary expression after the binary operator.
         right = self.ParsePrimary()

         # If binary_operator binds less tightly with right than the operator after
         # right, let the pending operator take right as its left.
         next_precedence = self.GetCurrentTokenPrecedence()
         if precedence < next_precedence:
            right = self.ParseBinOpRHS(right, precedence + 1)

         # Merge left/right.
         left = BinaryOperatorExpressionNode(binary_operator, left, right)

   # expression ::= primary binoprhs
   def ParseExpression(self):
      left = self.ParsePrimary()
      return self.ParseBinOpRHS(left, 0)

   # prototype ::= id '(' id* ')'
   def ParsePrototype(self):
      if not isinstance(self.current, IdentifierToken):
         raise RuntimeError('Expected function name in prototype.')


      function_name = self.current.name
      self.Next()  # eat function name.

      if self.current != CharacterToken('('):
         raise RuntimeError('Expected "(" in prototype.')
      self.Next()  # eat '('.

      arg_names = []
      while isinstance(self.current, IdentifierToken):
         arg_names.append(self.current.name)
         self.Next()

      if self.current != CharacterToken(')'):
         raise RuntimeError('Expected ")" in prototype.')

      # Success.
      self.Next()  # eat ')'.

      return PrototypeNode(function_name, arg_names)

   # definition ::= 'def' prototype expression
   def ParseDefinition(self):
      self.Next()  # eat def.
      proto = self.ParsePrototype()
      body = self.ParseExpression()
      return FunctionNode(proto, body)

   # toplevelexpr ::= expression
   def ParseTopLevelExpr(self):
      proto = PrototypeNode('', [])
      return FunctionNode(proto, self.ParseExpression())

   # external ::= 'extern' prototype
   def ParseExtern(self):
      self.Next()  # eat extern.
      return self.ParsePrototype()

   # Top-Level parsing
   def HandleDefinition(self):
      self.Handle(self.ParseDefinition, 'Parsed a function definition.')

   def HandleExtern(self):
      self.Handle(self.ParseExtern, 'Parsed an extern.')

   def HandleTopLevelExpression(self):
      self.Handle(self.ParseTopLevelExpr, 'Parsed a top-level expression.')

   def Handle(self, function, message):
      try:
         function()
         print message
      except Exception, e:
         print 'Error:', e
         try:
            self.Next()  # Skip for error recovery.
         except:
            pass