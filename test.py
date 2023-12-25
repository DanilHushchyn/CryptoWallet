from decimal import Decimal

from web3 import HTTPProvider, Web3
from web3.eth import AsyncEth

from config.settings import MORALIS_API_KEY, QUICKNODE_URL

moralis_api_key = MORALIS_API_KEY
headers = {
    "X-API-Key": moralis_api_key
}


w3 = Web3(HTTPProvider(QUICKNODE_URL))


def get_balance( address):
    balance_wei = w3.eth.get_balance(address)
    balance_eth = w3.from_wei(balance_wei, 'ether')
    return {"address": address, "balance_eth": Decimal(balance_eth)}


print(get_balance('0x4e46028d5cccd750a4d1BAFca99BC575448a7e77'))