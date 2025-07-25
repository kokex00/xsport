import discord
from discord.ext import commands, tasks
from discord import app_commands
import asyncio
from datetime import datetime, timedelta
import pytz
from utils.translations import get_translation
from utils.timezone_handler import convert_timezone
# Translation views removed as requested

class MatchesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_matches = {}
        self.match_counter = 1
        
        # Start the reminder task
        self.reminder_task.start()
    
    async def cog_unload(self):
        self.reminder_task.cancel()
    
    @tasks.loop(minutes=1)
    async def reminder_task(self):
        """Check for matches that need reminders"""
        current_time = datetime.utcnow().replace(tzinfo=pytz.UTC)
        
        for match_id, match_data in list(self.active_matches.items()):
            match_time = match_data['start_time']
            
            # 10 minute reminder
            if not match_data.get('reminded_10') and current_time >= match_time - timedelta(minutes=10):
                await self.send_match_reminder(match_data, 10)
                self.active_matches[match_id]['reminded_10'] = True
            
            # 3 minute reminder
            elif not match_data.get('reminded_3') and current_time >= match_time - timedelta(minutes=3):
                await self.send_match_reminder(match_data, 3)
                self.active_matches[match_id]['reminded_3'] = True
    
    @reminder_task.before_loop
    async def before_reminder_task(self):
        await self.bot.wait_until_ready()
    
    async def send_match_reminder(self, match_data, minutes):
        """Send DM reminders to role members"""
        guild = self.bot.get_guild(match_data['guild_id'])
        if not guild:
            return
        
        role = guild.get_role(match_data['role_id'])
        if not role:
            return
        
        # Get user's language preference or use default
        language = match_data.get('language', 'en')
        
        for member in role.members:
            try:
                # Convert time to user's timezone
                user_time = convert_timezone(match_data['start_time'], language)
                
                embed = discord.Embed(
                    title=f"⏰ Match Reminder - {minutes} minutes!",
                    description=f"**Match:** {match_data['title']}\n**Time:** {user_time}\n**Teams:** {match_data['teams']}",
                    color=discord.Color.orange(),
                    timestamp=datetime.utcnow()
                )
                embed.set_footer(text="BOT - xSportBS")
                
                await member.send(embed=embed)
                
            except discord.Forbidden:
                continue
            
            await asyncio.sleep(0.5)  # Rate limit protection
    
    @app_commands.command(name="creatematch", description="Create a new match with scheduling")
    @app_commands.describe(
        title="Match title",
        teams="Teams playing (e.g., Team A vs Team B)",
        start_time="Match start time (YYYY-MM-DD HH:MM)",
        role="Role to notify for this match",
        image="Upload an image for the match"
    )
    async def create_match(
        self, 
        interaction: discord.Interaction, 
        title: str, 
        teams: str, 
        start_time: str,
        role: discord.Role,
        image: discord.Attachment = None
    ):
        """Create a new match"""
        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You need administrator permissions to create matches.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            # Parse the start time
            match_datetime = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
            match_datetime = pytz.UTC.localize(match_datetime)
            
        except ValueError:
            embed = discord.Embed(
                title="❌ Invalid Time Format",
                description="Please use the format: YYYY-MM-DD HH:MM (e.g., 2025-01-25 15:30)",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Check if time is in the future
        if match_datetime <= datetime.utcnow().replace(tzinfo=pytz.UTC):
            embed = discord.Embed(
                title="❌ Invalid Time",
                description="Match time must be in the future.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Handle image upload
        image_url = None
        if image:
            if image.content_type.startswith('image/'):
                image_url = image.url
            else:
                embed = discord.Embed(
                    title="❌ Invalid File",
                    description="Please upload an image file.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        
        # Create match entry
        match_id = self.match_counter
        self.match_counter += 1
        
        # Detect language based on interaction locale or default to English
        language = getattr(interaction.locale, 'name', 'en')[:2] if hasattr(interaction, 'locale') else 'en'
        if language not in ['en', 'pt', 'es']:
            language = 'en'
        
        match_data = {
            'id': match_id,
            'title': title,
            'teams': teams,
            'start_time': match_datetime,
            'role_id': role.id,
            'guild_id': interaction.guild.id,
            'creator_id': interaction.user.id,
            'language': language,
            'image_url': image_url,
            'reminded_10': False,
            'reminded_3': False
        }
        
        self.active_matches[match_id] = match_data
        
        # Convert time for display
        display_time = convert_timezone(match_datetime, language)
        
        # Create response embed
        embed = discord.Embed(
            title="⚽ Match Created Successfully!",
            description=f"**Match ID:** {match_id}\n**Title:** {title}\n**Teams:** {teams}\n**Start Time:** {display_time}\n**Notify Role:** {role.mention}",
            color=discord.Color.green(),
            timestamp=datetime.utcnow()
        )
        
        if image_url:
            embed.set_image(url=image_url)
        
        embed.set_footer(text="BOT - xSportBS")
        
        # Create translation view
        embed_data = {
            "title_key": "match_created",
            "description_key": "match_created_desc",
            "color": discord.Color.green(),
            "image_url": image_url,
            "fields": [
                {"name_key": "match_id", "value_key": str(match_id), "inline": True},
                {"name_key": "title", "value_key": title, "inline": True},
                {"name_key": "teams", "value_key": teams, "inline": True},
                {"name_key": "start_time", "value_key": display_time, "inline": False},
                {"name_key": "notify_role", "value_key": role.mention, "inline": False}
            ]
        }
        
        view = TranslationView(embed_data, interaction)
        await interaction.response.send_message(embed=embed, view=view)
        
        # Store in database
        await self.bot.db.create_match(match_data)
        await self.bot.log_command_usage(interaction, "creatematch")
    
    @app_commands.command(name="endmatch", description="End an active match")
    @app_commands.describe(match_id="The ID of the match to end")
    async def end_match(self, interaction: discord.Interaction, match_id: int):
        """End an active match"""
        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You need administrator permissions to end matches.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        if match_id not in self.active_matches:
            embed = discord.Embed(
                title="❌ Match Not Found",
                description=f"No active match found with ID {match_id}.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        match_data = self.active_matches[match_id]
        del self.active_matches[match_id]
        
        embed = discord.Embed(
            title="🏁 Match Ended",
            description=f"**Match:** {match_data['title']}\n**Teams:** {match_data['teams']}\n**Duration:** Match completed",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        embed.set_footer(text="BOT - xSportBS")
        
        await interaction.response.send_message(embed=embed)
        
        # Update database
        await self.bot.db.end_match(match_id)
        await self.bot.log_command_usage(interaction, "endmatch")
    
    @app_commands.command(name="listmatches", description="List all active matches")
    async def list_matches(self, interaction: discord.Interaction):
        """List all active matches"""
        if not self.active_matches:
            embed = discord.Embed(
                title="📋 Active Matches",
                description="No active matches at the moment.",
                color=discord.Color.blue()
            )
            embed.set_footer(text="BOT - xSportBS")
            await interaction.response.send_message(embed=embed)
            return
        
        # Detect user's language preference
        language = getattr(interaction.locale, 'name', 'en')[:2] if hasattr(interaction, 'locale') else 'en'
        if language not in ['en', 'pt', 'es']:
            language = 'en'
        
        embed = discord.Embed(
            title="📋 Active Matches",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        for match_id, match_data in self.active_matches.items():
            display_time = convert_timezone(match_data['start_time'], language)
            
            embed.add_field(
                name=f"Match {match_id}: {match_data['title']}",
                value=f"**Teams:** {match_data['teams']}\n**Time:** {display_time}\n**Role:** <@&{match_data['role_id']}>",
                inline=False
            )
        
        embed.set_footer(text="BOT - xSportBS")
        
        # Create translation view
        embed_data = {
            "title_key": "active_matches",
            "description_key": "active_matches_desc",
            "color": discord.Color.blue(),
            "fields": []
        }
        
        for match_id, match_data in self.active_matches.items():
            display_time = convert_timezone(match_data['start_time'], language)
            embed_data["fields"].append({
                "name_key": f"match_{match_id}",
                "value_key": f"**Teams:** {match_data['teams']}\n**Time:** {display_time}\n**Role:** <@&{match_data['role_id']}>",
                "inline": False
            })
        
        view = TranslationView(embed_data, interaction)
        await interaction.response.send_message(embed=embed, view=view)
        await self.bot.log_command_usage(interaction, "listmatches")

async def setup(bot):
    await bot.add_cog(MatchesCog(bot))
