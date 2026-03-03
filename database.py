"""
🗄️ DATABASE CONNECTION & MODELS
"""

import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import uuid4
from dataclasses import dataclass, field
from pymongo import MongoClient, DESCENDING
from pymongo.collection import Collection
from pymongo.database import Database as MongoDatabase

from config import (MONGODB_URL, DB_NAME, STARTING_COINS, STARTING_GEMS, STARTING_PREMIUM, LOAN_SETTINGS)

logger = logging.getLogger(__name__)

# --- Models ---
@dataclass
class User:
    user_id: int
    username: str
    first_name: str
    coins: int = STARTING_COINS
    gems: int = STARTING_GEMS
    premium_tokens: int = STARTING_PREMIUM
    bank_balance: int = 0
    bank_limit: int = 100000
    level: int = 1
    xp: int = 0
    total_catches: int = 0
    unique_catches: int = 0
    favorite_waifu: Optional[str] = None
    married_to: Optional[str] = None
    guild_id: Optional[str] = None
    daily_streak: int = 0
    last_daily: Optional[datetime] = None
    vote_streak: int = 0
    last_vote: Dict[str, datetime] = field(default_factory=dict)
    credit_score: int = 500
    active_loan: Optional[str] = None
    pity_counter: int = 0
    total_spent: int = 0
    total_earned: int = 0
    achievements: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    last_active: datetime = field(default_factory=datetime.utcnow)
    def to_dict(self): return self.__dict__

@dataclass
class Waifu:
    waifu_id: str
    owner_id: int
    name: str
    anime: str
    rarity: str
    image_url: str
    attack: int
    defense: int
    hp: int
    speed: int = 50
    level: int = 1
    xp: int = 0
    is_favorite: bool = False
    is_married: bool = False
    obtained_at: datetime = field(default_factory=datetime.utcnow)
    @classmethod
    def generate_id(cls): return str(uuid4())[:8].upper()
    def to_dict(self): return self.__dict__

@dataclass
class Guild:
    guild_id: str
    name: str
    description: str
    owner_id: int
    members: List[int] = field(default_factory=list)
    total_contribution: int = 0
    guild_level: int = 1
    guild_xp: int = 0
    bank_balance: int = 0
    icon_url: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    @classmethod
    def generate_id(cls): return f"GUILD_{str(uuid4())[:6].upper()}"
    def to_dict(self): return self.__dict__

@dataclass
class Auction:
    auction_id: str
    seller_id: int
    waifu_id: str
    starting_bid: int
    current_bid: int
    highest_bidder: Optional[int] = None
    buy_now_price: Optional[int] = None
    bids: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "active"
    created_at: datetime = field(default_factory=datetime.utcnow)
    end_time: datetime = field(default_factory=datetime.utcnow)
    @classmethod
    def generate_id(cls): return f"AUC_{str(uuid4())[:8].upper()}"
    def to_dict(self): return self.__dict__

@dataclass
class Loan:
    loan_id: str
    user_id: int
    amount: int
    interest_rate: float
    total_due: int
    days_to_repay: int
    amount_repaid: int = 0
    status: str = "active"
    created_at: datetime = field(default_factory=datetime.utcnow)
    due_date: datetime = field(default_factory=datetime.utcnow)
    repaid_at: Optional[datetime] = None
    defaulted_at: Optional[datetime] = None
    @classmethod
    def generate_id(cls): return f"LOAN_{str(uuid4())[:8].upper()}"
    def to_dict(self): return self.__dict__

@dataclass
class Trade:
    trade_id: str
    sender_id: int
    receiver_id: int
    sender_waifus: List[str] = field(default_factory=list)
    receiver_waifus: List[str] = field(default_factory=list)
    sender_coins: int = 0
    receiver_coins: int = 0
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime = field(default_factory=datetime.utcnow)
    accepted_at: Optional[datetime] = None
    declined_at: Optional[datetime] = None
    @classmethod
    def generate_id(cls): return f"TRADE_{str(uuid4())[:8].upper()}"
    def to_dict(self): return self.__dict__

@dataclass
class Spawn:
    spawn_id: str
    chat_id: int
    waifu_name: str
    waifu_anime: str
    waifu_rarity: str
    waifu_image: str
    hints: List[str] = field(default_factory=list)
    guessed_by: List[int] = field(default_factory=list)
    caught_by: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime = field(default_factory=datetime.utcnow)
    @classmethod
    def generate_id(cls): return f"SPAWN_{str(uuid4())[:6].upper()}"
    def to_dict(self): return self.__dict__


