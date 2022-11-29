from forta_agent import Finding, FindingType, FindingSeverity

#Update this to be accurate
BLACKLISTED_ADDRESSES = ["0x5c1fe6f340dd36b5daf88c2cf390bf715d2af139","0x15FE7CE21B181a4706063B31E5c968477c7A00Cc"]

def handle_transaction(transaction_event):
    findings = []
    from_ = transaction_event.from_
    if from_ in BLACKLISTED_ADDRESSES:
        findings.append(Finding({
            'name': 'Suspicious Transaction',
            'description': f'Transaction from blacklisted address {from_}',
            'alert_id': 'FORTAKNIGHT-1',
            'severity': FindingSeverity.High,
            'type': FindingType.Info,
            'metadata': {
                'from': from_,
            }
        }))
    return findings
