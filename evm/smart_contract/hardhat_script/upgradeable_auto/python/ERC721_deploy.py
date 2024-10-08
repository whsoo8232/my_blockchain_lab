# os
import sys
import os
import subprocess

# logging
import logging
from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler

# file
from deployContract import *

#env
from dotenv import load_dotenv
load_dotenv('/home/whsoo8232/Projects/.env')

if __name__ == "__main__":
    python_pgm = os.path.basename(sys.argv[0])

    logger = polygon_set_logger(python_pgm)
    logger.setLevel(logging.DEBUG)

    network = "baseSepolia"

    infuraKey = os.getenv("INFURA_API_KEY")
    QUICKNODE_BASE_SEPOLIA_ENDPOINT_KEY = os.getenv("QUICKNODE_BASE_SEPOLIA_ENDPOINT_KEY")
    etherscanKey = ""
    MY_TESTMAIN_PK = os.getenv("MY_TESTMAIN_PK")

    ownerPK = os.getenv("MY_TESTMAIN_PK")
    tokenType = "ERC721"
    targetTokenName = "TestV3"
    targetSymbolName = "TVT"
    targetAmount = None

    retCode, retMessage, abiData, contractAddress, contractTransactionHash = polygon_deploy_contract(network, QUICKNODE_BASE_SEPOLIA_ENDPOINT_KEY, etherscanKey, ownerPK, tokenType, targetTokenName, targetSymbolName, targetAmount, logger)
    print(f"retCode=[{retCode}], retMessage=[{retMessage}]")
    print("Deploy contract transaction hash =", contractTransactionHash)

    print("------------------------------------------")
