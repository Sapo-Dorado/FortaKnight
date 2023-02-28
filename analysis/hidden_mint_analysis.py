from collections import defaultdict
from src.detectors import *
import os

contract_dir = "./analysis/Hidden_Mints"

hiddenMint = HiddenMintDetector()
hiddenMint2 = ChipsSquadDetector()

counts = 0
total = 0

print("Starting analysis...")

files = os.listdir(contract_dir)
for filename in files:
  print(f"analyzing file {total}")
  total += 1
  if(hiddenMint2.check_file(f"{contract_dir}/{filename}")):
    # hiddenMint2.check_file(f"{contract_dir}/{filename}")):
    counts += 1

print("Analysis completed!")
print(f"Hidden Mints: {counts}/{total}")