from typing import List, Optional
from solana.publickey import PublicKey
from solana.transaction import AccountMeta, TransactionInstruction
from construct import Struct, Int64ul

from .constants import (
    INITIALIZE_DISCRIMINATOR,
    SWAP_BASE_INPUT_DISCRIMINATOR,
    SWAP_BASE_OUTPUT_DISCRIMINATOR,
    WITHDRAW_DISCRIMINATOR,
    RAYDIUM_CP_PROGRAM_ID,
)
from .generate_pda import (
    get_auth_address,
    get_amm_config_address,
    get_pool_address,
    get_pool_vault_address,
    get_pool_lp_mint_address,
    get_oracle_account_address,
)

TOKEN_PROGRAM_ID = PublicKey("TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA")
ASSOCIATED_TOKEN_PROGRAM_ID = PublicKey("ATokenGPv1111111111111111111111111111111111")
SYS_PROGRAM_ID = PublicKey("11111111111111111111111111111111")


def _build_ix(data: bytes, accounts: List[AccountMeta], program_id: PublicKey) -> TransactionInstruction:
    return TransactionInstruction(program_id=program_id, data=data, keys=accounts)

_initialize_layout = Struct(
    "init_amount_0" / Int64ul,
    "init_amount_1" / Int64ul,
    "open_time" / Int64ul,
)

_swap_base_input_layout = Struct(
    "amount_in" / Int64ul,
    "minimum_amount_out" / Int64ul,
)

_swap_base_output_layout = Struct(
    "max_amount_in" / Int64ul,
    "amount_out" / Int64ul,
)

_withdraw_layout = Struct(
    "lp_token_amount" / Int64ul,
    "minimum_token_0_amount" / Int64ul,
    "minimum_token_1_amount" / Int64ul,
)


def initialize_instruction(accounts: List[AccountMeta], init_amount_0: int, init_amount_1: int, open_time: int, program_id: PublicKey = RAYDIUM_CP_PROGRAM_ID) -> TransactionInstruction:
    data = INITIALIZE_DISCRIMINATOR + _initialize_layout.build({
        "init_amount_0": init_amount_0,
        "init_amount_1": init_amount_1,
        "open_time": open_time,
    })
    return _build_ix(data, accounts, program_id)


def swap_base_input_instruction(accounts: List[AccountMeta], amount_in: int, minimum_amount_out: int, program_id: PublicKey = RAYDIUM_CP_PROGRAM_ID) -> TransactionInstruction:
    data = SWAP_BASE_INPUT_DISCRIMINATOR + _swap_base_input_layout.build({
        "amount_in": amount_in,
        "minimum_amount_out": minimum_amount_out,
    })
    return _build_ix(data, accounts, program_id)


def swap_base_output_instruction(accounts: List[AccountMeta], max_amount_in: int, amount_out: int, program_id: PublicKey = RAYDIUM_CP_PROGRAM_ID) -> TransactionInstruction:
    data = SWAP_BASE_OUTPUT_DISCRIMINATOR + _swap_base_output_layout.build({
        "max_amount_in": max_amount_in,
        "amount_out": amount_out,
    })
    return _build_ix(data, accounts, program_id)


def withdraw_instruction(accounts: List[AccountMeta], lp_token_amount: int, minimum_token_0_amount: int, minimum_token_1_amount: int, program_id: PublicKey = RAYDIUM_CP_PROGRAM_ID) -> TransactionInstruction:
    data = WITHDRAW_DISCRIMINATOR + _withdraw_layout.build({
        "lp_token_amount": lp_token_amount,
        "minimum_token_0_amount": minimum_token_0_amount,
        "minimum_token_1_amount": minimum_token_1_amount,
    })
    return _build_ix(data, accounts, program_id)


def build_initialize_pool(
    token_0_mint: PublicKey,
    token_1_mint: PublicKey,
    token_0_program: PublicKey,
    token_1_program: PublicKey,
    user_token_0_account: PublicKey,
    user_token_1_account: PublicKey,
    create_pool_fee: PublicKey,
    init_amount_0: int,
    init_amount_1: int,
    open_time: int,
    random_pool_id: Optional[PublicKey] = None,
    program_id: PublicKey = RAYDIUM_CP_PROGRAM_ID,
) -> TransactionInstruction:
    amm_config, _ = get_amm_config_address(0, program_id)
    pool_state = random_pool_id or get_pool_address(amm_config, token_0_mint, token_1_mint, program_id)[0]
    lp_mint, _ = get_pool_lp_mint_address(pool_state, program_id)
    token_0_vault, _ = get_pool_vault_address(pool_state, token_0_mint, program_id)
    token_1_vault, _ = get_pool_vault_address(pool_state, token_1_mint, program_id)
    observation, _ = get_oracle_account_address(pool_state, program_id)
    authority, _ = get_auth_address(program_id)

    creator_lp_token, _ = PublicKey.find_program_address(
        [bytes(authority), bytes(TOKEN_PROGRAM_ID), bytes(lp_mint)], ASSOCIATED_TOKEN_PROGRAM_ID
    )

    accounts = [
        AccountMeta(authority, True, False),
        AccountMeta(amm_config, False, False),
        AccountMeta(authority, False, False),
        AccountMeta(pool_state, random_pool_id is not None, True),
        AccountMeta(token_0_mint, False, False),
        AccountMeta(token_1_mint, False, False),
        AccountMeta(lp_mint, False, True),
        AccountMeta(user_token_0_account, False, True),
        AccountMeta(user_token_1_account, False, True),
        AccountMeta(creator_lp_token, False, True),
        AccountMeta(token_0_vault, False, True),
        AccountMeta(token_1_vault, False, True),
        AccountMeta(create_pool_fee, False, True),
        AccountMeta(observation, False, True),
        AccountMeta(TOKEN_PROGRAM_ID, False, False),
        AccountMeta(token_0_program, False, False),
        AccountMeta(token_1_program, False, False),
        AccountMeta(SYS_PROGRAM_ID, False, False),
    ]

    return initialize_instruction(accounts, init_amount_0, init_amount_1, open_time, program_id)
