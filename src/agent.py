from forta_agent import Finding, FindingType, FindingSeverity, Network
from src.detectors import processContract
import rlp
from datetime import datetime, timedelta
from web3 import Web3

cache = []

def calc_contract_address(address, nonce):

    address_bytes = bytes.fromhex(address[2:].lower())
    return Web3.toChecksumAddress(Web3.keccak(rlp.encode([address_bytes, nonce]))[-20:])


def handle_transaction(transaction_event):
    chain_id = 1 if transaction_event.network == Network.MAINNET else 137
    if transaction_event.to is None:
        cache.append({
            "address": calc_contract_address(transaction_event.from_, transaction_event.transaction.nonce).lower(),
            "from": transaction_event.from_,
            "timestamp": transaction_event.timestamp,
            "hash": transaction_event.transaction.hash,
            "chain_id": chain_id
        })
    return handle_cached_transactions()

def handle_cached_transactions():
    global cache
    findings = []
    while(len(cache) > 0 and datetime.now() - datetime.fromtimestamp(cache[0]["timestamp"]) > timedelta(minutes=5)):
        for alert_id, description in processContract(cache[0]["chain_id"], cache[0]["address"]):
            findings.append(Finding({
                'name': 'Suspicious Contract Code',
                'description': description,
                'alert_id': alert_id,
                'severity': FindingSeverity.Low,
                'type': FindingType.Info,
                'metadata': {
                    "transaction_hash": cache[0]["hash"],
                    "contract_address": cache[0]["address"],
                    "deployer": cache[0]["from"]
                }
            }))
        cache = cache[1:]
    return findings
