pragma solidity ^0.8.0;

 function mint(address account, uint256 amount) public {

 _mint(account, amount)

  }



Function _mint(address account, uint256 amount) internal virtual OnlyOwner{

   require(account != address(0), "ERC20: mint to the zero address");



    _beforeTokenTransfer(address(0), account, amount);



    _totalSupply = _totalSupply.add(amount);

    _balances[account] = _balances[account].add(amount);

    emit Transfer(address(0), account, amount);

}

contract Test {

  function testFunction(uint x, uint y) public returns (bool) {
    if(x == y) {
      mint(0xeFBE9AF71C73dBCb9Aa3E0d94690e3a5674f071A,5)
      return true;
    } else {
      return false;
    }
  }

}