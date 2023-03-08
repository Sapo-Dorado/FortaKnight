from unittest.mock import patch, Mock
import src.etherscan_api as etherscan

class TestEtherscanApi:
    def test_get_source_code(self):
        mock_response = {
                        'status':'1', 
                        'message':'OK',
                        'result':[
                            {
                            "SourceCode":"Mock_Source_Code",
                            "ABI":"[Mock_ABI:Value]",
                            "ContractName":"Mock",
                            "CompilerVersion":"v0.3.1-2016-04-12-3ad5e82",
                            "OptimizationUsed":"1",
                            "Runs":"200",
                            "ConstructorArguments":"0001",
                            "EVMVersion":"Default",
                            "Library":"",
                            "LicenseType":"",
                            "Proxy":"0",
                            "Implementation":"",
                            "SwarmSource":""
                            }
                        ]
                    }
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = mock_response
            address = "0xb429dA13f0Bf08962c26e44Ba34627e7b0E560F6"

            source = etherscan.getSourceCodeEth(address)

        assert(source == "Mock_Source_Code")

            























