import discord
from discord.ext import commands
from discord import app_commands
import asyncio
from datetime import datetime

class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="setlogchannel", description="Set the log channel for bot activity")
    @app_commands.describe(channel="The channel to send logs to")
    async def set_log_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Set log channel for the server"""
        # Check if user has admin permissions
        if not hasattr(interaction.user, 'guild_permissions') or not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You need administrator permissions to use this command.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Store log channel
        if interaction.guild:
            self.bot.log_channels[interaction.guild.id] = channel.id
            await self.bot.db.set_log_channel(interaction.guild.id, channel.id)
        
        embed = discord.Embed(
            title="✅ Log Channel Set",
            description=f"Bot activity will now be logged to {channel.mention}",
            color=discord.Color.green()
        )
        embed.set_footer(text="Made by kokex - xSportBS")
        
        await interaction.response.send_message(embed=embed)
        
        # Log this command usage
        await self.bot.log_command_usage(interaction, "setlogchannel")
    
    @app_commands.command(name="setchannelbot", description="Control bot visibility in specific channels")
    @app_commands.describe(
        channel="The channel to modify",
        visible="Whether the bot should be visible in this channel"
    )
    async def set_channel_bot(self, interaction: discord.Interaction, channel: discord.TextChannel, visible: bool):
        """Control bot visibility in channels"""
        if not hasattr(interaction.user, 'guild_permissions') or not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You need administrator permissions to use this command.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Store channel visibility setting
        if interaction.guild:
            await self.bot.db.set_channel_visibility(interaction.guild.id, channel.id, visible)
        
        status = "visible" if visible else "hidden"
        embed = discord.Embed(
            title="⚙️ Channel Settings Updated",
            description=f"Bot is now **{status}** in {channel.mention}",
            color=discord.Color.blue()
        )
        embed.set_footer(text="Made by kokex - xSportBS")
        
        await interaction.response.send_message(embed=embed)
        await self.bot.log_command_usage(interaction, "setchannelbot")
    
    @app_commands.command(name="dmuser", description="Send a DM to a specific user")
    @app_commands.describe(
        user="The user to send DM to",
        message="The message to send"
    )
    async def dm_user(self, interaction: discord.Interaction, user: discord.Member, message: str):
        """Send DM to a specific user"""
        if not hasattr(interaction.user, 'guild_permissions') or not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You need administrator permissions to use this command.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        try:
            # Create DM embed
            dm_embed = discord.Embed(
                title="📩 Message from xSportBS Server",
                description=message,
                color=discord.Color.blue(),
                timestamp=datetime.utcnow()
            )
            dm_embed.set_footer(text=f"Sent by {interaction.user.display_name} | Made by kokex - xSportBS")
            
            await user.send(embed=dm_embed)
            
            # Confirmation embed
            embed = discord.Embed(
                title="✅ DM Sent Successfully",
                description=f"Message sent to {user.mention}",
                color=discord.Color.green()
            )
            embed.add_field(name="Message", value=message, inline=False)
            embed.set_footer(text="Made by kokex - xSportBS")
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="❌ Failed to Send DM",
                description=f"Could not send DM to {user.mention}. They may have DMs disabled.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        await self.bot.log_command_usage(interaction, "dmuser")
    
    @app_commands.command(name="dmrole", description="Send a DM to all users with a specific role")
    @app_commands.describe(
        role="The role to send DMs to",
        message="The message to send"
    )
    async def dm_role(self, interaction: discord.Interaction, role: discord.Role, message: str):
        """Send DM to all users with a specific role"""
        if not hasattr(interaction.user, 'guild_permissions') or not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You need administrator permissions to use this command.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        await interaction.response.defer(ephemeral=True)
        
        success_count = 0
        failed_count = 0
        
        for member in role.members:
            try:
                dm_embed = discord.Embed(
                    title="📩 Message from xSportBS Server",
                    description=message,
                    color=discord.Color.blue(),
                    timestamp=datetime.utcnow()
                )
                dm_embed.set_footer(text=f"Sent by {interaction.user.display_name} | Made by kokex - xSportBS")
                
                await member.send(embed=dm_embed)
                success_count += 1
                
            except discord.Forbidden:
                failed_count += 1
            
            # Small delay to avoid rate limits
            await asyncio.sleep(0.5)
        
        # Send summary
        embed = discord.Embed(
            title="📊 DM Role Summary",
            color=discord.Color.blue()
        )
        embed.add_field(name="✅ Successful", value=str(success_count), inline=True)
        embed.add_field(name="❌ Failed", value=str(failed_count), inline=True)
        embed.add_field(name="👥 Total Members", value=str(len(role.members)), inline=True)
        embed.set_footer(text="Made by kokex - xSportBS")
        
        await interaction.followup.send(embed=embed, ephemeral=True)
        await self.bot.log_command_usage(interaction, "dmrole")

async def setup(bot):
    await bot.add_cog(AdminCog(bot))