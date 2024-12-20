# Essential
from web3 import Web3

# env
import os
from dotenv import load_dotenv

# coinbase crypto change rate
from coinbase.wallet.client import Client


### Common ###
def decimals():
    return 18


def filter_receipt_dict(
    transactionType=None,
    From=None,
    To=None,
    inputETHAmount=None,
    inputTokenType=None,
    inputTokenAmount=None,
    outputTokenType=None,
    outputTokenAmount=None,
    serviceFee=None,
    gasPrice=None,
    gasUsed=None,
    transactionFee=None,
):
    receipt = {
        "transactionType": transactionType,
        "From": From,
        "To": To,
        "inputETHAmount": inputETHAmount,
        "inputTokenType": inputTokenType,
        "inputTokenAmount": inputTokenAmount,
        "outputTokenType": outputTokenType,
        "outputTokenAmount": outputTokenAmount,
        "serviceFee": serviceFee,
        "gasPrice": gasPrice,
        "gasUsed": gasUsed,
        "transactionFee": transactionFee,
    }

    return receipt


def coinbase_coin_spot_price(coin, currency):
    api_key = "organizations/1d87c8de-839b-4ef5-b73a-d6dca9bc9988/apiKeys/23fe4062-96b9-438c-b14f-e4b088fa8417"
    api_secret = "-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEINMjhjFpmI1H+BJ4Vrq51mwomQtiZuaVLOV9jrsmYA++oAoGCCqGSM49\nAwEHoUQDQgAE/erXjwh+7HVnEdL4RjHb3Au6iCORFxA3SqvJDG6EpDxFDEtqtUtr\nWxl2NmPUaFK10tuPb6gvodjDZswH5aJKBw==\n-----END EC PRIVATE KEY-----\n"
    client = Client(api_key, api_secret)
    coinPair = coin + "-" + currency
    priceData = client.get_spot_price(currency_pair=coinPair)
    return priceData  # return Dict


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


def get_fundingContract_totalETH(fundingContract):
    totalBalance = fundingContract.functions.contract_ETH_balance().call()

    return totalBalance


def get_fundingContract_totalARTC(fundingContract):
    totalBalance = fundingContract.functions.contract_ARTC_balance().call()

    return totalBalance


def get_fundingContract_totalUSDT(fundingContract):
    totalBalance = fundingContract.functions.contract_USDT_balance().call()

    return totalBalance


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
    receipt = filter_receipt_dict(
        transactionType="deposit_ARTC_to_fundingContract",
        From=ARTC_owner,
        To=fundingContract_address,
        inputTokenType="ARTC",
        inputTokenAmount=ARTC_amount,
        gasPrice=tx_receipt["effectiveGasPrice"],
        gasUsed=tx_receipt["gasUsed"],
        transactionFee=int(tx_receipt["effectiveGasPrice"])
        * int(tx_receipt["gasUsed"]),
    )
    print(receipt)

    return receipt, tx_receipt


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
    receipt = filter_receipt_dict(
        transactionType="approve_USDT_to_fundingContract",
        From=buyer,
        To=fundingContract_address,
        inputTokenType="USDT",
        inputTokenAmount=USDT_amount,
        serviceFee=serviceFee,
        gasPrice=tx_receipt["effectiveGasPrice"],
        gasUsed=tx_receipt["gasUsed"],
        transactionFee=int(tx_receipt["effectiveGasPrice"])
        * int(tx_receipt["gasUsed"]),
    )
    print(receipt)

    return receipt, tx_receipt


def estimateGas_approve_USDT_to_fundingContract(
    web3,
    USDT_contract,
    buyer,
    fundingContract_address,
    USDT_amount,
    serviceFee,
):
    From_add = web3.to_checksum_address(buyer)
    To_add = web3.to_checksum_address(fundingContract_address)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    tokenAmount = USDT_amount + serviceFee
    estimateGas = USDT_contract.functions.approve(To_add, tokenAmount).estimate_gas(
        {"from": From_add, "nonce": nonce, "gasPrice": gas_price}
    )

    return estimateGas


def estimateGas_buy_ARTC_with_ETH(
    web3,
    fundingContract,
    buyer,
    depositETH_amount,
    serviceFee,
    ARTC_amount,
):
    From_add = web3.to_checksum_address(buyer)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    estimateGas = fundingContract.functions.buy_ARTC_with_ETH(
        ARTC_amount, serviceFee
    ).estimate_gas(
        {
            "from": From_add,
            "nonce": nonce,
            "gasPrice": gas_price,
            "value": depositETH_amount + serviceFee,
        }
    )

    return estimateGas


