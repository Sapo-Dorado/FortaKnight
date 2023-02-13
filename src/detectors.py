from src.parser import Detector
import src.parser as parser

class BalanceRemovalDetector(Detector):
  class TransferVisitor:
    def __init__(self):
      self.transfers = []
    def visitFunctionCall(self, node):
      if(node.expression.type == "MemberAccess" and node.expression.memberName == "transfer"):
        self.transfers.append(node)
  
  class BalanceVisitor:
    def __init__(self):
      self.foundBalance = False

    def visitMemberAccess(self, node):
      if node.memberName == "balance":
        self.foundBalance = True

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
      if node.name == "selfdestruct":
        self.foundSelfDestruct = True

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
      if(node.right.type == "NumberLiteral"):
        self.foundConstant = True
      elif(node.left.type == "NumberLiteral"):
        self.foundConstant = True
    
  def analyze(self, ast):
    chipsSquadVisitor = self.ChipsSquadVisitor()
    parser.visit(ast, chipsSquadVisitor)

    if(chipsSquadVisitor.foundConstant):
      return True
    return False

from src.parser import Detector
import src.parser as parser

class BalanceRemovalDetector(Detector):
  class TransferVisitor:
    def __init__(self):
      self.transfers = []
    def visitFunctionCall(self, node):
      if(node.expression.type == "MemberAccess" and node.expression.memberName == "transfer"):
        self.transfers.append(node)
  
  class BalanceVisitor:
    def __init__(self):
      self.foundBalance = False

    def visitMemberAccess(self, node):
      if node.memberName == "balance":
        self.foundBalance = True

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
      if node.name == "selfdestruct":
        self.foundSelfDestruct = True

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
      if(node.right.type == "NumberLiteral"):
        self.foundConstant = True
      elif(node.left.type == "NumberLiteral"):
        self.foundConstant = True
    
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
      if((node.eventCall.type == "FunctionCall") and (node.eventCall.expression.type == "Identifier") and (node.eventCall.expression.name == "Transfer")):
        arguments = node.eventCall.arguments
        if(arguments[1]):
          if((arguments[1].type == "FunctionCall") and (arguments[1].expression.type == "ElementaryTypeName") and (arguments[1].expression.name == "address")):
            subargument = arguments[1].arguments
            if(subargument):
              if((subargument[0].type == "NumberLiteral") and (subargument[0].number == "0")):
                self.foundTransfer_to_NullAddress = True
  
  def analyze(self, ast):
    NATVisitor = self.NullAddressTransferVisitor()
    parser.visit(ast, NATVisitor)

    if(NATVisitor.foundTransfer_to_NullAddress):
      return True
    return False
