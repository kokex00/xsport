import discord
from discord.ext import commands
import os
import asyncio
from datetime import datetime
import pytz
from utils.translations import get_translation, LANGUAGES
from utils.database import Database

class XSportBSBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        
        super().__init__(
            command_prefix="!",
            intents=intents,
            description="xSportBS - Server Management & Match System Bot"
        )
        
        # Initialize database
        self.db = Database()
        
        # Bot configuration
        self.default_language = "en"
        self.supported_languages = ["en", "pt", "es"]
        
        # Log channels storage
        self.log_channels = {}
        
    async def setup_hook(self):
        """Load all cogs when bot starts"""
        cogs = [
            "cogs.admin",
            "cogs.matches", 
            "cogs.utility",
            "cogs.help"
        ]
        
        for cog in cogs:
            try:
                await self.load_extension(cog)
                print(f"✅ Loaded {cog}")
            except Exception as e:
                print(f"❌ Failed to load {cog}: {e}")
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            print(f"✅ Synced {len(synced)} slash commands")
        except Exception as e:
            print(f"❌ Failed to sync commands: {e}")
    
    async def on_ready(self):
        """Called when bot is ready"""
        print(f"🤖 {self.user} is now online!")
        print(f"📊 Connected to {len(self.guilds)} servers")
        
        # Set bot status
        activity = discord.Activity(
            type=discord.ActivityType.watching,
            name="xSportBS BOT |BEST BOT"
        )
        await self.change_presence(activity=activity)
        
        # Initialize database tables
        await self.db.init_tables()
    
    async def on_guild_join(self, guild):
        """Called when bot joins a new guild"""
        print(f"📥 Joined new server: {guild.name} (ID: {guild.id})")
        
        # Log to database
        await self.db.log_event("guild_join", guild.id, f"Joined server: {guild.name}")
    
    async def on_application_command_error(self, interaction, error):
        """Handle slash command errors"""
        if interaction.response.is_done():
            return
            
        embed = discord.Embed(
            title="❌ Error",
            description="An error occurred while processing your command.",
            color=discord.Color.red()
        )
        
        try:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except:
            pass
    
    async def log_command_usage(self, interaction, command_name):
        """Log slash command usage"""
        guild_id = interaction.guild.id if interaction.guild else 0
        user_id = interaction.user.id
        
        await self.db.log_command(command_name, guild_id, user_id)
        
        # Send to log channel if configured
        if guild_id in self.log_channels:
            channel = self.get_channel(self.log_channels[guild_id])
            if channel:
                embed = discord.Embed(
                    title="📝 Command Used",
                    description=f"**Command:** `/{command_name}`\n**User:** {interaction.user.mention}\n**Channel:** {interaction.channel.mention if interaction.channel else 'DM'}",
                    color=discord.Color.blue(),
                    timestamp=datetime.utcnow()
                )
                await channel.send(embed=embed)

# Translation views removed as requested
