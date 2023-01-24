from solidity_parser import parser

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

def parse_file(file):
  return parser.parse_file(file, loc=False)

def parse(text):
  return parser.parse(text, loc=False)

