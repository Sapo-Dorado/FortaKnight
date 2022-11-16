# FortaKnight Agent

## Description

This agent detects transactions with large Tether transfers

## Supported Chains

- Ethereum
- Any chain with addresses

## Alerts

Describe each of the type of alerts fired by this agent

- FORTAKNIGHT-1
  - Fired when a transaction is from a blacklisted address
  - Severity is always set to "high" 
  - Type is always set to "info"
  - from is the address that sent the transaction

## Test Data

The agent behaviour can be verified with the following transactions:

- 0xbfc0b941e0110b323a461208209f583656120dd754287c71603f2bf4d589fce7
