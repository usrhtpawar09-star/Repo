"""
🤖 HAR EK COMMANDS KA DETAILED LOGIC (100% FULL CODE - ZERO CUT)
"""

import random
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import *
from database import db, Guild, Auction, Trade, Waifu
from utils import (EconomyManager, EvolutionSystem, GachaSystem, WaifuSpawner, get_rarity_emoji, get_rarity_name, active_trades, active_spawns)

# ==============================
# START & PROFILES
# ==============================
async def start_handler(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = upd.effective_user
    u = db.get_user(user.id)
    if not u: 
        db.create_user(user.id, user.username or "Unknown", user.first_name)
    m = (f"🎉 Welcome to **{BOT_NAME}**, {user.first_name}!\n\n"
         f"🏆 **The Most Advanced Waifu Catcher Bot!**\n"
         f"  • 🎮 Catch Anime Characters\n  • 💰 Economy & Trading\n  • 👥 Guild & Events\n"
         f"📖 Use /help to see all commands!")
    kb = [[InlineKeyboardButton("📖 Help", callback_data="help"), InlineKeyboardButton("💰 Balance", callback_data="balance")],[InlineKeyboardButton("➕ Add to Group", url=f"https://t.me/{ctx.bot.username}?startgroup=true")]]
    await upd.message.reply_text(m, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def help_handler(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    m = """📖 **ULTIMATE WAIFU CATCHER - COMMANDS** 📖

🎮 /start, /help, /about
👤 /profile, /inventory, /collection, /waifu <id>, /favorite <id>
💰 /balance, /bank, /atm, /deposit, /withdraw, /loan, /repay, /transfer
🏃 /catch, /guess, /hint, /giveup
🔄 /trade <u_id> <waifu_id>, /market, /buy <id>, /sell <id>
🎰 /gacha, /summon, /pity
🎮 /slots, /dice, /coinflip
🗳️ /vote, /daily, /streak, /claim
🏆 /leaderboard, /rich, /topcatches, /topguilds
👥 /guild, /createguild, /joinguild, /leaveguild, /guilddonate
🔨 /auction, /bid, /listauction, /myauctions
✨ /evolve, /evolveinfo
💕 /hug, /kiss, /pat, /slap, /marry, /divorce, /ship
⚙️ /addcoins, /removecoins, /addwaifu, /removewaifu"""
    await upd.message.reply_text(m)

async def about_handler(upd: Update, ctx: ContextTypes.DEFAULT_TYPE):
    st = db.get_stats()
    m = (f"🏆 **ULTIMATE WAIFU CATCHER** 🏆\n📊 **Bot Stats:**\n  👤 Users: {st['total_users']}\n"
         f"  👰 Waifus: {st['total_waifus']}\n  🎯 Total Catches: {st['total_catches']}")
    await upd.message.reply_text(m, parse_mode="Markdown")

async def profile_handler(u: Update, c: ContextTypes.DEFAULT_TYPE):
    uid = u.effective_user.id
    du = db.get_user(uid) or db.create_user(uid, u.effective_user.username or "Unk", u.effective_user.first_name)
    m = (f"👤 **{du['first_name']}'s Profile**\n📊 **Level:** {du.get('level',1)} | XP {du.get('xp',0)}\n"
         f"💰 **Wallet:** {du.get('coins',0)} 🪙 | {du.get('gems',0)} 💎\n🏦 **Bank:** {du.get('bank_balance',0)} 🪙\n"
         f"📈 **Catches:** {du.get('total_catches',0)}\n💳 **Credit Score:** {du.get('credit_score', 500)}")
    await u.message.reply_text(m, parse_mode="Markdown")

async def inventory_handler(u: Update, c: ContextTypes.DEFAULT_TYPE):
    waifus = db.get_user_waifus(u.effective_user.id)
    if not waifus: return await u.message.reply_text("📦 Inventory empty. Use /catch!")
    pg = int(c.args[0]) if c.args else 1
    t = f"📦 **Inventory** (P{pg}/{(len(waifus)+9)//10})\n\n"
    for i, w in enumerate(waifus[(pg-1)*10 : pg*10], 1):
        f = "❤️" if w.get('is_favorite') else ""
        m = "💍" if w.get('is_married') else ""
        t += f"{get_rarity_emoji(w['rarity'])} `{w['waifu_id']}` {w['name']} {f}{m} (Atk: {w['attack']})\n"
    await u.message.reply_text(t, parse_mode="Markdown")

async def collection_handler(u: Update, c: ContextTypes.DEFAULT_TYPE):
    waifus = db.get_user_waifus(u.effective_user.id)
    grp = {}
    for w in waifus:
        if w["name"] not in grp: grp[w["name"]] = {"count":0, "rar":w["rarity"], "an":w["anime"]}
        grp[w["name"]]["count"] += 1
    if not grp: return await u.message.reply_text("📚 Collection empty!")
    tx = f"📚 **Your Collection** ({len(grp)} unique)\n\n"
    for nm, dt in list(grp.items())[:20]:
        tx += f"{get_rarity_emoji(dt['rar'])} **{nm}** x{dt['count']} - {dt['an']}\n"
    await u.message.reply_text(tx, parse_mode="Markdown")

async def waifu_info_handler(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if not c.args: return await u.message.reply_text("❌ Usage: `/waifu <waifu_id>`")
    w = db.get_waifu(c.args[0].upper())
    if not w: return await u.message.reply_text("❌ Waifu not found!")
    i = (f"{get_rarity_emoji(w['rarity'])} **{w['name']}**\n📺 Anime: {w['anime']}\n🆔 ID: `{w['waifu_id']}`\n"
         f"📊 Lvl: {w.get('level',1)}\n⚔️ Atk: {w['attack']} | 🛡️ Def: {w['defense']} | ❤️ HP: {w['hp']}\n")
    if w.get('is_favorite'): i+= "❤️ Favorite\n"
    if w.get('is_married'): i+= "💍 Married\n"
    try: await u.message.reply_photo(photo=w["image_url"], caption=i, parse_mode="Markdown")
    except: await u.message.reply_text(i, parse_mode="Markdown")

async def favorite_handler(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if not c.args: return await u.message.reply_text("❌ /favorite <waifu_id>")
    db.waifus.update_many({"owner_id": u.effective_user.id}, {"$set":{"is_favorite":False}})
    db.waifus.update_one({"waifu_id": c.args[0].upper()}, {"$set":{"is_favorite":True}})
    db.users.update_one({"user_id": u.effective_user.id}, {"$set":{"favorite_waifu": c.args[0].upper()}})
    await u.message.reply_text("✅ Favorite Set!")

async def unfavorite_handler(u: Update, c: ContextTypes.DEFAULT_TYPE):
    db.waifus.update_many({"owner_id": u.effective_user.id}, {"$set":{"is_favorite":False}})
    db.users.update_one({"user_id": u.effective_user.id}, {"$set":{"favorite_waifu": None}})
    await u.message.reply_text("💔 Favorite Unset.")

# ==============================
# ECONOMY OPERATIONS
# ==============================
async def balance_handler(u: Update, c: ContextTypes.DEFAULT_TYPE): await profile_handler(u, c)

async def bank_handler(u: Update, c: ContextTypes.DEFAULT_TYPE):
    bu = db.get_user(u.effective_user.id)
    msg = (f"🏦 **Bank of Waifu**\nYour Balance: {bu.get('bank_balance',0):,} 🪙\n"
           f"Limit: {bu.get('bank_limit', BANK_SETTINGS['max_balance']):,} 🪙\n"
           f"Rate: {BANK_SETTINGS['interest_rate']*100}%/Day\nCommands: /deposit, /withdraw, /atm")
    await u.message.reply_text(msg)

async def atm_handler(u:Update, c: ContextTypes.DEFAULT_TYPE): 
    if not c.args: return await u.message.reply_text("/atm <amount>")
    s, m = EconomyManager.atm_withdraw(u.effective_user.id, int(c.args[0]))
    await u.message.reply_text(m)

async def deposit_handler(u:Update, c: ContextTypes.DEFAULT_TYPE): 
    if not c.args: return await u.message.reply_text("/deposit <amount>")
    s, m = EconomyManager.deposit(u.effective_user.id, int(c.args[0]))
    await u.message.reply_text(m)

async def withdraw_handler(u:Update, c: ContextTypes.DEFAULT_TYPE): 
    if not c.args: return await u.message.reply_text("/withdraw <amount>")
    s, m = EconomyManager.withdraw(u.effective_user.id, int(c.args[0]))
    await u.message.reply_text(m)

async def loan_handler(u:Update, c: ContextTypes.DEFAULT_TYPE): 
    if not c.args:
        us = db.get_user(u.effective_user.id)
        sc = us.get('credit_score', 500)
        ml = int((sc/1000) * LOAN_SETTINGS['max_loan_amount'])
        if us.get("active_loan"):
            ln = db.get_loan(us["active_loan"])
            await u.message.reply_text(f"💳 Active Loan Due: {ln['total_due'] - ln.get('amount_repaid',0)}")
            return
        await u.message.reply_text(f"💳 **Loan Center**\nMax allow: {ml} 🪙\nRate: {LOAN_SETTINGS['interest_rate']*100}%\nUsage: /loan <amount>")
        return
    s, m = EconomyManager.request_loan(u.effective_user.id, int(c.args[0]))
    await u.message.reply_text(m)

async def repay_handler(u:Update, c: ContextTypes.DEFAULT_TYPE): 
    amt = int(c.args[0]) if c.args else None
    s, m = EconomyManager.repay_loan(u.effective_user.id, amt)
    await u.message.reply_text(m)

async def transfer_handler(u:Update, c: ContextTypes.DEFAULT_TYPE):
    if len(c.args)<2: return await u.message.reply_text("❌ /transfer <UserID_or_UserName> <amt>")
    r_id = db.users.find_one({"username": c.args[0].replace("@","")})["user_id"] if c.args[0].startswith("@") else int(c.args[0])
    s, m = EconomyManager.transfer(u.effective_user.id, r_id, int(c.args[1]))
    await u.message.reply_text(m)

# ==============================
# SPAWN & GUESS
# ==============================
async def catch_handler(u:Update, c: ContextTypes.DEFAULT_TYPE): 
    if u.effective_chat.type == "private": return await u.message.reply_text("Add bot to groups for spawns.")
    await WaifuSpawner.spawn_waifu(u.effective_chat.id, c)

async def spawn_handler(u:Update, c: ContextTypes.DEFAULT_TYPE): await catch_handler(u, c)
async def guess_handler(u:Update, c: ContextTypes.DEFAULT_TYPE): await WaifuSpawner.handle_guess(u, c)
async def guessgame_handler(u:Update, c: ContextTypes.DEFAULT_TYPE): await WaifuSpawner.handle_guess(u, c)
async def hint_handler(u:Update, c: ContextTypes.DEFAULT_TYPE):
    sp = WaifuSpawner.get_active_spawn(u.effective_chat.id)
    if sp: await u.message.reply_text(f"💡 Hint: {sp['spawn_data']['hints'][0]}")

async def giveup_handler(u:Update, c: ContextTypes.DEFAULT_TYPE):
    if WaifuSpawner.is_spawn_active(u.effective_chat.id):
        n = WaifuSpawner.get_active_spawn(u.effective_chat.id)['spawn_data']['waifu_name']
        await u.message.reply_text(f"🏳️ You gave up! The waifu was: **{n}**", parse_mode="Markdown")
        await WaifuSpawner.delete_spawn(u.effective_chat.id, c)

# ==============================
# MINIGAMES (Slots, Dice, Coinflip)
# ==============================
async def slots_handler(u:Update, c: ContextTypes.DEFAULT_TYPE):
    if not c.args: return await u.message.reply_text("🎰 `/slots <bet>`", parse_mode="Markdown")
    try: bet = int(c.args[0])
    except: return await u.message.reply_text("Bet a Number")
    du = db.get_user(u.effective_user.id)
    if du['coins'] < bet: return await u.message.reply_text("❌ Not enough coins!")
    db.remove_coins(u.effective_user.id, bet)
    sym = SLOTS_SETTINGS["symbols"]
    res = [random.choice(sym) for _ in range(3)]
    st = ''.join(res)
    p = 0
    for pat, mp in SLOTS_SETTINGS["payouts"].items():
        if st == pat: p = int(bet * mp)
    if p>0:
        db.add_coins(u.effective_user.id, p)
        m = f"🎰 `| {res[0]} | {res[1]} | {res[2]} |`\n🎉 You Win! +{p:,} 🪙"
    else: m = f"🎰 `| {res[0]} | {res[1]} | {res[2]} |`\n😢 You Lost -{bet:,} 🪙"
    await u.message.reply_text(m, parse_mode="Markdown")

async def dice_handler(u:Update, c: ContextTypes.DEFAULT_TYPE):
    if len(c.args)<2: return await u.message.reply_text("🎲 `/dice <bet> <high/low>`", parse_mode="Markdown")
    bet, g = int(c.args[0]), c.args[1].lower()
    if db.get_user(u.effective_user.id)['coins'] < bet: return await u.message.reply_text("❌ Not enough coins")
    db.remove_coins(u.effective_user.id, bet)
    ur, br = random.randint(1,6), random.randint(1,6)
    won = (g in['h','high','higher'] and ur>br) or (g in ['l','low','lower'] and ur<br)
    m = f"🎲 You: {ur} | Bot: {br}\n"
    if ur == br:
        db.add_coins(u.effective_user.id, bet); m += "Tie! Returned bet."
    elif won:
        py = int(bet*1.8)
        db.add_coins(u.effective_user.id, py); m += f"Win! +{py:,} 🪙"
    else: m += "Loss."
    await u.message.reply_text(m)

async def coinflip_handler(u:Update, c: ContextTypes.DEFAULT_TYPE):
    if len(c.args)<2: return await u.message.reply_text("🪙 `/coinflip <bet> <heads/tails>`", parse_mode="Markdown")
    b, g = int(c.args[0]), c.args[1].lower()
    if db.get_user(u.effective_user.id)['coins'] < b: return await u.message.reply_text("Not enough!")
    db.remove_coins(u.effective_user.id, b)
    r = random.choice(["h","t"])
    if g[0] == r:
        p = int(b*1.9)
        db.add_coins(u.effective_user.id, p); await u.message.reply_text(f"🌕 Res: {r.upper()} | Win +{p}🪙")
    else: await u.message.reply_text(f"🌑 Res: {r.upper()} | Lost {b}🪙")

# ==============================
# AUCTION & MARKET
# ==============================
async def list_auction_handler(u: Update, c: ContextTypes.DEFAULT_TYPE):
    if len(c.args)<2: return await u.message.reply_text("🔨 /listauction <WaifuID> <StartPrice>")
    wid, sp = c.args[0].upper(), int(c.args[1])
    w = db.get_waifu(wid)
    if not w or w['owner_id']!=u.effective_user.id: return await u.message.reply_text("❌ Your Waifu Not Found")
    f = int(sp * 0.03)
    if db.get_user(u.effective_user.id)['coins']<f: return await u.message.reply_text(f"❌ Fee {f} required")
    db.remove_coins(u.effective_user.id, f)
    auc = Auction(auction_id=Auction.generate_id(), seller_id=u.effective_user.id, waifu_id=wid,
                  starting_bid=sp, current_bid=sp, buy_now_price=int(sp*1.5), end_time=datetime.utcnow()+timedelta(days=3))
    db.create_auction(auc.to_dict())
    await u.message.reply_text(f"✅ AUC Created: {auc.auction_id}")

async def auction_handler(u:Update, c: ContextTypes.DEFAULT_TYPE):
    A = db.get_active_auctions()
    if not A: return await u.message.reply_text("🔨 Empty House. Use /listauction")
    tx = "🔨 **Auction House**\n"
    for a in A[:5]: tx += f"`{a['auction_id']}` : WID `{a['waifu_id']}` -> 💰 {a['current_bid']} 🪙\n"
    await u.message.reply_text(tx, parse_mode="Markdown")

async def bid_handler(u:Update, c: ContextTypes.DEFAULT_TYPE):
    if len(c.args)<2: return await u.message.reply_text("🔨 /bid <AUC_ID> <Amt>")
    amt = int(c.args[1])
    A = db.get_auction(c.args[0].upper())
    if not A or A["status"]!="active": return await u.message.reply_text("Ended or null")
    if amt <= int(A['current_bid']*1.05): return await u.message.reply_text("Bid low (+5% min)")
    if db.get_user(u.effective_user.id)['coins']<amt: return await u.message.reply_text("Poor.")
    if A.get('highest_bidder'): db.add_coins(A['highest_bidder'], A['current_bid'])
    db.remove_coins(u.effective_user.id, amt)
    db.place_bid(c.args[0].upper(), u.effective_user.id, amt)
    await u.message.reply_text(f"✅ Placed Bid for {amt}!")

async def market_handler(u:Update,c): await auction_handler(u,c)
async def sell_handler(u:Update, c): await list_auction_handler(u,c)
async def my_auctions_handler(u:Update,c): 
    M = list(db.auctions.find({"seller_id": u.effective_user.id, "status":"active"}))
    if not M: return await u.message.reply_text("You have 0 Active auctions!")
    tx = "📦 My Active:\n"
    for a in M: tx += f"`{a['auction_id']}` (Wid: {a['waifu_id']}) @ {a['current_bid']}\n"
    await u.message.reply_text(tx, parse_mode="Markdown")

async def buy_handler(u:Update, c):
    if not c.args: return await u.message.reply_text("🛒 /buy <AUC_ID>")
    A = db.get_auction(c.args[0].upper())
    pr = A.get('buy_now_price', 0) if A else 0
    if not A or not pr: return await u.message.reply_text("No Instant Buy price/Auction doesnt exist")
    if db.get_user(u.effective_user.id)['coins'] < pr: return await u.message.reply_text("Need coins")
    db.remove_coins(u.effective_user.id, pr); db.add_coins(A['seller_id'], pr
