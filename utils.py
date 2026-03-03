"""
🏆 ULTIMATE WAIFU CATCHER BOT - MAIN ENTRY POINT
Cleaned up Monolithic setup mapped onto modern PyTgBot Architecture.
"""

import logging
from datetime import datetime
from telegram import Update
from telegram.ext import (Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters)

import config
import commands

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def post_init(application: Application) -> None:
    logger.info(f"🚀 {config.BOT_NAME} startup. Current Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    cmnds =[
        ("start", "🎮 Start the bot"), ("help", "📖 Help list"), ("profile", "👤 Profile Info"),
        ("balance", "💰 Coins and bank check"), ("bank", "🏦 Core Bank ops"), ("catch", "🏃 Spawn waifus in chat!"), 
        ("gacha", "🎰 Standard menu"), ("guess", "🤔 Guess Active"), ("daily", "📅 Dailies & claim")
    ]
    await application.bot.set_my_commands(cmnds)
    logger.info("📋 Base App Bot Commands injected safely.")

async def error_handler(update, context):
    logger.error(f"❌ Error logic routing fault! - Payload trace : {context.error}")
    if update and update.effective_message: await update.effective_message.reply_text("⚠️ Processing encountered crash condition!")

def main() -> None:
    print(f"""
    ======================================
      🌟 Waifu Boot : Mode (Production)
       Starting Main loop architecture
       Token Inject Valid & OK {config.BOT_TOKEN[:6]}
    ======================================
    """)
    app = Application.builder().token(config.BOT_TOKEN).post_init(post_init).build()
    
    # 🎯 Handler injections Mapping Block 
    mappings = {
        "start": commands.start_handler, "help": commands.help_handler, "about": commands.about_handler,
        "profile": commands.profile_handler, "me": commands.profile_handler, "inv": commands.inventory_handler,
        "inventory": commands.inventory_handler, "collection": commands.collection_handler, "bal": commands.balance_handler,
        "balance": commands.balance_handler, "bank": commands.bank_handler, "atm": commands.atm_handler,
        "deposit": commands.deposit_handler, "withdraw": commands.withdraw_handler, "loan": commands.loan_handler,
        "repay": commands.repay_handler, "transfer": commands.transfer_handler, "catch": commands.catch_handler,
        "waifu": commands.waifu_info_handler, "fav": commands.favorite_handler, "favorite": commands.favorite_handler,
        "unfav": commands.unfavorite_handler, "gacha": commands.gacha_handler, "summon": commands.summon_handler,
        "pity": commands.pity_handler, "trade": commands.trade_handler, "buy": commands.buy_handler,
        "market": commands.market_handler, "sell": commands.sell_handler, "guess": commands.guessgame_handler,
        "hint": commands.hint_handler, "giveup": commands.giveup_handler, "slots": commands.slots_handler,
        "dice": commands.dice_handler, "coinflip": commands.coinflip_handler, "daily": commands.daily_handler,
        "streak": commands.streak_handler, "claim": commands.claim_handler, "evolve": commands.evolve_handler,
        "leaderboard": commands.leaderboard_handler, "topguilds": commands.top_guilds_handler, 
        "auction": commands.auction_handler, "guild": commands.guild_handler, "marry": commands.marry_handler,
        "hug": commands.hug_handler, "pat": commands.pat_handler, "addcoins": commands.add_coins_handler
    }

    # Iterate dictionary above and directly add command-types.
    for k, v in mappings.items(): app.add_handler(CommandHandler(k, v))
    
    # Implicit & Callback Fallback Handlers
    app.add_handler(CallbackQueryHandler(commands.accept_trade_handler, pattern="^accept_trade:"))
    app.add_handler(CallbackQueryHandler(commands.decline_trade_handler, pattern="^decline_trade:"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, commands.guess_handler))

    # Global Exception fall-over Catch handling & Polling Initialization.
    app.add_error_handler(error_handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
