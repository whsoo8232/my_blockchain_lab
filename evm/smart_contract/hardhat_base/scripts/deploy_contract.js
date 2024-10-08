const { ethers } = require("hardhat");

async function main() {
    const deployContract = await ethers.getContractFactory("contractName");

    console.log("Deploying TestV3...");
    const contract = await deployContract.deploy();

    console.log(deployContract, "deployed address to:", contract.address);
    console.log("Transaction hash:", contract.deployTransaction.hash);
}

main();
