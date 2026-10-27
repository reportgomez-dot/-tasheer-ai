// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
contract GENE is ERC20, Ownable {
    constructor() ERC20("GENE Token", "GENE") Ownable(msg.sender) {}
    function mint1000T() external onlyOwner {
        _mint(msg.sender, 1000000000000000 * 10**decimals());
    }
}
