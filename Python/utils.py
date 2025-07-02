from math import ceil, floor
from solana.rpc.api import Client
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient
from construct import Container
from typing import Tuple
from .layout import PoolStateLayout, AmmConfigLayout
from .dto import PoolState, AmmConfig


def deserialize_anchor_account(layout, data: bytes) -> Container:
    return layout.parse(data)


def amount_with_slippage(amount: int, slippage: float, round_up: bool) -> int:
    if round_up:
        return ceil(amount * (1 + slippage))
    return floor(amount * (1 - slippage))


async def monitor_liquidity(rpc_ws_url: str, vault_accounts: Tuple[PublicKey, PublicKey], callback):
    """Subscribe to vault account changes and invoke callback(balance0, balance1)."""
    from solana.rpc.websocket_api import connect

    async with connect(rpc_ws_url) as ws:
        sub0 = await ws.account_subscribe(str(vault_accounts[0]))
        sub1 = await ws.account_subscribe(str(vault_accounts[1]))
        while True:
            msg = await ws.recv()
            if msg.result and msg.result.get('value'):
                # simplistic: fetch both accounts each time
                client = Client(ws.endpoint_uri.replace('ws', 'http'))
                acc0 = client.get_account_info(vault_accounts[0])['result']['value']
                acc1 = client.get_account_info(vault_accounts[1])['result']['value']
                if acc0 and acc1:
                    balance0 = int.from_bytes(acc0['data'][0], 'little')
                    balance1 = int.from_bytes(acc1['data'][0], 'little')
                    callback(balance0, balance1)

from solana.client.rpc_client import RpcClient


def get_pool_mints_inverse_fee(client: RpcClient, token_mint0: PublicKey, token_mint1: PublicKey, post_fee_amount0: int, post_fee_amount1: int):
    # Placeholder: implement token-2022 transfer fee logic if needed
    return (
        {"mint": token_mint0, "transfer_fee": 0},
        {"mint": token_mint1, "transfer_fee": 0},
    )


def get_pool_mints_transfer_fee(client: RpcClient, token_mint0: PublicKey, token_mint1: PublicKey, pre_fee_amount0: int, pre_fee_amount1: int):
    # Placeholder for transfer fee calculation
    return (
        {"mint": token_mint0, "transfer_fee": 0},
        {"mint": token_mint1, "transfer_fee": 0},
    )
