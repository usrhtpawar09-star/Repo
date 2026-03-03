"""
⚡ ULTIMATE WAIFU CATCHER BOT - CONFIGURATION ⚡
"""

import os
from typing import Dict, List, Set

# 🔑 TELEGRAM API CONFIGURATION
BOT_TOKEN = "8424950811:AAE-Jf6wfsPDjsu7J-iqPHlPCDEkq61UXH4"
API_ID = 36455116
API_HASH = "dddbb57121805c7b1434734390ff2e08"
OWNER_ID = 8327837344

# Sudo Users (Admin access)
SUDO_USERS: List[int] = [OWNER_ID]

# 🗄️ DATABASE CONFIGURATION
MONGODB_URL = "mongodb+srv://usrhtffdbr:miku1234@cluster0.jhvwttf.mongodb.net/?appName=Cluster0"
DB_NAME = "UltimateWaifuBot"
REDIS_URL = None 

# 🤖 BOT SETTINGS
BOT_USERNAME = "the_mahibot" 
BOT_NAME = "🏆 Ultimate Waifu Catcher"
SUPPORT_CHAT = None 
UPDATE_CHANNEL = None
LOG_CHANNEL = None 

# 🎮 GAME SETTINGS
MESSAGE_THRESHOLD = 80 
SPAWN_COOLDOWN = 300 
MAX_SPAWN_PER_HOUR = 12 
MAX_GUESSES_PER_SPAWN = 3 
GUESS_COOLDOWN = 4
GUESS_TIME_LIMIT = 60 

# REWARDS & DROPS
REWARD_COINS = {"common": 10, "uncommon": 25, "rare": 75, "epic": 200, "legendary": 800, "mythical": 2500}
REWARD_GEMS = {"common": 0, "uncommon": 0, "rare": 1, "epic": 2, "legendary": 5, "mythical": 15}

# ⭐ RARITY SYSTEM
RARITY_TIERS = {
    "common": {
        "name": "⚪ Common", "emoji": "⚪", "chance": 65.0,
        "min_stats": {"attack": 10, "defense": 10, "hp": 50},
        "max_stats": {"attack": 30, "defense": 30, "hp": 100},
    },
    "uncommon": {
        "name": "🟢 Uncommon", "emoji": "🟢", "chance": 25.0,
        "min_stats": {"attack": 25, "defense": 25, "hp": 80},
        "max_stats": {"attack": 50, "defense": 50, "hp": 150},
    },
    "rare": {
        "name": "🔵 Rare", "emoji": "🔵", "chance": 7.0,
        "min_stats": {"attack": 45, "defense": 45, "hp": 120},
        "max_stats": {"attack": 80, "defense": 80, "hp": 220},
    },
    "epic": {
        "name": "🟣 Epic", "emoji": "🟣", "chance": 2.5,
        "min_stats": {"attack": 70, "defense": 70, "hp": 180},
        "max_stats": {"attack": 120, "defense": 120, "hp": 320},
    },
    "legendary": {
        "name": "🟡 Legendary", "emoji": "🟡", "chance": 0.45,
        "min_stats": {"attack": 110, "defense": 110, "hp": 280},
        "max_stats": {"attack": 180, "defense": 180, "hp": 480},
    },
    "mythical": {
        "name": "🔴 Mythical", "emoji": "🔴", "chance": 0.05,
        "min_stats": {"attack": 170, "defense": 170, "hp": 400},
        "max_stats": {"attack": 250, "defense": 250, "hp": 650},
    },
}

# 💰 ECONOMY SYSTEM
COIN_NAME = "🪙 Coins"
GEM_NAME = "💎 Gems"
PREMIUM_NAME = "👑 Premium Tokens"

STARTING_COINS = 1000
STARTING_GEMS = 10
STARTING_PREMIUM = 0

# 🏦 BANK & ATM SETTINGS
BANK_SETTINGS = {
    "max_balance": 10_000_000, 
    "interest_rate": 0.02, 
    "interest_max": 100_000, 
    "deposit_fee": 0, 
    "withdrawal_fee": 0.01,
    "min_deposit": 100,
    "min_withdrawal": 50,
}

# 💳 LOAN SYSTEM
LOAN_SETTINGS = {
    "max_loan_amount": 500_000,
    "interest_rate": 0.05, 
    "max_days": 7, 
    "credit_score_min": 0,
    "credit_score_max": 1000,
    "default_penalty": 50,
    "collateral_required_above": 100_000,
}

# 🎁 DAILY REWARDS
DAILY_REWARDS = {
    "base_coins": 500,
    "base_gems": 1,
    "streak_bonus": 0.1, 
    "max_streak": 30, 
    "streak_reset_hours": 48,
}

# 🗳️ VOTING SYSTEM
VOTE_SETTINGS = {
    "sites": {
        "topgg": {"reward_coins": 2000, "reward_gems": 5, "cooldown_hours": 12},
        "discordbotlist": {"reward_coins": 1500, "reward_gems": 3, "cooldown_hours": 12},
        "botsfordiscord": {"reward_coins": 1000, "reward_gems": 2, "cooldown_hours": 12},
    },
    "vote_streak_bonus": 0.15,
    "max_vote_streak": 7, 
}

# 🎰 MINI GAMES
SLOTS_SETTINGS = {
    "min_bet": 50, "max_bet": 50_000,
    "symbols":["🍒", "🍋", "🍇", "💎", "7️⃣", "🎰", "⭐"],
    "payouts": {
        "🍒🍒🍒": 2, "🍋🍋🍋": 3, "🍇🍇🍇": 5, "💎💎💎": 10,
        "7️⃣7️⃣7️⃣": 25, "🎰🎰🎰": 50, "⭐⭐⭐": 100,
    },
}

DICE_SETTINGS = {"min_bet": 100, "max_bet": 100_000}
COINFLIP_SETTINGS = {"min_bet": 50, "max_bet": 500_000}

# 🎴 GACHA/SUMMON SYSTEM
GACHA_SETTINGS = {
    "single_cost": 100, "multi_cost": 900,
    "premium_single": 50, "premium_multi": 450,
    "guaranteed_epic": 30, "pity_counter": 90,
}

# 🔄 TRADING SYSTEM
TRADE_SETTINGS = {
    "expiry_minutes": 30, "tax_percent": 5,
    "max_items": 10, "min_level": 5,
}

# 🏷️ AUCTION SYSTEM
AUCTION_SETTINGS = {
    "min_duration": 3600, "max_duration": 604800,
    "fee_percent": 3, "bid_increment": 1.05,
}

# 👥 GUILD/CLAN SYSTEM
GUILD_SETTINGS = {
    "creation_cost": 50_000, "max_members": 50,
    "max_name_length": 30, "max_description_length": 200, "min_level": 10,
}

# 📊 LEVEL SYSTEM
LEVEL_SETTINGS = {
    "base_xp": 100, "xp_multiplier": 1.5, "max_level": 1000,
    "catch_xp": {"common": 10, "uncommon": 20, "rare": 40, "epic": 80, "legendary": 150, "mythical": 300},
    "guess_xp": 25, "vote_xp": 50, "daily_xp": 30,
}

LOG_LEVEL = "INFO"
