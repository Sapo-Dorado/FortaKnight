from collections import defaultdict
from src.detectors import *
import os

contract_dir = "./analysis/Hidden_Burns"

hiddenMint = HiddenMintDetector()

counts = 0
total = 0

print("Starting analysis...")

files = os.listdir(contract_dir)
for filename in files:
  print(f"analyzing file {filename}")
  total += 1
  if(hiddenMint.check_file(f"{contract_dir}/{filename}")):
    counts += 1

print("Analysis completed!")
print(f"Hidden Burns: {counts}/{total}")