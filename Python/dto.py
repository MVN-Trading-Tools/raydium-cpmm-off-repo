from dataclasses import dataclass
from typing import List
from solana.publickey import PublicKey

@dataclass
class AmmConfig:
    bump: int
    disable_create_pool: int
    index: int
    trade_fee_rate: int
    protocol_fee_rate: int
    fund_fee_rate: int
    create_pool_fee: int
    protocol_owner: PublicKey
    fund_owner: PublicKey

@dataclass
class PoolState:
    amm_config: PublicKey
    pool_creator: PublicKey
    token_0_vault: PublicKey
    token_1_vault: PublicKey
    lp_mint: PublicKey
    token_0_mint: PublicKey
    token_1_mint: PublicKey
    token_0_program: PublicKey
    token_1_program: PublicKey
    observation_key: PublicKey
    auth_bump: int
    status: int
    lp_mint_decimals: int
    mint_0_decimals: int
    mint_1_decimals: int
    lp_supply: int
    protocol_fees_token_0: int
    protocol_fees_token_1: int
    fund_fees_token_0: int
    fund_fees_token_1: int
    open_time: int
    recent_epoch: int

@dataclass
class Observation:
    block_timestamp: int
    cumulative_token_0_price_x32: int
    cumulative_token_1_price_x32: int

@dataclass
class ObservationState:
    initialized: int
    observation_index: int
    pool_id: PublicKey
    observations: List[Observation]
