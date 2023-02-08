from src.detectors import *

class TestBalanceRemovalDetector:
  def test_detects_malicious_contract(self):
    detector = BalanceRemovalDetector()
    assert(detector.check_file("./src/contracts/Falcon9SpaceXToken.sol"))
  
  def test_correctly_handles_normal_contracts(self):
    detector = BalanceRemovalDetector()
    assert(not detector.check_file("./src/contracts/TetherToken.sol"))

  def test_detects_hidden_mint_contract(self):
    detector = ChipsSquadDetector()
    assert(detector.check_file("./src/contracts/ChipsSquadTest.sol"))