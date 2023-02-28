import src.etherscan_api as etherscan
from src.detectors import *
import time


detectors_list = [BalanceRemovalDetector(), SelfDestructDetector(),ChipsSquadDetector(),TokenBurningDetector(),HiddenMintDetector()]
detector_names = ["BalanceRemoval", "SelfDestruct", "ChipsSquad", "TokenBurning", "HiddenMint"]

print("Starting analysis...")

success_count = 0
totalTime = 0
with open("./analysis/ContractAddresses.txt") as f:
  count = 0
  for line in f.readlines():
    try:
      print(f"Analyzing contract {count}")
      start = time.time()
      sourceCode = etherscan.getSourceCode(line.strip())
      for detector in detectors_list:
        detector.check(sourceCode)
      end = time.time()
      contractTime = end - start
      print(f"Contract {count} completed successfully in {contractTime}s")
      count += 1
      success_count += 1
      totalTime += contractTime
    except:
      print(f"Contract {count} failed :(")
print(f"{success_count} contracts analyzed successfully")
print(f"{totalTime}s of analysis have elapsed")
print(f"{totalTime/success_count}s taken to analyze each contract on average")
