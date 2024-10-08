import os
from dotenv import load_dotenv

from web3 import Web3

def connect_web3(connect_host, apikey): 
    # Mainnet #
    if connect_host == 'ethereum':
        rpc_url = "https://mainnet.infura.io/v3/" + apikey
    elif connect_host == "base_mainnet":
        rpc_url = "https://base-sepolia.g.alchemy.com/v2/" + apikey
    elif connect_host == 'polygon':
        rpc_url = "https://polygon-mainnet.infura.io/v3/" + apikey
    # Testnet #
    elif connect_host == 'sepolia':
        rpc_url = "https://sepolia.infura.io/v3/" + apikey
    elif connect_host == "base_sepolia":
        rpc_url = "https://base-sepolia.g.alchemy.com/v2/" + apikey
    elif connect_host == 'amoy':
        rpc_url = "https://polygon-amoy.infura.io/v3/" + apikey
    else:
        return None
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    
    return web3


def get_contract(web3, contractAddress, contractAbi): #test done
    file = open(contractAbi, 'r', encoding='utf-8')
    contractaddress = web3.to_checksum_address(contractAddress)
    mycontract = web3.eth.contract(abi=file.read(), address=contractaddress)
    
    return mycontract


def NFT_burn(web3, mycontract, From, From_pk, token_id):
    From_add = web3.to_checksum_address(From)
    nonce = web3.eth.get_transaction_count(From_add)
    gas_price = web3.eth.gas_price
    tx =  mycontract.functions.burn(token_id).build_transaction(
        {
            'from': From_add,
            'nonce': nonce,
            'gasPrice': gas_price
        }
    )
    signed_txn = web3.eth.account.sign_transaction(tx, From_pk)
    txHash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    tx_receipt = web3.eth.wait_for_transaction_receipt(txHash)
    print(tx_receipt)
    
    return tx_receipt


if __name__ == "__main__":
    ### common set ####
    load_dotenv('../../../../.env')

    network = "base_mainnet"
    apikey = os.getenv("ALCHEMY_API_KEY")

    OWNER = '0x5F260e9569bd824504f5AC2B050f3de46fC88888'
    OWNER_PK = '0x08c92c75b58e11a98743ce567335f68ace2113eedcd525a36c4d44481c220c02'

    web3 = connect_web3(network, apikey)
    
    NFT_contract_addr = "0x02CE058ed32E5E95BB57ae91eD71E1f9c8B4cdcF"
    NFT_contract_abi = "./envisager.abi"
    NFT_contract = get_contract(web3, NFT_contract_addr, NFT_contract_abi)
    
    ### scripts ###
    tokenId = 2
    NFT_burn(web3, NFT_contract, OWNER, OWNER_PK, tokenId)