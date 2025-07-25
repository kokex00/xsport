import os
import asyncio
from bot import XSportBSBot
from keep_alive import keep_alive

async def main():
    """Main entry point for the bot"""
    # Start the keep-alive server
    keep_alive()
    
    # Get bot token from environment
    token = os.getenv("DISCORD_TOKEN", "your_bot_token_here")
    
    if token == "your_bot_token_here":
        print("⚠️  Warning: Using default token. Please set DISCORD_TOKEN environment variable.")
    
    # Initialize and run the bot
    bot = XSportBSBot()
    
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        print("\n🛑 Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
