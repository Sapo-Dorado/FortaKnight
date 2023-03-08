from src.parser import Detector
import src.parser as parser
import src.etherscan_api as etherscan
import re

class BalanceRemovalDetector(Detector):
  class TransferVisitor:
    def __init__(self):
      self.transfers = []
    def visitFunctionCall(self, node):
      try:
        if(node.expression.type == "MemberAccess" and node.expression.memberName == "transfer"):
          self.transfers.append(node)
      except:
        pass
  
  class BalanceVisitor:
    def __init__(self):
      self.foundBalance = False

    def visitMemberAccess(self, node):
      try:
        if node.memberName == "balance":
          self.foundBalance = True
      except:
        pass

  def analyze(self, ast):
    transferVisitor = self.TransferVisitor()
    parser.visit(ast, transferVisitor)

    balanceVisitor = self.BalanceVisitor()
    for t in transferVisitor.transfers:
      parser.visit(t, balanceVisitor)
      if(balanceVisitor.foundBalance):
        return True
    return False
  
  def alert(self):
    return "Balance Removal Detected: contract at address {} contains a function has the ability to extract the entire balance of the contract"
  
  
class SelfDestructDetector(Detector):
  class SelfDestructVisitor:
    def __init__(self):
      self.foundSelfDestruct = False
      
    def visitIdentifier(self, node):
      try:
        if node.name == "selfdestruct":
          self.foundSelfDestruct = True
      except:
        pass

  def analyze(self, ast):
    selfDestructVisitor = self.SelfDestructVisitor()
    parser.visit(ast, selfDestructVisitor)
    
    if selfDestructVisitor.foundSelfDestruct:
      return True
    return False

  def alert(self):
    return "Self Destruct Detected: contract at address {} contains a function has the ability to self destruct the contract"
  
class TokenBurningDetector(Detector):
  class NullAddressTransferVisitor:
    def __init__(self):
      self.foundBurn = False
    
    def visitEmitStatement(self, node):#Detecting for the statement emit Transfer(from, to, amount); where to = address(0)
      try:
        if((node.eventCall.type == "FunctionCall") and (node.eventCall.expression.type == "Identifier") and (node.eventCall.expression.name == "Transfer")):
          arguments = node.eventCall.arguments
          if(arguments[1]):
            if((arguments[1].type == "FunctionCall") and (arguments[1].expression.type == "ElementaryTypeName") and (arguments[1].expression.name == "address")):
              subargument = arguments[1].arguments
              if(subargument):
                if((subargument[0].type == "NumberLiteral") and (subargument[0].number == "0")):
                  self.foundBurn = True
      except:
        pass

    #Picks up emit statments
    def visitFunctionCall(self, node):
      try:
        if(node.expression.name == "burn" or node.expression.name == "Burn"):
          self.foundBurn = True
      except:
        pass
  
  def analyze(self, ast):
    NATVisitor = self.NullAddressTransferVisitor()
    parser.visit(ast, NATVisitor)

    return NATVisitor.foundBurn
  
  def alert(self):
    return "Burn Function Detected: contract at address {} contains a function that can burn tokens"

class HiddenMintDetector(Detector): 
    
    
  def analyze(self, ast):
    hiddenMintVisitor = self.HiddenMintVisitor()
    parser.visit(ast, hiddenMintVisitor)


    if(hiddenMintVisitor.foundModified):
      return True
    return False


class HiddenMintDetector(Detector):
  class TotalSupplyModificationVisitor:
    def __init__(self):
      self.foundModified = False

    def visitMemberAccess(self, node):
      try:
        if((node.expression.name == "_totalSupply") and (node.memberName == "add")) :
          self.foundModified = True
      except:
        pass

    def visitBinaryOperation(self, node):
      try:
        if(node.operator == "=" and node.left.name == "_totalSupply"): 
          if(node.right.type == "BinaryOperation"):
            if(node.right.operator == "+" ):
              if(node.right.left.type == "Identifier"):
                if(node.right.left.name == "_totalSupply"):
                  self.foundModified = True
              elif(node.right.right.type == "Identifier"):
                if(node.right.right.name == "_totalSupply"): 
                  self.foundModified = True
      except:
        pass
  class FromNullAddressTransferVisitor:
    def __init__(self):
      self.foundTransfer_from_NullAddress = False
    
    def visitEmitStatement(self, node):#Detecting for the statement emit Transfer(from, to, amount); where from = address(0)
      try:
        if((node.eventCall.type == "FunctionCall") and (node.eventCall.expression.type == "Identifier") and (node.eventCall.expression.name == "Transfer")):
          arguments = node.eventCall.arguments
          if((arguments[0].type == "FunctionCall") and (arguments[0].expression.type == "ElementaryTypeName") and (arguments[0].expression.name == "address")):
            subargument = arguments[0].arguments
            if((subargument[0].type == "NumberLiteral") and (subargument[0].number == "0")):
              self.foundTransfer_from_NullAddress = True
      except:
        pass
  
  def analyze(self, ast):
    nullAddressTransferVisitor = self.FromNullAddressTransferVisitor()
    parser.visit(ast, nullAddressTransferVisitor)

    supplyVisitor = self.TotalSupplyModificationVisitor()
    parser.visit(ast, supplyVisitor)


    if(supplyVisitor.foundModified):
      return True

    if(nullAddressTransferVisitor.foundTransfer_from_NullAddress):
      return True

    return False

  def alert(self):
    return "Mint Function Detected: contract at address {} contains a function that can mint tokens"
def processContract(chain_id, address):
  detectors_list = [BalanceRemovalDetector(), SelfDestructDetector(),TokenBurningDetector(),HiddenMintDetector()]
  findings = []
  sourceCode = ""
  if(chain_id == 1):
    sourceCode = etherscan.getSourceCodeEth(address)
  elif (chain_id == 137):
    sourceCode = etherscan.getSourceCodePoly(address)
  sourceCode = re.sub(r'{\s*value:.*?}', '', sourceCode)
  try:
    for detector in detectors_list:
      if(detector.check(sourceCode)):
        findings.append(detector.alert().format(str(address)))
  except:
    pass
  return findings
