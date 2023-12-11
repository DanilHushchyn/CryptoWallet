import asyncio
from _decimal import Decimal
from datetime import datetime
import httpx
from eth_account import Account
from fastapi import HTTPException
from propan import RabbitBroker
from web3 import AsyncWeb3, AsyncHTTPProvider, Web3
from web3.eth import AsyncEth
from config.settings import QUICKNODE_URL, MORALIS_API_KEY, RABBITMQ_URL


# from src.web3.repository import WebRepository


class WebService:
    # w3 = Web3(HTTPProvider(QUICKNODE_URL))
    moralis_api_key = MORALIS_API_KEY
    headers = {
        "X-API-Key": moralis_api_key
    }
    new_block = None
    old_block = None

    # def __init__(self, web3_repository: WebRepository) -> None:
    def __init__(self) -> None:
        # self._repository: WebRepository = web3_repository
        self.w3 = AsyncWeb3(AsyncHTTPProvider(QUICKNODE_URL), modules={'eth': (AsyncEth,)})
        self.socket_w3 = Web3(Web3.WebsocketProvider(
            'wss://blissful-side-panorama.ethereum-sepolia.quiknode.pro/3a09730228a180516dca38e9d88d5693881d84cd/'))

    async def get_trans(self, _hash):
        return await self.w3.eth.get_transaction(_hash)

    # async def find_block(self) -> None:
    #
    #     self.old_block: int = await self._repository.get_old_block()
    #
    #     if self.old_block is None:
    #         self.old_block: int = await self.get_block()
    #         await self.send_block_to_parsing(self.old_block)
    #
    #     self.new_block: int = await self.get_block()
    #
    #     if self.old_block < self.new_block:
    #         for value in range(self.old_block + 1, self.new_block + 1):
    #             await self.send_block_to_parsing(value)
    #             await asyncio.sleep(1)
    #         self.old_block: int = self.new_block
    #
    #     await self._repository.update_block(self.new_block)

    @staticmethod
    async def send_block_to_parsing(block: int):
        print('---FIND_BLOCK---')
        print(f'---{block}---')
        async with RabbitBroker(RABBITMQ_URL) as broker:
            await broker.publish(message=block, queue='parser/parse_block')

    async def get_block(self, number: str = 'latest'):
        block = await self.w3.eth.get_block(number)
        return block['number'] if number == 'latest' else block

    async def get_transactions(self, address):
        url = f'https://deep-index.moralis.io/api/v2/{address}/?chain=sepolia'
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            if response.status_code == 200:
                transactions_data = response.json()
                result = transactions_data.get('result')
                transactions_list = []
                for trans in result:
                    transactions_list.append(trans)
                return transactions_list
            else:
                # print("Ошибка при запросе к Moralis API:", response.status_code)
                raise HTTPException(status_code=401,
                                    detail=f"Ошибка при запросе к Moralis API:, {response.status_code}")

    async def get_transaction(self, _hash):
        try:
            transaction = await self.w3.eth.get_transaction(_hash)
            block = await self.get_block(transaction.get('blockNumber'))
            transaction_receipt = await self.w3.eth.get_transaction_receipt(_hash)
            return {'transaction': transaction,
                    'timestamp': datetime.fromtimestamp(block.timestamp).strftime('%Y-%m-%d %H:%M:%S'),
                    'status': transaction_receipt.get('status')}
        except ValueError:
            raise HTTPException(status_code=401, detail=f"Ошибка не правильный хэш:, {_hash}")

    # async def transaction_info(self, tx_hash):
    #     tx = await self.w3.eth.get_transaction(tx_hash)
    #     tx_receipt = await self.w3.eth.get_transaction_receipt(tx_hash)
    #
    #     if tx_receipt is None:
    #         status = "PENDING"
    #     elif tx_receipt['status'] == 1:
    #         status = "SUCCESS"
    #     else:
    #         status = "FAILURE"
    #
    #     asset = await self.get_wallet_asset(tx['from'], tx['to'])
    #
    #     tx_info = {
    #         'hash': tx.hash.hex(),
    #         'from_address': tx['from'],
    #         'to_address': tx['to'],
    #         'value': self.w3.from_wei(tx.value, asset.abbreviation),
    #         'status': status
    #     }
    #     return tx_info

    async def get_balance(self, address):
        balance_wei = await self.w3.eth.get_balance(address)
        balance_eth = self.w3.from_wei(balance_wei, 'ether')
        return {"address": address, "balance_eth": Decimal(balance_eth)}
