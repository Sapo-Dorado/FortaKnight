import src.etherscan_api as etherscan
import src.parser as parser
import os

print("Starting.....")
contract_dir = "./analysis/Contracts"

with open("./analysis/ContractAddresses.txt") as f:
  count = 0
  for line in f.readlines():
    with open(f"{contract_dir}/contract_{count}.sol", "x") as write_file:
      write_file.write(etherscan.getSourceCode(line.strip()))
      count += 1

file_count = 0
files = os.listdir(contract_dir)
for filename in files:
  with open(f"{contract_dir}/{filename}") as f:
    if(len(f.readlines()) == 0):
      os.remove(f"{contract_dir}/{filename}")
      continue
    print(filename)
    parser.parse_file(f"{contract_dir}/{filename}")
    file_count += 1

print(f"{file_count} contracts downloaded")
print("Done!")