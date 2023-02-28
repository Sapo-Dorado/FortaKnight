from src.parser import Detector
import src.parser as parser

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
  
class ChipsSquadDetector(Detector): 
  class ChipsSquadVisitor:
    def __init__(self):
      self.foundConstant = False

    def visitBinaryOperation(self, node):
      try:
        if(node.right.type == "NumberLiteral"):
          self.foundConstant = True
        elif(node.left.type == "NumberLiteral"):
          self.foundConstant = True
      except:
        pass
    
  def analyze(self, ast):
    chipsSquadVisitor = self.ChipsSquadVisitor()
    parser.visit(ast, chipsSquadVisitor)

    if(chipsSquadVisitor.foundConstant):
      return True
    return False

class TokenBurningDetector(Detector):
  class NullAddressTransferVisitor:
    def __init__(self):
      self.foundTransfer_to_NullAddress = False
    
    def visitEmitStatement(self, node):#Detecting for the statement emit Transfer(from, to, amount); where to = address(0)
      try:
        if((node.eventCall.type == "FunctionCall") and (node.eventCall.expression.type == "Identifier") and (node.eventCall.expression.name == "Transfer")):
          arguments = node.eventCall.arguments
          if(arguments[1]):
            if((arguments[1].type == "FunctionCall") and (arguments[1].expression.type == "ElementaryTypeName") and (arguments[1].expression.name == "address")):
              subargument = arguments[1].arguments
              if(subargument):
                if((subargument[0].type == "NumberLiteral") and (subargument[0].number == "0")):
                  self.foundTransfer_to_NullAddress = True
      except:
        pass
  
  def analyze(self, ast):
    NATVisitor = self.NullAddressTransferVisitor()
    parser.visit(ast, NATVisitor)

    if(NATVisitor.foundTransfer_to_NullAddress):
      return True
    return False

class HiddenMintDetector(Detector): 
  class HiddenMintVisitor:
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
    
  def analyze(self, ast):
    hiddenMintVisitor = self.HiddenMintVisitor()
    parser.visit(ast, hiddenMintVisitor)


    if(hiddenMintVisitor.foundModified):
      return True
    return False

class HiddenMintDetectorV2(Detector):
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
    MintDetectorV2 = self.FromNullAddressTransferVisitor()
    parser.visit(ast, MintDetectorV2)

    if(MintDetectorV2.foundTransfer_from_NullAddress):
      return True
    return False
