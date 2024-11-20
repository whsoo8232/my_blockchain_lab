const { ethers, upgrades } = require("hardhat");
const { verify } = require("../utils/verify");
const { BigNumber } = ethers;

async function main() {
  const UpgradableV1 = await ethers.getContractFactory("Artcoin");


  console.log("Deploying Artcoin...");
  const contract = await upgrades.deployProxy(UpgradableV1, [], {
    initializer: "initialize",
    kind: "transparent",
  });
  await contract.deployed();
  console.log("Artcoin deployed address to:", contract.address);
  console.log("Transaction hash:", contract.deployTransaction.hash);
}

main();
