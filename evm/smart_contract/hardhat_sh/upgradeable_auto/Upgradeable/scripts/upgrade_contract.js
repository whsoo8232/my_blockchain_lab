// scripts/upgrade.js
const { ethers, upgrades } = require("hardhat");

async function main() {
  const MyContractV2 = await ethers.getContractFactory("ArtcoinV2");
  console.log("Upgrading MyContract...");
  await upgrades.upgradeProxy("0x943f2A691cD479bfaF661aC0281dFf2a46C4ACe9", MyContractV2);
  console.log("MyContract upgraded to V2");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
