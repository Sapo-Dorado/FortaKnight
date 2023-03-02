from collections import defaultdict
from src.detectors import *
import os

contract_dir = "./analysis/Hidden_Mints"

hiddenMint1 = HiddenMintDetector()

counts = 0

total = 0

print("Starting analysis...")

files = os.listdir(contract_dir)
for filename in files:
  print(f"analyzing file {filename}")
  total += 1
  if(hiddenMint1.check_file(f"{contract_dir}/{filename}")):
    print("mint")
    counts += 1
  


print("Analysis completed!")
print(f"Hidden Mint: {counts}/{total}")