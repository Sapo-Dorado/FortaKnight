from collections import defaultdict
from src.detectors import *
import os

contract_dir = "./analysis/Contracts"

detectors_list = [BalanceRemovalDetector(), SelfDestructDetector()]
detector_names = ["BalanceRemoval", "SelfDestruct"]
detector_counts = defaultdict(int)

print("Starting analysis...")

files = os.listdir(contract_dir)
file_count = 0
for filename in files:
  file_count += 1
  for i in range(len(detectors_list)):
    if detectors_list[i].check_file(f"{contract_dir}/{filename}"):
      detector_counts[detector_names[i]] += 1

print("Analysis completed!")
print("Results:")
for i in range(len(detectors_list)):
  name = detector_names[i]
  print(f"{name}: {detector_counts[name]}/{file_count}")

