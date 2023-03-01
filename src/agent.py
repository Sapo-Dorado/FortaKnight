from forta_agent import Finding, FindingType, FindingSeverity
from src.detectors import processContract

def handle_transaction(transaction_event):
    findings = []
    for address in transaction_event.addresses:
        for description in processContract(address):
            findings.append(Finding({
                'name': 'Suspicious Contract Code',
                'description': description,
                'alert_id': 'FORTAKNIGHT-1',
                'severity': FindingSeverity.Low,
                'type': FindingType.Info,
                'addresses': [address, transaction_event.from_],
                'metadata': {}
            }))
    return findings
