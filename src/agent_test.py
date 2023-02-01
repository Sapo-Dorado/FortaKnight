from unittest.mock import Mock
from forta_agent import FindingSeverity, FindingType, create_transaction_event
from src.agent import handle_transaction, BLACKLISTED_ADDRESSES

VALID_ADDRESS1 = "0x58f3DB9d89eCC7c653F531689BCceD3937b797cc"
VALID_ADDRESS2 = "0x58f3DB9d89eCC7c653F531689BCceD3937b797cd"



class TestHighTetherTransferAgent:
    def test_returns_empty_findings_if_from_and_to_not_in_blacklist(self):
        mock_tx_event = create_transaction_event({"transaction": {"from": VALID_ADDRESS1, "to": VALID_ADDRESS2}})

        findings = handle_transaction(mock_tx_event)

        assert len(findings) == 0

    def test_returns_finding_if_from_in_blacklist(self):
        mock_tx_event = create_transaction_event({"transaction": {"from": BLACKLISTED_ADDRESSES[0], "to": VALID_ADDRESS1}})

        findings = handle_transaction(mock_tx_event)

        assert len(findings) == 1
        finding = findings[0]
        assert finding.name == "Suspicious Transaction"
        assert finding.description == f'Transaction involving blacklisted address {BLACKLISTED_ADDRESSES[0]}'
        assert finding.alert_id == "FORTAKNIGHT-1"
        assert finding.severity == FindingSeverity.High
        assert finding.type == FindingType.Info
        assert finding.metadata['addr'] == BLACKLISTED_ADDRESSES[0]

    def test_returns_finding_if_to_in_blacklist(self):
        mock_tx_event = create_transaction_event({"transaction": {"from": VALID_ADDRESS1, "to": BLACKLISTED_ADDRESSES[0]}})

        findings = handle_transaction(mock_tx_event)

        assert len(findings) == 1
        finding = findings[0]
        assert finding.name == "Suspicious Transaction"
        assert finding.description == f'Transaction involving blacklisted address {BLACKLISTED_ADDRESSES[0]}'
        assert finding.alert_id == "FORTAKNIGHT-1"
        assert finding.severity == FindingSeverity.High
        assert finding.type == FindingType.Info
        assert finding.metadata['addr'] == BLACKLISTED_ADDRESSES[0]
