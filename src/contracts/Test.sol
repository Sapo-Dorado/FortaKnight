pragma solidity ^0.8.0;

contract Test {
  function testFunction(uint x, uint y) public returns (bool) {
    if(x == y) {
      return true;
    } else {
      return false;
    }
  }

}