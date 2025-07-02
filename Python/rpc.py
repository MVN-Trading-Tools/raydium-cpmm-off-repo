from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.publickey import PublicKey
from solana.rpc.commitment import Commitment
from solana.rpc.types import TxOpts
from solana.rpc.core import RPCException


def send_txn(client: Client, txn: Transaction, skip_preflight: bool = True) -> str:
    opts = TxOpts(skip_preflight=skip_preflight)
    resp = client.send_transaction(txn, *txn.signatures, opts=opts)
    return resp["result"]


def get_token_account(client: Client, addr: PublicKey):
    return client.get_account_info(addr)


def get_multiple_accounts(client: Client, pubkeys):
    return client.get_multiple_accounts(pubkeys)
