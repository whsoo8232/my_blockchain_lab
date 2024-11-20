import os, sys
from dotenv import load_dotenv

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../web3_module/.'))
sys.path.append(parent_dir)
import evm_utils


if __name__ == "__main__":
    ### common set ####
    load_dotenv('/home/whsoo8232/Projects/.env')

    network = "base_sepolia"
    apikey = os.getenv("GNC_ALCHEMY_API_KEY")
    base_web3 = evm_utils.connect_web3(network, apikey)

    artc_contract_addr = "0x943f2A691cD479bfaF661aC0281dFf2a46C4ACe9"
    artc_contract_abi = "./artc_v2/artc_v2.abi"
    artc_contract = evm_utils.get_contract(base_web3, artc_contract_addr, artc_contract_abi)
    
    artc_contract_owner = os.getenv("MY_TESTMAIN")
    artc_contract_owner_pk = os.getenv("MY_TESTMAIN_PK")
    
    ### scripts ###
    
    # artc_contract_owner_add = base_web3.to_checksum_address(artc_contract_owner)
    # nonce = base_web3.eth.get_transaction_count(artc_contract_owner_add)
    # gas_price = base_web3.eth.gas_price
    # tx = artc_contract.functions.setSymbol("ART").build_transaction(
    #     {
    #         'from': artc_contract_owner_add,
    #         'nonce': nonce,
    #         'gasPrice': gas_price
    #     }
    # )
    # sign_tx = base_web3.eth.account.sign_transaction(tx, artc_contract_owner_pk)
    # tx_hash = base_web3.eth.send_raw_transaction(sign_tx.rawTransaction)
    # tx_receipt = base_web3.eth.wait_for_transaction_receipt(tx_hash)
    # print(tx_receipt)
    
    # symbol = artc_contract.functions.symbol().call()
    # print(symbol)