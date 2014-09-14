# Base class for all expression nodes.
class ExpressionNode(object):
   pass

# Expression class for numeric literals like "1.0".
class NumberExpressionNode(ExpressionNode):
   def __init__(self, value):
      self.value = value

# Expression class for referencing a variable, like "a".
class VariableExpressionNode(ExpressionNode):
   def __init__(self, name):
      self.name = name

# Expression class for a binary operator.
class BinaryOperatorExpressionNode(ExpressionNode):
   def __init__(self, operator, left, right):
      self.operator = operator
      self.left = left
      self.right = right

# Expression class for function calls.
class CallExpressionNode(ExpressionNode):
   def __init__(self, callee, args):
      self.callee = callee
      self.args = args

# This class represents the "prototype" for a function, which captures its name,
# and its argument names (thus implicitly the number of arguments the function
# takes).
class PrototypeNode(object):
   def __init__(self, name, args):
      self.name = name
      self.args = args

# This class represents a function definition itself.
class FunctionNode(object):
   def __init__(self, prototype, body):
      self.prototype = prototype
      self.body = body