# --- Main Connection & Database Wrapper ---
class DatabaseWrapper:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized: return
        try:
            self.client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
            self.db: MongoDatabase = self.client[DB_NAME]
            
            self.users = self.db["users"]
            self.waifus = self.db["waifus"]
            self.guilds = self.db["guilds"]
            self.auctions = self.db["auctions"]
            self.loans = self.db["loans"]
            self.trades = self.db["trades"]
            self.spawns = self.db["spawns"]
            self.analytics = self.db["analytics"]

            self._create_indexes()
            self._initialized = True
            logger.info("✅ Database connected successfully!")
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")

    def _create_indexes(self):
        self.users.create_index("user_id", unique=True)
        self.waifus.create_index("waifu_id", unique=True)
        self.guilds.create_index("guild_id", unique=True)
        self.auctions.create_index("auction_id", unique=True)
        self.loans.create_index("loan_id", unique=True)

    # Base Queries
    def get_user(self, user_id: int) -> Optional[Dict[str, Any]]:
        return self.users.find_one({"user_id": user_id})

    def create_user(self, user_id: int, username: str, first_name: str) -> Dict[str, Any]:
        usr = User(user_id=user_id, username=username, first_name=first_name)
        data = usr.to_dict()
        self.users.insert_one(data)
        return data

    def add_coins(self, user_id: int, amount: int):
        self.users.update_one({"user_id": user_id}, {"$inc": {"coins": amount, "total_earned": amount}})

    def remove_coins(self, user_id: int, amount: int):
        self.users.update_one({"user_id": user_id}, {"$inc": {"coins": -amount, "total_spent": amount}})

    def add_gems(self, user_id: int, amount: int):
        self.users.update_one({"user_id": user_id}, {"$inc": {"gems": amount}})

    def get_top_users(self, limit=10, sort_by="coins"):
        return list(self.users.find().sort(sort_by, DESCENDING).limit(limit))

    def get_waifu(self, waifu_id: str) -> Optional[Dict[str, Any]]:
        return self.waifus.find_one({"waifu_id": waifu_id})

    def get_user_waifus(self, user_id: int) -> List[Dict]:
        return list(self.waifus.find({"owner_id": user_id}))

    def count_user_waifus(self, user_id: int, rarity: str = None) -> int:
        q = {"owner_id": user_id}
        if rarity: q["rarity"] = rarity
        return self.waifus.count_documents(q)

    def add_waifu(self, waifu_data: Dict[str, Any]):
        self.waifus.insert_one(waifu_data)
        self.users.update_one({"user_id": waifu_data["owner_id"]}, {"$inc": {"total_catches": 1}})
    
    def transfer_waifu(self, waifu_id: str, from_id: int, to_id: int):
        self.waifus.update_one({"waifu_id": waifu_id, "owner_id": from_id}, {"$set": {"owner_id": to_id}})

    def delete_waifu(self, waifu_id: str):
        self.waifus.delete_one({"waifu_id": waifu_id})

    # System Entities wrappers (Guilds, Auctions, Loans, Trades)
    def get_guild(self, guild_id): return self.guilds.find_one({"guild_id": guild_id})
    def create_guild(self, data): self.guilds.insert_one(data)
    def get_top_guilds(self, limit=10): return list(self.guilds.find().sort("total_contribution", DESCENDING).limit(limit))

    def get_auction(self, auction_id): return self.auctions.find_one({"auction_id": auction_id})
    def create_auction(self, data): self.auctions.insert_one(data)
    def get_active_auctions(self): return list(self.auctions.find({"status": "active"}))
    def place_bid(self, auction_id, bidder_id, amount):
        self.auctions.update_one({"auction_id": auction_id}, {"$set": {"current_bid": amount, "highest_bidder": bidder_id}})
    
    def get_loan(self, loan_id): return self.loans.find_one({"loan_id": loan_id})
    def create_loan(self, data):
        self.loans.insert_one(data)
        self.users.update_one({"user_id": data["user_id"]}, {"$set": {"active_loan": data["loan_id"]}})
    def repay_loan(self, loan_id):
        loan = self.get_loan(loan_id)
        if loan:
            self.loans.update_one({"loan_id": loan_id}, {"$set": {"status": "repaid"}})
            self.users.update_one({"user_id": loan["user_id"]}, {"$set": {"active_loan": None}})
    def default_loan(self, loan_id):
        loan = self.get_loan(loan_id)
        if loan:
            self.loans.update_one({"loan_id": loan_id}, {"$set": {"status": "defaulted"}})
            self.users.update_one({"user_id": loan["user_id"]}, {"$set": {"active_loan": None}, "$inc": {"credit_score": -LOAN_SETTINGS["default_penalty"]}})
    
    def get_trade(self, trade_id): return self.trades.find_one({"trade_id": trade_id})
    def create_trade(self, data): self.trades.insert_one(data)
    def accept_trade(self, trade_id): self.trades.update_one({"trade_id": trade_id}, {"$set": {"status": "accepted"}})
    def decline_trade(self, trade_id): self.trades.update_one({"trade_id": trade_id}, {"$set": {"status": "declined"}})

    def get_stats(self) -> Dict[str, Any]:
        return {
            "total_users": self.users.count_documents({}),
            "total_waifus": self.waifus.count_documents({}),
            "total_guilds": self.guilds.count_documents({}),
            "total_catches": sum(user.get("total_catches", 0) for user in self.users.find())
        }

db = DatabaseWrapper()
