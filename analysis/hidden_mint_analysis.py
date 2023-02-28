from collections import defaultdict
from src.detectors import *
import os

contract_dir = "./analysis/Hidden_Mints"

hiddenMint1 = HiddenMintDetector()
hiddenMint2 = HiddenMintDetectorV2()

counts1 = 0
counts2 = 0
counts3 = 0

total = 0

print("Starting analysis...")

files = os.listdir(contract_dir)
for filename in files:
  print(f"analyzing file {filename}")
  total += 1
  if(hiddenMint1.check_file(f"{contract_dir}/{filename}")):
    counts1 += 1
  if(hiddenMint2.check_file(f"{contract_dir}/{filename}")):
    counts2 += 1
  


print("Analysis completed!")
print(f"Hidden Mint 1: {counts1}/{total}")
print(f"Hidden Mint 2: {counts2}/{total}")