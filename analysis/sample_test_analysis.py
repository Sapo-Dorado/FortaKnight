from collections import defaultdict
from src.detectors import *
import os

contract_dir = "./analysis/Testing_Samples"

detectors_list = [BalanceRemovalDetector(), SelfDestructDetector(),TokenBurningDetector(),HiddenMintDetector(),HiddenMintDetectorV2()]
detector_names = ["BalanceRemoval", "SelfDestruct", "TokenBurning", "HiddenMint", "HiddenMintV2"]

detector_counts = defaultdict(int)
detector_detectedFiles = defaultdict(list)
detector_undetectedFiles = defaultdict(list)

print("Starting analysis...")

files = os.listdir(contract_dir)
file_count = 0
for filename in files:
  print(f"analyzing file {file_count}: {filename}")
  file_count += 1
  for i in range(len(detectors_list)):
    if detectors_list[i].check_file(f"{contract_dir}/{filename}"):
      detector_counts[detector_names[i]] += 1
      detector_detectedFiles[detector_names[i]].append(filename)
    else:
      detector_undetectedFiles[detector_names[i]].append(filename)

def printResult(d_list, d_name, d_counts, fileCount):
  for i in range(len(d_list)):
    name = d_name[i]
    print(f"{name}: {d_counts[name]}/{fileCount}")

def printDetectedFiles(d_name,name_pos,d_detectedF):
  name = d_name[name_pos]
  filecount = 0
  for fileName in d_detectedF[name]:
    filecount+=1
    print(f"{filecount}: {name} detected {fileName}.")

def printUndetectedFiles(d_name,name_pos,d_undetectedF):
  name = d_name[name_pos]
  filecount = 0
  for fileName in d_undetectedF[name]:
    filecount+=1
    print(f"{filecount}: {name} did not detect {fileName}.")


print("Analysis completed!")
print(f"{file_count} files analysed.")

response = -2
while(response != -1):
  print("Analysis Menu:")
  print("Enter 0 to print the results.")
  print("Enter 1 to print the files detected by a detector.")
  print("Enter 2 to print the files NOT detected by a detector.")
  print("Enter -1 to exit the Analysis Menu.")
  response = input("Enter either 0, 1, 2, or -1: ")
  response = int(response)

  match response:
    case -1:
      exit
    case 0:
      print("Results:")
      printResult(detectors_list, detector_names, detector_counts, file_count)
    case 1:
      print("Enter 0 to print the files detected by detector BalanceRemoval")
      print("Enter 1 to print the files detected by detector SelfDestruct")
      print("Enter 2 to print the files detected by detector TokenBurning")
      print("Enter 3 to print the files detected by detector HiddenMint")
      print("Enter 4 to print the files detected by detector HiddenMintV2")
      name_Index = input("Enter either 0, 1, 2, 3, or 4: ")
      name_Index = int(name_Index)
      if (name_Index == 0 or name_Index == 1 or name_Index == 2 or name_Index == 3 or name_Index == 4):
        printDetectedFiles(detector_names,name_Index,detector_detectedFiles)
      else:
        response = 1
    case 2:
      print("Enter 0 to print the files NOT detected by detector BalanceRemoval")
      print("Enter 1 to print the files NOT detected by detector SelfDestruct")
      print("Enter 2 to print the files NOT detected by detector TokenBurning")
      print("Enter 3 to print the files NOT detected by detector HiddenMint")
      print("Enter 4 to print the files NOT detected by detector HiddenMintV2")
      name_Index = input("Enter either 0, 1, 2, 3, or 4: ")
      name_Index = int(name_Index)
      if (name_Index == 0 or name_Index == 1 or name_Index == 2 or name_Index == 3 or name_Index == 4):
        printUndetectedFiles(detector_names,name_Index,detector_undetectedFiles)
      else:
        response = 2
    case _:
      response = 0
print("BYE")