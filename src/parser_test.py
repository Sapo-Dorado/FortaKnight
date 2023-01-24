import parser

CONTRACTS = ["SafeMath", "Ownable","Pausable", "ERC20Basic", "ERC20","BasicToken","StandardToken","UpgradedStandardToken","TetherToken"]
TETHER_FUNCTIONS = ["TetherToken", "transfer", "transferFrom", "balanceOf", "approve", "allowance", "deprecate", "totalSupply", "issue", "redeem", "setParams"]

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