def estimateGas_buy_ARTC_with_USDT(
    web3,
    fundingContract,
    buyer,
    USDT_amount,
    serviceFee,
    ARTC_amount,
):
    From_add = web3.to_checksum_address(buyer)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    estimateGas = fundingContract.functions.buy_ARTC_with_USDT(
        USDT_amount, ARTC_amount, serviceFee
    ).estimate_gas({"from": From_add, "nonce": nonce, "gasPrice": gas_price})

    return estimateGas


def buy_ARTC_with_ETH(
    web3,
    fundingContract,
    fundingContract_addr,
    buyer,
    buyer_pk,
    depositETH_amount,
    serviceFee,
    ARTC_amount,
):
    From_add = web3.to_checksum_address(buyer)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    tx = fundingContract.functions.buy_ARTC_with_ETH(
        ARTC_amount, serviceFee
    ).build_transaction(
        {
            "from": From_add,
            "nonce": nonce,
            "gasPrice": gas_price,
            "value": depositETH_amount + serviceFee,
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, buyer_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    receipt = filter_receipt_dict(
        transactionType="buy_ARTC_with_ETH",
        From=buyer,
        To=fundingContract_addr,
        inputTokenType="ETH",
        inputTokenAmount=depositETH_amount,
        outputTokenType="ARTC",
        outputTokenAmount=ARTC_amount,
        serviceFee=serviceFee,
        gasPrice=tx_receipt["effectiveGasPrice"],
        gasUsed=tx_receipt["gasUsed"],
        transactionFee=int(tx_receipt["effectiveGasPrice"])
        * int(tx_receipt["gasUsed"]),
    )
    print(receipt)

    return receipt, tx_receipt


def buy_ARTC_with_USDT(
    web3,
    fundingContract,
    fundingContract_addr,
    buyer,
    buyer_pk,
    USDT_amount,
    serviceFee,
    ARTC_amount,
):
    From_add = web3.to_checksum_address(buyer)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(From_add)
    tx = fundingContract.functions.buy_ARTC_with_USDT(
        USDT_amount, ARTC_amount, serviceFee
    ).build_transaction({"from": From_add, "nonce": nonce, "gasPrice": gas_price})
    signed_txn = web3.eth.account.sign_transaction(tx, buyer_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    receipt = filter_receipt_dict(
        transactionType="buy_ARTC_with_USDT",
        From=buyer,
        To=fundingContract_addr,
        inputTokenType="USDT",
        inputTokenAmount=USDT_amount,
        outputTokenType="ARTC",
        outputTokenAmount=ARTC_amount,
        serviceFee=serviceFee,
        gasPrice=tx_receipt["effectiveGasPrice"],
        gasUsed=tx_receipt["gasUsed"],
        transactionFee=int(tx_receipt["effectiveGasPrice"])
        * int(tx_receipt["gasUsed"]),
    )
    print(receipt)

    return receipt, tx_receipt


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
    fundingContract_addr,
    fundingContract_owner,
    fundingContract_owner_pk,
):
    Owner_add = web3.to_checksum_address(fundingContract_owner)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(Owner_add)
    contractBalanace = fundingContract.functions.contract_ARTC_balance().call()
    tx = fundingContract.functions.withdraw_ARTC().build_transaction(
        {"from": Owner_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, fundingContract_owner_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    receipt = filter_receipt_dict(
        transactionType="withdraw_fundingContract_ARTC",
        From=fundingContract_addr,
        To=fundingContract_owner,
        inputTokenType="ARTC",
        inputTokenAmount=contractBalanace,
        gasPrice=tx_receipt["effectiveGasPrice"],
        gasUsed=tx_receipt["gasUsed"],
        transactionFee=int(tx_receipt["effectiveGasPrice"])
        * int(tx_receipt["gasUsed"]),
    )
    print(receipt)

    return receipt, tx_receipt


def withdraw_fundingContract_USDT(
    web3,
    fundingContract,
    fundingContract_addr,
    fundingContract_owner,
    fundingContract_owner_pk,
):
    Owner_add = web3.to_checksum_address(fundingContract_owner)
    gas_price = web3.eth.gas_price
    nonce = web3.eth.get_transaction_count(Owner_add)
    contractBalanace = fundingContract.functions.contract_USDT_balance().call()
    tx = fundingContract.functions.withdraw_USDT().build_transaction(
        {"from": Owner_add, "nonce": nonce, "gasPrice": gas_price}
    )
    signed_txn = web3.eth.account.sign_transaction(tx, fundingContract_owner_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    receipt = filter_receipt_dict(
        transactionType="withdraw_fundingContract_USDT",
        From=fundingContract_addr,
        To=fundingContract_owner,
        inputTokenType="USDT",
        inputTokenAmount=contractBalanace,
        gasPrice=tx_receipt["effectiveGasPrice"],
        gasUsed=tx_receipt["gasUsed"],
        transactionFee=int(tx_receipt["effectiveGasPrice"])
        * int(tx_receipt["gasUsed"]),
    )
    print(receipt)

    return receipt, tx_receipt


if __name__ == "__main__":
    load_dotenv(".env")
    INFURA_KEY = os.getenv("INFURA_API_KEY")
    MY_TESTMAIN = os.getenv("MY_TESTMAIN")
    MY_TESTMAIN_PK = os.getenv("MY_TESTMAIN_PK")
    MY_TESTTEST = os.getenv("MY_TESTTEST")
    MY_TESTTEST_PK = os.getenv("MY_TESTTEST_PK")

    # WEB3 setup
    network = "sepolia"
    web3 = connect_web3(network, INFURA_KEY)

    # # ETH Funding Contract
    # fundingContract_addr = "0xa10f248f6525C742137e2eFb883e0cFB31f64F16"
    # fundingContract_abi = "./contracts_dir/ARTC_Funding/ARTC_Funding.abi"
    # fundingContract = get_contract(web3, fundingContract_addr, fundingContract_abi)
    # fundingContract_owner = MY_TESTMAIN  # tmp
    # fundingContract_owner_pk = MY_TESTMAIN_PK  # tmp

    # # ARTC Contract
    # ARTC_contract_address = "0x130ac05a2a5C8ba2e83021eFC0E442EA2B297f5d"
    # ARTC_contract_abi = "./contracts_dir/testGovernance/testGovernance.abi"
    # ARTC_contract = get_contract(web3, ARTC_contract_address, ARTC_contract_abi)
    # ARTC_owner = MY_TESTMAIN  # tmp
    # ARTC_owner_pk = MY_TESTMAIN_PK  # tmp

    # # USDT contract
    # USDT_contract_addr = "0x777af890456cFcF93431D37E756ec06bf190e3a7"
    # USDT_contract_abi = "./contracts_dir/payToken/payToken.abi"
    # USDT_contract = get_contract(web3, USDT_contract_addr, USDT_contract_abi)

    # # crypto change rate
    # ETH_USDT = coinbase_coin_spot_price("ETH", "USDT")


# ARTC_amount = 10000000 * 10 ** decimals()
# deposit_ARTC_to_fundingContract(
#     web3,
#     ARTC_contract,
#     ARTC_owner,
#     ARTC_owner_pk,
#     fundingContract_addr,
#     ARTC_amount,
# )

# # ## transaction part
# # # SET
# buyer = MY_TESTTEST
# buyer_pk = MY_TESTTEST_PK

# # buy ARTC with ETH
# deposit_ETH = 0.0004
# serviceFee = 0
# tokenAmount = deposit_ETH * ETH_USDT["amount"] * 10
# estimateGas = estimateGas_buy_ARTC_with_ETH(
#     web3, fundingContract, buyer, deposit_ETH, serviceFee, tokenAmount
# )
# print(estimateGas)
# buy_ARTC_with_ETH(
#     web3,
#     fundingContract,
#     fundingContract_addr,
#     buyer,
#     buyer_pk,
#     deposit_ETH,
#     serviceFee,
#     tokenAmount,
# )  # User sign with wallet

# # buy ARTC with USDT
# deposit_USDT = 10000
# serviceFee = 0
# tokenAmount = int(deposit_USDT) * 10  # USDT
# estimateGas = (
#     estimateGas_approve_USDT_to_fundingContract(
#         web3, USDT_contract, buyer, fundingContract_addr, deposit_USDT, serviceFee
#     )
#     + 66306
# )  # buy_ARTC_with_USDT average gasUsed
# print(estimateGas)
# approve_USDT_to_fundingContract(
#     web3, USDT_contract, buyer, buyer_pk, fundingContract_addr, deposit_USDT, serviceFee
# )  # User sign with wallet
# buy_ARTC_with_USDT(
#     web3,
#     fundingContract,
#     fundingContract_addr,
#     buyer,
#     buyer_pk,
#     deposit_USDT,
#     serviceFee,
#     tokenAmount,
# )  # User sign with wallet

buy_event = fundingContract.events.Buy_ARTC_With_USDT
buy_filter = buy_event.create_filter(fromBlock=6223829, lastBlock=6223829)
events = buy_filter.get_all_entries()
for event in events:
    print(event)
