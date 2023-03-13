from src.parser import Detector
import src.parser as parser

CONTRACTS = ["SafeMath", "Ownable","Pausable", "ERC20Basic", "ERC20","BasicToken","StandardToken","UpgradedStandardToken","TetherToken"]
TETHER_FUNCTIONS = ["TetherToken", "transfer", "transferFrom", "balanceOf", "approve", "allowance", "deprecate", "totalSupply", "issue", "redeem", "setParams"]

class IfStatementDetector(Detector):
  class IfStatementVisitor:
    def __init__(self):
      self.has_if = False

    def visitIfStatement(self, node):
      self.has_if = True

  def analyze(self, ast):
    visitor = self.IfStatementVisitor()
    parser.visit(ast, visitor)
    return visitor.has_if
  def alert(self):
    return "If statement detected"
  def alert_id(self):
    return "IF-STATEMENT"
    


class TestParser:
  def test_parse_parses_contracts(self):
    text = ""
    with open("./src/contracts/TetherToken.sol", 'r') as f:
      text = f.read()
    ast = parser.parse(text)
    contracts = parser.getContracts(ast)
    names = [c.name for c in contracts]
    for contract_name in CONTRACTS:
      assert(contract_name in names)

  def test_parse_file_parses_contracts(self):
    ast = parser.parse_file("./src/contracts/TetherToken.sol")
    contracts = parser.getContracts(ast)
    names = [c.name for c in contracts]
    for contract_name in CONTRACTS:
      assert(contract_name in names)

  def test_parse_parses_functions(self):
    text = ""
    with open("./src/contracts/TetherToken.sol", 'r') as f:
      text = f.read()
    ast = parser.parse(text)
    contracts = parser.getContracts(ast)
    contract = None
    for c in contracts:
      if c.name == "TetherToken":
        contract = c
        break
    functions = parser.getFunctions(contract)
    names = [f.name for f in functions]
    for fn_name in TETHER_FUNCTIONS:
      assert(fn_name in names)

  def test_helpers(self):
    ast = parser.parse_file("./src/contracts/Test.sol")
    contract = parser.getContracts(ast)[0]
    function = parser.getFunctions(contract)[0]
    parameters = parser.getParameters(function)
    statements = parser.getStatements(parser.getBody(function))
    assert(len(parameters) == 2)
    assert(parameters[0].name == "x")
    assert(len(statements) == 1)
    assert(statements[0].type == "IfStatement")
  
  def test_detector(self):
    detector = IfStatementDetector()
    no_if_result = detector.check_file("./src/contracts/NoIfStatements.sol")
    if_result = detector.check_file("./src/contracts/Test.sol")
    assert(if_result and not no_if_result)
    




