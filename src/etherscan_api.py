import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_ETH = os.environ['ETHERSCAN_API_KEY']
API_KEY_POL = os.environ['POLYGONSCAN_API_KEY']

def getSourceCodeEth(address):
      # Input: address of contract
      # Output: only the source code of contract
      url = "https://api.etherscan.io/api?module=contract&action=getsourcecode&address=" + address + "&apikey=" + API_KEY_ETH
      r = requests.get(url)
      data = r.json()
      result = data.get("result")
      source = result[0].get("SourceCode")
      return source

def getContractInfo(address):
      # API documentation: https://docs.etherscan.io/api-endpoints/contracts 
      # Input: address of contract
      # Output: json of information of smart contract in format:
      # {
      # "status":"1",
      # "message":"OK",
      # "result":[
      #       {
      #       "SourceCode":""
      #       "ABI":""
      #       "ContractName":"DAO",
      #       "CompilerVersion":"v0.3.1-2016-04-12-3ad5e82",
      #       "OptimizationUsed":"1",
      #       "Runs":"200",
      #       "ConstructorArguments":"",
      #       "EVMVersion":"Default",
      #       "Library":"",
      #       "LicenseType":"",
      #       "Proxy":"0",
      #       "Implementation":"",
      #       "SwarmSource":""
      #       }
      # ]
      # }
      url = "https://api.etherscan.io/api?module=contract&action=getsourcecode&address=" + address + "&apikey=" + API_KEY_ETH
      r = requests.get(url)
      data = r.json()
      return data


def checkContractStatus(address):
      # Input: transaction address
      # Output: status code of contract execution in format:
      # {
      # "status":"1",
      # "message":"OK",
      # "result":{
      #       "isError":"1",
      #       "errDescription":"Bad jump destination"
      # }
      # }
      url = "https://api.etherscan.io/api?module=transaction&action=getstatus&txhash=" + address + "&apikey=" + API_KEY_ETH
      results = requests.get(url)
      data = results.json()
      return data

def getSourceCodePoly(address):
      url = "https://api.polygonscan.com/api?module=contract&action=getsourcecode&address=" + address + "&apikey=" + API_KEY_POL
      r = requests.get(url)
      data = r.json()
      result = data.get("result")
      source = result[0].get("SourceCode")
      return source