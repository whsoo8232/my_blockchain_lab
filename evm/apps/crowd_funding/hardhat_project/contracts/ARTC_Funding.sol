// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

// USDT Interface
interface non_standard_IERC20 {
    function transfer(address _to, uint256 _amount) external;
    function transferFrom(address _from, address _to, uint256 _amount) external;
    function balanceOf(address _address) external view returns (uint256);
}

contract ARTC_Funding is ReentrancyGuard, Ownable {
    non_standard_IERC20 public USDT;
    IERC20 public ARTC;
    address public ARTC_owner;

    // USDT contract distribute
    address public _USDT = 0x2Dc78Fec7772f84E781a4911196547cFbe119541;

    // token contract distribute
    address public _ARTC = 0xC1f7Fe7b421aad3fab9Fb5bD4289b77aB14332A0;
    address public _ARTC_owner = 0x701c91878201d7C1901b20e6d8E9518A12DD2682;

    uint public decimals = 18;

    event Funding(string tx_type, uint id, address wallet, uint input_amount, uint output_amount, uint fee);
    event Withdraw_ETH(address user, uint amount);
    event Withdraw_ARTC(address user, uint amount);
    event Withdraw_USDT(address user, uint amount);

    constructor() Ownable(msg.sender) {
        USDT = non_standard_IERC20(_USDT);
        ARTC = IERC20(_ARTC);
        ARTC_owner = _ARTC_owner;
    }

    function contract_ARTC_balance() external view returns (uint256) {
        return ARTC.balanceOf(address(this));
    }

    function contract_ETH_balance() external view returns (uint256) {
        return address(this).balance;
    }

    function contract_USDT_balance() external view returns (uint256) {
        return USDT.balanceOf(address(this));
    }

    function buy_ARTC_with_ETH(uint256 buyARTC_amount, uint256 ETH_fee, uint256 _id) external payable {
        require(msg.value - ETH_fee > 0, "You must send some Ether to buy tokens");
        require(ARTC.transfer(msg.sender, buyARTC_amount), "ARTC transfer failed");
        emit Funding('ETH', _id, msg.sender, msg.value, buyARTC_amount, ETH_fee);
    }

    function buy_ARTC_with_USDT(uint256 USDT_amount, uint256 buyARTC_amount, uint256 USDT_fee, uint256 _id) external payable {
        require(USDT_amount - USDT_fee > 0, "You must send some Ether to buy tokens");
        uint256 senderBalance = USDT.balanceOf(msg.sender);
        USDT.transferFrom(msg.sender, address(this), USDT_amount + USDT_fee);
        bool _result;
        if(senderBalance-USDT.balanceOf(msg.sender) == USDT_amount){
            _result = true;
        }
        else{
            _result = false;
        }
        require(_result, "USDT transfer failed");
        require(ARTC.transfer(msg.sender, buyARTC_amount), "ARTC transfer failed");
        emit Funding('USDT', _id, msg.sender, USDT_amount, buyARTC_amount, USDT_fee);
    }

    function withdraw_ETH() external onlyOwner {
        uint256 contractBalance = address(this).balance;
        payable(msg.sender).transfer(address(this).balance);
        emit Withdraw_ETH(msg.sender, contractBalance);
    }

    function withdraw_ARTC() external onlyOwner {
        uint256 contractBalance = ARTC.balanceOf(address(this));
        require(ARTC.transfer(msg.sender, ARTC.balanceOf(address(this))), "balance transfer failed");
        emit Withdraw_ARTC(msg.sender, contractBalance);
    }

    function withdraw_USDT() external onlyOwner {
        uint256 contractBalance = USDT.balanceOf(address(this));
        USDT.transfer(msg.sender, USDT.balanceOf(address(this)));
        require(USDT.balanceOf(address(this)) == 0, "balance transfer failed");
        emit Withdraw_USDT(msg.sender, contractBalance);
    }
}