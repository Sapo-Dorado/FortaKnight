from collections import defaultdict
import src.etherscan_api as etherscan
from src.detectors import *
import re

detectors_list = [BalanceRemovalDetector(), SelfDestructDetector(),ChipsSquadDetector(),TokenBurningDetector(),HiddenMintDetector()]
detector_names = ["BalanceRemoval", "SelfDestruct", "ChipsSquad", "TokenBurning", "HiddenMint"]

print("Starting analysis...")

success_count = 0
results = defaultdict(int)
with open("./analysis/MaliciousContractAddresses.txt") as f:
  count = 0
  for line in f.readlines():
    try:
      print(f"Analyzing contract {count}")
      sourceCode = etherscan.getSourceCode(line.strip())
      contractCode = re.sub(r'{value:.*?}', '', sourceCode)
      for i,detector in enumerate(detectors_list):
        if(detector.check(contractCode)):
          results[detector_names[i]] += 1
      print(f"Contract {count} completed successfully")
      success_count += 1
    except:
      print(f"Contract {count} failed :(")
    count += 1
print("Completed analysis!!!")


for name in results:
  print(f"{name} detected {results[name]}/{success_count} vulnerable tokens")