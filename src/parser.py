from abc import ABC, abstractmethod
from solidity_parser import parser

class Detector(ABC):
  def check(self, text):
    ast = parser.parse(text)
    return self.analyze(ast)

  def check_file(self, file):
    ast = parser.parse_file(file)
    return self.analyze(ast)
  
  #Should return a bool
  @abstractmethod
  def analyze(self, ast):
    return False

def parse_file(file):
  return parser.parse_file(file, loc=False)

def parse(text):
  return parser.parse(text, loc=False)

def visit(ast, visitor):
  parser.visit(ast, visitor)

def getContracts(root):
  contracts = []
  for n in root.children:
    if(n.type == "ContractDefinition"):
      contracts.append(n)
  return contracts

def getFunctions(contract):
  functions = []
  for v in contract.subNodes:
    if(v.type == "FunctionDefinition"):
      functions.append(v)
  return functions

def getParameters(function):
  parameters = []
  for p in function.parameters.parameters:
    parameters.append(p)
  return parameters

def getBody(function):
  return function.body

def getStatements(block):
  statements = []
  for statement in block.statements:
    statements.append(statement)
  return statements
