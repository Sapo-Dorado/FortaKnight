/**
 *Submitted for verification at Etherscan.io on 2019-10-10
*/

/**
 *Submitted for verification at Etherscan.io on 2019-08-29
*/

pragma solidity ^0.5.11;

contract ERC20 {
  function balanceOf(address who) public view returns (uint256);
  function allowance(address owner, address spender) public view returns (uint256);
  function transferFrom(address from, address to, uint256 value) public returns (bool);
  function approve(address spender, uint256 value) public returns (bool);
  function transfer(address to, uint value) public returns(bool);
  event Transfer(address indexed from, address indexed to, uint value);
  event Approval(address indexed owner, address indexed spender, uint256 value);
  
}

library SafeMath{
      function mul(uint256 a, uint256 b) internal pure returns (uint256) 
    {
        if (a == 0) {
        return 0;}
        uint256 c = a * b;
        assert(c / a == b);
        return c;
    }

    function div(uint256 a, uint256 b) internal pure returns (uint256) 
    {
        uint256 c = a / b;
        return c;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) 
    {
        assert(b <= a);
        return a - b;
    }

    function add(uint256 a, uint256 b) internal pure returns (uint256) 
    {
        uint256 c = a + b;
        assert(c >= a);
        return c;
    }

}
contract GRIC_COIN is ERC20 {
    
        using SafeMath for uint256;

    string internal _name;
    string internal _symbol;
    uint8 internal _decimals;
    uint256 internal _totalSupply;
    
    address internal  _admin;
    uint256 public exchangeRate; //percentage
    address public tokenaddress;

    mapping (address => uint256) internal balances;
    mapping (address => mapping (address => uint256)) internal allowed;
    event oldtokenhistory(address tokenaddress,address _from, address _to,uint256 _amount);
   

    constructor(uint256 _rate,address _tokenaddress) public {
        _admin = msg.sender;
        _symbol = "GC";  
        _name = "Gric Coin"; 
        _decimals = 18; 
        _totalSupply = 20000000* 10**uint(_decimals);
        balances[msg.sender]=_totalSupply;
        exchangeRate = _rate;
        tokenaddress = _tokenaddress;
    }
    
    modifier ownership()  {
    require(msg.sender == _admin);
        _;
    }
    
  
    function name() public view returns (string memory) 
    {
        return _name;
    }

    function symbol() public view returns (string memory) 
    {
        return _symbol;
    }

    function decimals() public view returns (uint8) 
    {
        return _decimals;
    }

    function totalSupply() public view returns (uint256) 
    {
        return _totalSupply;
    }

   function transfer(address _to, uint256 _value) public returns (bool) {
     require(_to != address(0));
     require(_value <= balances[msg.sender]);
     balances[msg.sender] = balances[msg.sender].sub(_value);
     balances[_to] = (balances[_to]).add( _value);
     emit ERC20.Transfer(msg.sender, _to, _value);
     return true;
   }

  function balanceOf(address _owner) public view returns (uint256 balance) {
    return balances[_owner];
   }

  function transferFrom(address _from, address _to, uint256 _value) public returns (bool) {
     require(_to != address(0));
     require(_value <= balances[_from]);
     require(_value <= allowed[_from][msg.sender]);

    balances[_from] = (balances[_from]).sub( _value);
    balances[_to] = (balances[_to]).add(_value);
    allowed[_from][msg.sender] = (allowed[_from][msg.sender]).sub(_value);
    emit ERC20.Transfer(_from, _to, _value);
     return true;
   }

   function approve(address _spender, uint256 _value) public returns (bool) {
     allowed[msg.sender][_spender] = _value;
    emit ERC20.Approval(msg.sender, _spender, _value);
     return true;
   }

  function allowance(address _owner, address _spender) public view returns (uint256) {
     return allowed[_owner][_spender];
   }

  function mint(uint256 _amount) public ownership returns (bool) {
    _totalSupply = (_totalSupply).add(_amount);
    balances[_admin] +=_amount;
    return true;
  }
    
  function exchange(uint256 _amount) public{   //amountA = value //_rate= ratio value
     uint256 total = (_amount.div(1000)).mul(exchangeRate) ;
     require(balances[_admin]>=total);
     ERC20(tokenaddress).transferFrom(msg.sender,address(this), _amount); //after allowance
     balances[_admin]= (balances[_admin]).sub(total);
     balances[msg.sender] = (balances[msg.sender]).add(total);
     emit ERC20.Transfer(_admin,msg.sender,total);
     emit oldtokenhistory(tokenaddress,msg.sender,address(this),_amount);
  }

  // owner can update the ratio rate of old token
  function updateRate(uint256 _rate) public returns(bool) {
        require(msg.sender==_admin);
        exchangeRate = _rate;
        return true;
    }

  //owner can update the old token address    
  function updatetokenaddress(address _tokenaddress) public returns(bool) {
      require(msg.sender==_admin);
      tokenaddress = _tokenaddress;
      return true;
  }    
  
  //only admin can initiate this function
  //he can transfer the old token to him or any body else
  function withdrawoldtoken(uint256 amount, address to) public returns (bool){      
      require(msg.sender==_admin && uint256(ERC20(tokenaddress).balanceOf(address(this)))>=amount);
      ERC20(tokenaddress).transferFrom(address(this),to,amount);
      emit oldtokenhistory(tokenaddress,address(this),to,amount);
      return true;
  }
  
  //Admin can transfer his ownership to new address
  function transferownership(address _newaddress) public returns(bool){
      require(msg.sender==_admin);
      _admin=_newaddress;
      return true;
  }
    
}