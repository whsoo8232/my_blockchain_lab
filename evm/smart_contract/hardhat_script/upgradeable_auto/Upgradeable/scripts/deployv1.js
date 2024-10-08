const { ethers, upgrades } = require("hardhat");
const { verify } = require("../utils/verify");
const { BigNumber } = ethers;

async function main() {
  const UpgradableV1 = await ethers.getContractFactory("TestV3");

  console.log("Deploying TestV3...");
  const contract = await upgrades.deployProxy(UpgradableV1, [], {
    initializer: "initialize",
    kind: "transparent",
  });

  await contract.deployed();
  console.log("TestV3 deployed address to:", contract.address);
  console.log("Transaction hash:", contract.deployTransaction.hash);
}

main();
