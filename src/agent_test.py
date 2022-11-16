from unittest.mock import Mock
from forta_agent import FindingSeverity, FindingType, create_transaction_event
from agent import handle_transaction, BLACKLISTED_ADDRESSES

VALID_ADDRESS = "0x58f3DB9d89eCC7c653F531689BCceD3937b797cc"



class TestHighTetherTransferAgent:
    def test_returns_empty_findings_if_no_tether_transfers(self):
        mock_tx_event = create_transaction_event({"transaction": {"from": VALID_ADDRESS}})

        findings = handle_transaction(mock_tx_event)

        assert len(findings) == 0

    def test_returns_finding_if_tether_transfer_over_10k(self):
        mock_tx_event = create_transaction_event({"transaction": {"from": BLACKLISTED_ADDRESSES[0]}})

        findings = handle_transaction(mock_tx_event)

        assert len(findings) == 1
        finding = findings[0]
        assert finding.name == "Suspicious Transaction"
        assert finding.description == f'Transaction from blacklisted address {BLACKLISTED_ADDRESSES[0]}'
        assert finding.alert_id == "FORTA-1"
        assert finding.severity == FindingSeverity.High
        assert finding.type == FindingType.Info
        assert finding.metadata['from'] == BLACKLISTED_ADDRESSES[0]
