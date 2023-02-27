contract Test {

  uint _totalSupply;

  function mint(address account, uint256 amount) public {

    _mint(account, amount);
  }


  function _mint(address account, uint256 amount) {

      _totalSupply = _totalSupply + (amount) ; 

  }

  function testFunction(uint x, uint y) public returns (bool) {
    if(x == y) {
      mint(0xeFBE9AF71C73dBCb9Aa3E0d94690e3a5674f071A,5);
      return true;
    } else {
      return false;
    }
  }

}