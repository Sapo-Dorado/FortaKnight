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
        
  class SelfDestructVisitor:
    def __init__(self):
      self.foundSelfDestruct = False
      
    def visitIdentifier(self, node):
      if node.name == "selfdestruct":
        self.foundSelfDestruct = True

  def analyze(self, ast):
    transferVisitor = self.TransferVisitor()
    parser.visit(ast, transferVisitor)
    
    selfDestructVisitor = self.SelfDestructVisitor()
    parser.visit(ast, selfDestructVisitor)

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
  