import requests
import sys


class EtherscanAPI:
      def getSourceCode(self, address):
            # Input: address of contract
            # Output: only the source code of contract
            url = "https://api.etherscan.io/api?module=contract&action=getsourcecode&address=" + address + "&apikey=" + apikey
            r = requests.get(url)
            data = r.json()
            result = data.get("result")
            source = result[0].get("SourceCode")
            return source

      def getContractInfo(self, address):
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
            url = "https://api.etherscan.io/api?module=contract&action=getsourcecode&address=" + address + "&apikey=" + apikey
            r = requests.get(url)
            data = r.json()
            return data


      def checkContractStatus(self, address):
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
            url = "https://api.etherscan.io/api?module=transaction&action=getstatus&txhash=" + address + "&apikey=" + apikey
            results = requests.get(url)
            data = results.json()
            return data

      apikey = "dummy"


address = "0xb429dA13f0Bf08962c26e44Ba34627e7b0E560F6"
txhash = "0x23b041759e63947fc643eb68cff1d4e6c6a1064a6878633811450dc0e6fb2500"

