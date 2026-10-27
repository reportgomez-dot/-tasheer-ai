// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract GeneBalance {
    string public name = "GENE Balance";
    string public symbol = "GENE";
    uint8 public decimals = 18;
    uint256 public totalSupply;
    
    mapping(address => uint256) public balanceOf;
    mapping(address => string) public myGene;
    
    event NewBalance(address indexed user, string gene, uint256 amount);

    // هذه هي الدالة اللي تصنع الرصيد من الجين
    function createBalanceFromGene(string memory _geneCode) public {
        require(bytes(_geneCode).length > 10, "كود الجين قصير جدا");
        require(bytes(myGene[msg.sender]).length == 0, "عندك رصيد من قبل");

        uint256 geneLength = bytes(_geneCode).length;
        
        // المعادلة: كل حرف = 1000 وحدة
        // جين 500 حرف = 500,000 GENE
        uint256 amount = geneLength * 1000 * 10**decimals;
        
        myGene[msg.sender] = _geneCode;
        balanceOf[msg.sender] += amount;
        totalSupply += amount;

        emit NewBalance(msg.sender, _geneCode, amount);
    }

    // تحويل الرصيد
    function transfer(address to, uint256 amount) public returns (bool) {
        require(balanceOf[msg.sender] >= amount, "رصيدك ما يكفي");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        return true;
    }
}
