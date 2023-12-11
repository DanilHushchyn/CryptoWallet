import json
import pprint
import secrets

# from web3 import Web3, exceptions
#
# #
# # binance_testnet_rpc_url = "https://data-seed-prebsc-1-s1.binance.org:8545/"
# # web3 = Web3(Web3.HTTPProvider(binance_testnet_rpc_url))
# # print(f"Is connected: {web3.is_connected()}")  # Is connected: True
# # # С подключением вас 🥳
# #
# #
# # #
# wallet_address = "0x3C4bda98D658750ACdb5Dc6fB49B0fb90B4971d6"  # ваш адрес
# # checksum_address = Web3.to_checksum_address(wallet_address)
# # balance = web3.eth.get_balance(checksum_address)
# # print(f"balance of {wallet_address}={balance} Wei")
#
# import base64
# import os
#
# import web3
#
#
# class WalletManager:
#     def __init__(self):
#         """ """
#         self.w3 = self.__create_web3_instance()
#         # self.account = os.environ['SEPOLIA_ACCOUNT']
#         self.account = '0x3C4bda98D658750ACdb5Dc6fB49B0fb90B4971d6'
#         # self.account_private_key = os.environ['METAMASK_PRIVATE_KEY']
#         self.account_private_key = "b2ad77f8a69063e844d4753e4cd098ff1a734522dcd2f0c0d2998fadfef84448"
#         self.max_fee_per_gas = self.w3.to_wei('250', 'gwei')
#         self.max_priority_fee_per_gas = self.w3.eth.max_priority_fee
#         self.chain_id = self.w3.eth.chain_id
#
#     @staticmethod
#     def __create_web3_instance():
#         """ """
#         infura_api_key = 'ee2ccd61faef4e848221fcd619462154'
#         infura_api_key_secret = '9W0sBXLgv3vdFX8W9fqYaoDz499BKGNnzBNr04YAas4+J73Q/M+3Rg'
#         data = f'{infura_api_key}:{infura_api_key_secret}'.encode('ascii')
#         basic_auth_token = base64.b64encode(data).strip().decode('utf-8')
#
#         infura_sepolia_endpoint = f'https://sepolia.infura.io/v3/{infura_api_key}'
#
#         headers = dict(Authorization=f'Basic {basic_auth_token}')
#         return web3.Web3(web3.HTTPProvider(infura_sepolia_endpoint, request_kwargs=dict(headers=headers)))
#
#     def get_balance(self, unit='wei'):
#         balance = self.w3.eth.get_balance(self.account)
#         if unit != 'wei':
#             return self.w3.from_wei(balance, unit)
#
#     def send_eth(self, target_account, amount, unit='wei'):
#         if unit != 'wei':
#             amount = self.w3.to_wei(amount, unit)
#
#         nonce = self.w3.eth.get_transaction_count(self.account)
#         print(nonce)
#         tx = {'nonce': nonce,
#               'maxFeePerGas': self.max_fee_per_gas,
#               'maxPriorityFeePerGas': self.max_priority_fee_per_gas,
#               'from': self.account,
#               'to': target_account,
#               'value': amount,
#               'data': b'',
#               'type': 2,
#               'chainId': self.chain_id}
#         tx['gas'] = self.w3.eth.estimate_gas(tx)
#         #
#         signed_tx = self.w3.eth.account.sign_transaction(tx, self.account_private_key)
#         tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
#         #
#         result = self.w3.eth.wait_for_transaction_receipt(tx_hash)
#         if result['status'] != 1:
#             raise RuntimeError(f'transaction failed: {tx_hash}')



#
# def main():
#     """ """
#     # wm = WalletManager()
#     #
#     # sepolia_faucet_account = wm.w3.to_checksum_address('0xff388805613263352FdB00F2ec255Fef8716CeCF')
#     #
#     # balance = str(wm.get_balance('ether'))
#     # print(f'balance before transaction: {balance}')
#     # #
#     # # print(f'send 20,000 gwei to {sepolia_faucet_account} (Sepolia faucet account)')
#     # wm.send_eth("0xff388805613263352FdB00F2ec255Fef8716CeCF", 20000, 'gwei')
#     #
#     # balance = str(wm.get_balance('ether'))
#     # print(f'balance after transaction: {balance}')
#
#     infura_url = 'https://blissful-side-panorama.ethereum-sepolia.quiknode.pro/mktp-1d2354ad7e1425476ccf78833521650ca5ed56ea'
#     private_key = "b2ad77f8a69063e844d4753e4cd098ff1a734522dcd2f0c0d2998fadfef84448"
#     from_account = '0x3C4bda98D658750ACdb5Dc6fB49B0fb90B4971d6'
#     to_account = '0xff388805613263352FdB00F2ec255Fef8716CeCF'
#     web3 = Web3(Web3.HTTPProvider(infura_url))
#
#     try:
#         from_account = web3.to_checksum_address(from_account)
#     except exceptions.InvalidAddress:
#         print(f"Invalid 'from_account' address: {from_account}")
#
#     try:
#         to_account = web3.to_checksum_address(to_account)
#     except exceptions.InvalidAddress:
#         print(f"Invalid 'to_account' address: {to_account}")
#
#     nonce = web3.eth.get_transaction_count(from_account)
#     tx = {
#         'type': '0x2',
#         'nonce': nonce,
#         'from': from_account,
#         'to': to_account,
#         'value': web3.to_wei(0.001, 'ether'),
#         'maxFeePerGas': web3.to_wei('250', 'gwei'),
#         'maxPriorityFeePerGas': web3.to_wei('3', 'gwei'),
#         'chainId': web3.eth.chain_id
#     }
#     gas = web3.eth.estimate_gas(tx)
#     tx['gas'] = gas
#     signed_tx = web3.eth.account.sign_transaction(tx, private_key)
#     tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
#     print(tx_hash)
#
# if __name__ == '__main__':
#     main()

print(secrets.token_hex(32))