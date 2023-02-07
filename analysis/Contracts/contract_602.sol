pragma solidity ^0.4.23;

contract CoinAtc // @eachvar
{
    // ======== 初始化代币相关逻辑 ==============
    // 地址信息
    address public admin_address = 0x6dFe4B3AC236A392a6dB25A8cAc27b0fC563B0Da; // @eachvar
    address public account_address = 0x6dFe4B3AC236A392a6dB25A8cAc27b0fC563B0Da; // @eachvar 初始化后转入代币的地址
    
    // 定义账户余额
    mapping(address => uint256) balances;
    
    // solidity 会自动为 public 变量添加方法，有了下边这些变量，就能获得代币的基本信息了
    string public name = "All Things Connect"; // @eachvar
    string public symbol = "ATC"; // @eachvar
    uint8 public decimals = 18; // @eachvar
    uint256 initSupply = 210000000; // @eachvar
    uint256 public totalSupply = 0; // @eachvar

    // 生成代币，并转入到 account_address 地址
    constructor() 
    payable 
    public
    {
        totalSupply = mul(initSupply, 10**uint256(decimals));
        balances[account_address] = totalSupply;

        
    }

    function balanceOf( address _addr ) public view returns ( uint )
    {
        return balances[_addr];
    }

    // ========== 转账相关逻辑 ====================
    event Transfer(
        address indexed from, 
        address indexed to, 
        uint256 value
    ); 

    function transfer(
        address _to, 
        uint256 _value
    ) 
    public 
    returns (bool) 
    {
        require(_to != address(0));
        require(_value <= balances[msg.sender]);

        balances[msg.sender] = sub(balances[msg.sender],_value);

            

        balances[_to] = add(balances[_to], _value);
        emit Transfer(msg.sender, _to, _value);
        return true;
    }

    // ========= 授权转账相关逻辑 =============
    
    mapping (address => mapping (address => uint256)) internal allowed;
    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 value
    );

    function transferFrom(
        address _from,
        address _to,
        uint256 _value
    )
    public
    returns (bool)
    {
        require(_to != address(0));
        require(_value <= balances[_from]);
        require(_value <= allowed[_from][msg.sender]);

        balances[_from] = sub(balances[_from], _value);
        
        
        balances[_to] = add(balances[_to], _value);
        allowed[_from][msg.sender] = sub(allowed[_from][msg.sender], _value);
        emit Transfer(_from, _to, _value);
        return true;
    }

    function approve(
        address _spender, 
        uint256 _value
    ) 
    public 
    returns (bool) 
    {
        allowed[msg.sender][_spender] = _value;
        emit Approval(msg.sender, _spender, _value);
        return true;
    }

    function allowance(
        address _owner,
        address _spender
    )
    public
    view
    returns (uint256)
    {
        return allowed[_owner][_spender];
    }

    function increaseApproval(
        address _spender,
        uint256 _addedValue
    )
    public
    returns (bool)
    {
        allowed[msg.sender][_spender] = add(allowed[msg.sender][_spender], _addedValue);
        emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
        return true;
    }

    function decreaseApproval(
        address _spender,
        uint256 _subtractedValue
    )
    public
    returns (bool)
    {
        uint256 oldValue = allowed[msg.sender][_spender];

        if (_subtractedValue > oldValue) {
            allowed[msg.sender][_spender] = 0;
        } 
        else 
        {
            allowed[msg.sender][_spender] = sub(oldValue, _subtractedValue);
        }
        
        emit Approval(msg.sender, _spender, allowed[msg.sender][_spender]);
        return true;
    }

    
    // ========= 直投相关逻辑 ===============
    bool public direct_drop_switch = true; // 是否开启直投 @eachvar
    uint256 public direct_drop_rate = 10000; // 兑换比例，注意这里是eth为单位，需要换算到wei @eachvar
    address public direct_drop_address = 0x5D9789bE0Fd19299443F8bA61658C0afb1De0379; // 用于发放直投代币的账户 @eachvar
    address public direct_drop_withdraw_address = 0x6dFe4B3AC236A392a6dB25A8cAc27b0fC563B0Da; // 直投提现地址 @eachvar

    bool public direct_drop_range = false; // 是否启用直投有效期 @eachvar
    uint256 public direct_drop_range_start = 1568081880; // 有效期开始 @eachvar
    uint256 public direct_drop_range_end = 1599617880; // 有效期结束 @eachvar

    event TokenPurchase
    (
        address indexed purchaser,
        address indexed beneficiary,
        uint256 value,
        uint256 amount
    );

    // 支持为别人购买
    function buyTokens( address _beneficiary ) 
    public 
    payable // 接收支付
    returns (bool)
    {
        require(direct_drop_switch);
        require(_beneficiary != address(0));

        // 检查有效期开关
        if( direct_drop_range )
        {
            // 当前时间必须在有效期内
            // solium-disable-next-line security/no-block-members
            require(block.timestamp >= direct_drop_range_start && block.timestamp <= direct_drop_range_end);

        }
        
        // 计算根据兑换比例，应该转移的代币数量
        // uint256 tokenAmount = mul(div(msg.value, 10**18), direct_drop_rate);
        
        uint256 tokenAmount = div(mul(msg.value,direct_drop_rate ), 10**18); //此处用 18次方，这是 wei to  ether 的换算，不是代币的，所以不用 decimals,先乘后除，否则可能为零
        uint256 decimalsAmount = mul( 10**uint256(decimals), tokenAmount);
        
        // 首先检查代币发放账户余额
        require
        (
            balances[direct_drop_address] >= decimalsAmount
        );

        assert
        (
            decimalsAmount > 0
        );

        
        // 然后开始转账
        uint256 all = add(balances[direct_drop_address], balances[_beneficiary]);

        balances[direct_drop_address] = sub(balances[direct_drop_address], decimalsAmount);

            

        balances[_beneficiary] = add(balances[_beneficiary], decimalsAmount);
        
        assert
        (
            all == add(balances[direct_drop_address], balances[_beneficiary])
        );

        // 发送事件
        emit TokenPurchase
        (
            msg.sender,
            _beneficiary,
            msg.value,
            tokenAmount
        );

        return true;

    } 
    

     // ========= 空投相关逻辑 ===============
    bool public air_drop_switch = true; // 是否开启空投 @eachvar
    uint256 public air_drop_rate = 300; // 赠送的代币枚数，这个其实不是rate，直接是数量 @eachvar
    address public air_drop_address = 0x5D9789bE0Fd19299443F8bA61658C0afb1De0379; // 用于发放空投代币的账户 @eachvar
    uint256 public air_drop_count = 1; // 每个账户可以参加的次数 @eachvar

    mapping(address => uint256) airdrop_times; // 用于记录参加次数的mapping

    bool public air_drop_range = false; // 是否启用空投有效期 @eachvar
    uint256 public air_drop_range_start = 1568081880; // 有效期开始 @eachvar
    uint256 public air_drop_range_end = 1599617880; // 有效期结束 @eachvar

    event TokenGiven
    (
        address indexed sender,
        address indexed beneficiary,
        uint256 value,
        uint256 amount
    );

    // 也可以帮别人领取
    function airDrop( address _beneficiary ) 
    public 
    payable // 接收支付
    returns (bool)
    {
        require(air_drop_switch);
        require(_beneficiary != address(0));
        // 检查有效期开关
        if( air_drop_range )
        {
            // 当前时间必须在有效期内
            // solium-disable-next-line security/no-block-members
            require(block.timestamp >= air_drop_range_start && block.timestamp <= air_drop_range_end);

        }

        // 检查受益账户参与空投的次数
        if( air_drop_count > 0 )
        {
            require
            ( 
                airdrop_times[_beneficiary] <= air_drop_count 
            );
        }
        
        // 计算根据兑换比例，应该转移的代币数量
        uint256 tokenAmount = air_drop_rate;
        uint256 decimalsAmount = mul(10**uint256(decimals), tokenAmount);// 转移代币时还要乘以小数位
        
        // 首先检查代币发放账户余额
        require
        (
            balances[air_drop_address] >= decimalsAmount
        );

        assert
        (
            decimalsAmount > 0
        );

        
        
        // 然后开始转账
        uint256 all = add(balances[air_drop_address], balances[_beneficiary]);

        balances[air_drop_address] = sub(balances[air_drop_address], decimalsAmount);

        
        balances[_beneficiary] = add(balances[_beneficiary], decimalsAmount);
        
        assert
        (
            all == add(balances[air_drop_address], balances[_beneficiary])
        );

        // 发送事件
        emit TokenGiven
        (
            msg.sender,
            _beneficiary,
            msg.value,
            tokenAmount
        );

        return true;

    }
    
    // ========== 代码销毁相关逻辑 ================
    event Burn(address indexed burner, uint256 value);

    function burn(uint256 _value) public 
    {
        _burn(msg.sender, _value);
    }

    function _burn(address _who, uint256 _value) internal 
    {
        require(_value <= balances[_who]);
        
        balances[_who] = sub(balances[_who], _value);

            

        totalSupply = sub(totalSupply, _value);
        emit Burn(_who, _value);
        emit Transfer(_who, address(0), _value);
    }
    
    
    // ============== admin 相关函数 ==================
    modifier admin_only()
    {
        require(msg.sender==admin_address);
        _;
    }

    function setAdmin( address new_admin_address ) 
    public 
    admin_only 
    returns (bool)
    {
        require(new_admin_address != address(0));
        admin_address = new_admin_address;
        return true;
    }

    // 空投管理
    function setAirDrop( bool status )
    public
    admin_only
    returns (bool)
    {
        air_drop_switch = status;
        return true;
    }
    
    // 直投管理
    function setDirectDrop( bool status )
    public
    admin_only
    returns (bool)
    {
        direct_drop_switch = status;
        return true;
    }
    
    // ETH提现
    function withDraw()
    public
    {
        // 管理员和之前设定的提现账号可以发起提现，但钱一定是进提现账号
        require(msg.sender == admin_address || msg.sender == direct_drop_withdraw_address);
        require(address(this).balance > 0);
        // 全部转到直投提现中
        direct_drop_withdraw_address.transfer(address(this).balance);
    }
        // ======================================
    /// 默认函数
    function () external payable
    {
                        if( msg.value > 0 )
            buyTokens(msg.sender);
        else
            airDrop(msg.sender); 
        
        
        
           
    }

    // ========== 公用函数 ===============
    // 主要就是 safemath
    function mul(uint256 a, uint256 b) internal pure returns (uint256 c) 
    {
        if (a == 0) 
        {
            return 0;
        }

        c = a * b;
        assert(c / a == b);
        return c;
    }

    function div(uint256 a, uint256 b) internal pure returns (uint256) 
    {
        return a / b;
    }

    function sub(uint256 a, uint256 b) internal pure returns (uint256) 
    {
        assert(b <= a);
        return a - b;
    }

    function add(uint256 a, uint256 b) internal pure returns (uint256 c) 
    {
        c = a + b;
        assert(c >= a);
        return c;
    }

}