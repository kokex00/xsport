import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from utils.translations import get_translation
# Translation views removed as requested

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="help", description="Show all available commands and assistance")
    async def help_command(self, interaction: discord.Interaction):
        """Display help information with all available commands"""
        
        # Detect user's language preference
        language = getattr(interaction.locale, 'name', 'en')[:2] if hasattr(interaction, 'locale') else 'en'
        if language not in ['en', 'pt', 'es']:
            language = 'en'
        
        embed = discord.Embed(
            title="🤖 xSportBS Bot - Help & Commands",
            description="Welcome to xSportBS! Here are all available commands organized by category.",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        # Admin Commands
        admin_commands = [
            "`/setlogchannel` - Set the log channel for bot activity",
            "`/setchannelbot` - Control bot visibility in specific channels", 
            "`/dmuser` - Send a DM to a specific user",
            "`/dmrole` - Send a DM to all users with a specific role"
        ]
        
        embed.add_field(
            name="🔧 Admin Commands",
            value="\n".join(admin_commands),
            inline=False
        )
        
        # Match Management Commands
        match_commands = [
            "`/creatematch` - Create a new match with scheduling and image upload",
            "`/endmatch` - End an active match by ID",
            "`/listmatches` - List all currently active matches"
        ]
        
        embed.add_field(
            name="⚽ Match Management", 
            value="\n".join(match_commands),
            inline=False
        )
        
        # Utility Commands
        utility_commands = [
            "`/embed` - Create custom embeds with image upload from device",
            "`/serverinfo` - Display detailed server information",
            "`/userinfo` - Display user information",
            "`/help` - Show this help message"
        ]
        
        embed.add_field(
            name="🛠️ Utility Commands",
            value="\n".join(utility_commands),
            inline=False
        )
        
        # Features
        features = [
            "🌍 **Multilingual Support** - English, Portuguese, Spanish",
            "🔄 **Translation Buttons** - Instant language switching on all messages",
            "📱 **Image Upload** - Upload images from your device gallery/album",
            "⏰ **Smart Reminders** - Automatic DM reminders 10 & 3 minutes before matches",
            "🕒 **Timezone Conversion** - Times auto-convert based on language",
            "📊 **Activity Logging** - Complete bot activity tracking",
            "🔒 **Admin Protection** - Secure admin-only commands"
        ]
        
        embed.add_field(
            name="✨ Key Features",
            value="\n".join(features),
            inline=False
        )
        
        # Support Information
        embed.add_field(
            name="💬 Support",
            value="**Discord Server:** https://discord.gg/5BHpgnG8QP\n"
                  "**Technical Support:** kokex | Wo\n"
                  "**Need Help?** Use the translation buttons below!",
            inline=False
        )
        
        embed.set_footer(text="BOT - xSportBS")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/123456789/xsportbs_logo.png")
        
        # Create embed data for translations
        embed_data = {
            "title_key": "help_title",
            "description_key": "help_description", 
            "color": discord.Color.blue(),
            "fields": [
                {
                    "name_key": "admin_commands",
                    "value_key": "admin_commands_list",
                    "inline": False
                },
                {
                    "name_key": "match_commands", 
                    "value_key": "match_commands_list",
                    "inline": False
                },
                {
                    "name_key": "utility_commands",
                    "value_key": "utility_commands_list", 
                    "inline": False
                },
                {
                    "name_key": "features",
                    "value_key": "features_list",
                    "inline": False
                },
                {
                    "name_key": "support",
                    "value_key": "support_info",
                    "inline": False
                }
            ]
        }
        
        await interaction.response.send_message(embed=embed)
        await self.bot.log_command_usage(interaction, "help")
    
    @app_commands.command(name="about", description="About xSportBS Bot")
    async def about_command(self, interaction: discord.Interaction):
        """Display information about the bot"""
        
        embed = discord.Embed(
            title="🤖 About xSportBS Bot",
            description="A powerful multilingual Discord bot designed for server management and match scheduling.",
            color=discord.Color.gold(),
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="📝 Description",
            value="xSportBS is a comprehensive server management bot with advanced match scheduling, "
                  "multilingual support, and image upload capabilities. Built specifically for the xSportBS community.",
            inline=False
        )
        
        embed.add_field(
            name="🌟 Version & Features",
            value="**Version:** 2.0\n"
                  "**Languages:** English, Portuguese, Spanish\n"
                  "**Slash Commands:** ✅\n"
                  "**Image Upload:** ✅\n"
                  "**Translation Buttons:** ✅\n"
                  "**Match System:** ✅\n"
                  "**Admin Tools:** ✅",
            inline=True
        )
        
        embed.add_field(
            name="👨‍💻 Development Team",
            value="**Lead Developer:** kokex\n"
                  "**Support Team:** Wo\n"
                  "**Server:** xSportBS\n"
                  "**Discord:** https://discord.gg/5BHpgnG8QP",
            inline=True
        )
        
        embed.add_field(
            name="🚀 Getting Started",
            value="Use `/help` to see all available commands.\n"
                  "Administrators can use `/setlogchannel` to set up logging.\n"
                  "Create matches with `/creatematch` and upload images from your device!",
            inline=False
        )
        
        embed.set_footer(text="Made by kokex - xSportBS")
        
        # Create translation data
        embed_data = {
            "title_key": "about_title",
            "description_key": "about_description",
            "color": discord.Color.gold(),
            "fields": [
                {"name_key": "description", "value_key": "about_bot_desc", "inline": False},
                {"name_key": "version_features", "value_key": "version_info", "inline": True},
                {"name_key": "dev_team", "value_key": "team_info", "inline": True},
                {"name_key": "getting_started", "value_key": "start_info", "inline": False}
            ]
        }
        
        await interaction.response.send_message(embed=embed)
        await self.bot.log_command_usage(interaction, "about")

async def setup(bot):
    await bot.add_cog(HelpCog(bot))
