# Essential
from web3 import Web3

# env
import os
from dotenv import load_dotenv


### Common ###
def decimals():
    return 18


def connect_web3(connect_host, apikey):
    # Mainnet #
    if connect_host == "ethereum":
        rpc_url = "https://mainnet.infura.io/v3/" + apikey
    elif connect_host == "polygon":
        rpc_url = "https://polygon-mainnet.infura.io/v3/" + apikey
    # Testnet #
    elif connect_host == "sepolia":
        rpc_url = "https://sepolia.infura.io/v3/" + apikey
    elif connect_host == "amoy":
        rpc_url = "https://polygon-amoy.infura.io/v3/" + apikey
    else:
        return None
    web3 = Web3(Web3.HTTPProvider(rpc_url))

    return web3


def get_contract(web3, contractAddress, contractAbi):
    file = open(contractAbi, "r", encoding="utf-8")
    contractAddr = web3.to_checksum_address(contractAddress)
    contract = web3.eth.contract(abi=file.read(), address=contractAddr)

    return contract


def approve_USDT_to_fundingContract(
    web3,
    USDT_contract,
    buyer,
    buyer_pk,
    fundingContract_address,
    USDT_amount,
    serviceFee,
):
    From_add = web3.to_checksum_address(buyer)
    To_add = web3.to_checksum_address(fundingContract_address)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    tokenAmount = USDT_amount + serviceFee
    tx = USDT_contract.functions.approve(To_add, tokenAmount).build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, buyer_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


def buy_ARTC_with_USDT(
    web3,
    fundingContract,
    buyer,
    buyer_pk,
    USDT_amount,
    ARTC_amount,
    serviceFee,
    id
):
    From_add = web3.to_checksum_address(buyer)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    tx = fundingContract.functions.buy_ARTC_with_USDT(
        USDT_amount, ARTC_amount, serviceFee, id
    ).build_transaction({"from": From_add, "nonce": nonce, "gasPrice": gas_price})
    signed_txn = web3.eth.account.sign_transaction(tx, buyer_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


def deposit_ARTC_to_fundingContract(
    web3,
    ARTC_contract,
    ARTC_owner,
    ARTC_owner_pk,
    fundingContract_address,
    ARTC_amount,
):
    From_add = web3.to_checksum_address(ARTC_owner)
    To_add = web3.to_checksum_address(fundingContract_address)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    tx = ARTC_contract.functions.transfer(To_add, ARTC_amount).build_transaction(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, ARTC_owner_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)
    
    return tx_receipt

def withdraw_fundingContract_ETH(
    web3,
    fundingContract,
    fundingContract_owner,
    fundingContract_owner_pk,
):
    Owner_add = web3.to_checksum_address(fundingContract_owner)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(Owner_add)
    tx = fundingContract.functions.withdraw_ETH().build_transaction(
        {"from": Owner_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, fundingContract_owner_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)

    return tx_receipt

def withdraw_fundingContract_ETH(
    web3,
    fundingContract,
    fundingContract_addr,
    fundingContract_owner,
    fundingContract_owner_pk,
):
    Owner_add = web3.to_checksum_address(fundingContract_owner)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(Owner_add)
    contractBalanace = fundingContract.functions.contract_ETH_balance().call()
    tx = fundingContract.functions.withdraw_ETH().build_transaction(
        {"from": Owner_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, fundingContract_owner_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)

    return tx_receipt

def withdraw_fundingContract_ARTC(
    web3,
    fundingContract,
    fundingContract_owner,
    fundingContract_owner_pk,
):
    Owner_add = web3.to_checksum_address(fundingContract_owner)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(Owner_add)
    tx = fundingContract.functions.withdraw_ARTC().build_transaction(
        {"from": Owner_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, fundingContract_owner_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)

    return tx_receipt


if __name__ == "__main__":
    
    load_dotenv("./hardhat-project/.env")
    INFURA_KEY = os.getenv("INFURA_API_KEY")
    COLLECTION_OWNER = os.getenv("ARTC_CROWDFUNDING_OWNER")
    COLLECTION_OWNER_PK = os.getenv("ARTC_CROWDFUNDING_OWNER_PK")
    
    # WEB3 setup
    network = "ethereum"
    web3 = connect_web3(network, INFURA_KEY)
    
    # ETH Funding Contract
    fundingContract_addr = "0xC07C86d21BD2C6a41fdb02f04EcAcCc1961a7119"
    fundingContract_abi = "./contracts_dir/ARTC_Funding/ARTC_Funding.abi"
    fundingContract = get_contract(web3, fundingContract_addr, fundingContract_abi)
    
    # ARTC Contract
    ARTC_contract_address = "0xC1f7Fe7b421aad3fab9Fb5bD4289b77aB14332A0"
    ARTC_contract_abi = "./contracts_dir/ARTC/ARTC.abi"
    ARTC_contract = get_contract(web3, ARTC_contract_address, ARTC_contract_abi)
    
    # ARTC Contract
    USDT_contract_address = "0xdAC17F958D2ee523a2206206994597C13D831ec7"
    USDT_contract_abi = "./contracts_dir/USDT/USDT.abi"
    USDT_contract = get_contract(web3, USDT_contract_address, USDT_contract_abi)
    
    # ARTC_Amount = 10000000 * 10**decimals()
    # deposit_ARTC_to_fundingContract(web3, ARTC_contract, COLLECTION_OWNER, COLLECTION_OWNER_PK, fundingContract_addr, ARTC_Amount)
    
    
    USDTAmount = 0
    ARTCAmount = 40 * 10**18
    # approve_USDT_to_fundingContract(web3, USDT_contract, COLLECTION_OWNER, COLLECTION_OWNER_PK, fundingContract_addr, USDTAmount, 0)    
    buy_ARTC_with_USDT(web3, fundingContract, COLLECTION_OWNER, COLLECTION_OWNER_PK, USDTAmount, ARTCAmount, 0, 100)
    
    # allowance = USDT_contract.functions.allowance(COLLECTION_OWNER,fundingContract_addr).call()
    # print(allowance)
    
    # bal = fundingContract.functions.contract_USDT_balance().call()
    # print(bal)