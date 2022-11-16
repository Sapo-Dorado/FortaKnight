from forta_agent import Finding, FindingType, FindingSeverity

ERC20_TRANSFER_EVENT = '{"name":"Transfer","type":"event","anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}]}'
TETHER_ADDRESS = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
TETHER_DECIMALS = 6

#Update this to be accurate
HIGH_GAS_PRICE = 13080000000
findings_count = 0


def handle_transaction(transaction_event):
    findings = []

    # limiting this agent to emit only 5 findings so that the alert feed is not spammed
    global findings_count
    if findings_count >= 5:
        return findings
    gas_price = transaction_event.gas_price
    if gas_price > HIGH_GAS_PRICE:
        findings.append(Finding({
            'name': 'High Gas Cost Transaction',
            'description': f'High Gas cost {gas_price / 10**9}',
            'alert_id': 'FORTA-1',
            'severity': FindingSeverity.Low,
            'type': FindingType.Info,
            'metadata': {
                'from_': transaction_event.from_,
            }
        }))
        findings_count += 1
# 
    return findings
