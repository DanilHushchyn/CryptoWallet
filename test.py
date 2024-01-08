from web3 import Web3

from config.settings import CHAINSTACK


# Set up the Etherscan provider
api_key = '6P4QJMW7S5ZQ6G8PJRAMTPR7MXPKBVUDVH'
etherscan_url = f'https://api-sepolia.etherscan.io/api?apikey={api_key}'
web3 = Web3(Web3.HTTPProvider(CHAINSTACK, request_kwargs={'timeout': 60}))
# infura_url = 'https://mainnet.infura.io/v3/6f24953f24544450a6bbeb43e8b4c353'
# web3 = Web3(Web3.HTTPProvider(infura_url))
print(web3.is_connected())
# Define the address for which you want to retrieve the balance
address = "0x3C4bda98D658750ACdb5Dc6fB49B0fb90B4971d6"

# Get the balance
block = web3.eth.get_block('latest')
print(block)
print(web3.eth.get_transaction(block['transactions'][1]))
# # Convert the balance from Wei to Ether
# formatted_balance = web3.from_wei(balance, "ether")

# Print the balance
# print("Balance:", formatted_balance)
#
# print(get_balance('0x4e46028d5cccd750a4d1BAFca99BC575448a7e77'))
