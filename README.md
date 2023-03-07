## FortaKnight Agent

## Description

This agent detects activity typically associated rug pulls

## Supported Chains

- Ethereum

## Alerts

- FORTAKNIGHT-1
  - Fired when one of our detectors detects activity typically associated rug pulls 
  - description explains the type of potential rug pull functionality detected
  - Severity is always set to "low" 
  - Type is always set to "info"
  - addresses includes the address of the contract and the deployer

## Test Data

The agent behaviour can be verified with the following transactions:

- 0x53d1c582bee01963953e458b4b74303a246cc9ede65647607ea1e007bcb9cb83
