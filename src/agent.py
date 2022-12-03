from forta_agent import Finding, FindingType, FindingSeverity

#Update this to be accurate
BLACKLISTED_ADDRESSES = ["0x5c1fe6f340dd36b5daf88c2cf390bf715d2af139","0x15fe7ce21b181a4706063b31e5c968477c7a00cc", "0xb95f4d5529e3adcc10447d7e6797424edd1c701d"]

def handle_transaction(transaction_event):
    findings = []
    from_ = transaction_event.from_
    to = transaction_event.to
    alert = False
    addr = ""
    if (from_ in BLACKLISTED_ADDRESSES):
        alert = True
        addr = from_
    elif (to in BLACKLISTED_ADDRESSES):
        alert = True
        addr = to
    if alert:
        findings.append(Finding({
            'name': 'Suspicious Transaction',
            'description': f'Transaction involving blacklisted address {addr}',
            'alert_id': 'FORTAKNIGHT-1',
            'severity': FindingSeverity.High,
            'type': FindingType.Info,
            'metadata': {
                'addr': addr,
            }
        }))
    return findings
