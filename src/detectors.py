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
      
    def visitSDAccess(self, node):
      if node.memberName == "SelfDestruct":
        self.foundSelfDestruct = True

  def analyze(self, ast):
    transferVisitor = self.TransferVisitor()
    parser.visit(ast, transferVisitor)

    balanceVisitor = self.BalanceVisitor()
    for t in transferVisitor.transfers:
      parser.visit(t, balanceVisitor)
      if(balanceVisitor.foundBalance):
        return True
    return False
  