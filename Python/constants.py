from solana.publickey import PublicKey

# Program IDs (non-devnet)
RAYDIUM_CP_PROGRAM_ID = PublicKey("CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C")
ADMIN_ID = PublicKey("GThUX1Atko4tqhN2NaiTazWSeFWMuiUvfFnyJyUghFMJ")
CREATE_POOL_FEE_RECEIVER_ID = PublicKey(
    "DNXgeM9EiiaAbaWvwjHj9fQQLAX5ZsfHyvmYUNRAdNC8"
)

# Program derived address seeds
AMM_CONFIG_SEED = b"amm_config"
POOL_SEED = b"pool"
POOL_LP_MINT_SEED = b"pool_lp_mint"
POOL_VAULT_SEED = b"pool_vault"
AUTH_SEED = b"vault_and_lp_mint_auth_seed"
OBSERVATION_SEED = b"observation"

# Instruction discriminators
INITIALIZE_DISCRIMINATOR = bytes.fromhex("afaf6d1f0d989bed")
SWAP_BASE_INPUT_DISCRIMINATOR = bytes.fromhex("8fbe5adac41e33de")
SWAP_BASE_OUTPUT_DISCRIMINATOR = bytes.fromhex("37d96256a34ab4ad")
WITHDRAW_DISCRIMINATOR = bytes.fromhex("b712469c946da122")
