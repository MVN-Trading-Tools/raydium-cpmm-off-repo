from solana.publickey import PublicKey
from solana.rpc.types import TxOpts
from .constants import (
    AMM_CONFIG_SEED,
    AUTH_SEED,
    POOL_SEED,
    POOL_VAULT_SEED,
    POOL_LP_MINT_SEED,
    OBSERVATION_SEED,
)


def u16_to_bytes(value: int) -> bytes:
    return value.to_bytes(2, "big")


def get_amm_config_address(index: int, program_id: PublicKey) -> (PublicKey, int):
    return PublicKey.find_program_address([AMM_CONFIG_SEED, u16_to_bytes(index)], program_id)


def get_auth_address(program_id: PublicKey) -> (PublicKey, int):
    return PublicKey.find_program_address([AUTH_SEED], program_id)


def get_pool_address(amm_config: PublicKey, token_mint0: PublicKey, token_mint1: PublicKey, program_id: PublicKey) -> (PublicKey, int):
    return PublicKey.find_program_address(
        [POOL_SEED, bytes(amm_config), bytes(token_mint0), bytes(token_mint1)], program_id
    )


def get_pool_vault_address(pool: PublicKey, vault_token_mint: PublicKey, program_id: PublicKey) -> (PublicKey, int):
    return PublicKey.find_program_address(
        [POOL_VAULT_SEED, bytes(pool), bytes(vault_token_mint)], program_id
    )


def get_pool_lp_mint_address(pool: PublicKey, program_id: PublicKey) -> (PublicKey, int):
    return PublicKey.find_program_address([POOL_LP_MINT_SEED, bytes(pool)], program_id)


def get_oracle_account_address(pool: PublicKey, program_id: PublicKey) -> (PublicKey, int):
    return PublicKey.find_program_address([OBSERVATION_SEED, bytes(pool)], program_id)
