import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime
from utils.image_handler import process_image

class UtilityCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="embed", description="Create a custom embed with image upload from device gallery")
    @app_commands.describe(
        title="Embed title",
        description="Embed description",
        color="Embed color (hex code, e.g., #FF0000)",
        image="Upload an image from your device gallery"
    )
    async def create_embed(
        self, 
        interaction: discord.Interaction, 
        title: str, 
        description: str,
        color: str = "#0099FF",
        image: discord.Attachment = None
    ):
        """Create a custom embed with image upload from device gallery"""
        if not hasattr(interaction.user, 'guild_permissions') or not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(
                title="❌ Access Denied",
                description="You need administrator permissions to create custom embeds.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Parse color
        try:
            if color.startswith('#'):
                color_int = int(color[1:], 16)
            else:
                color_int = int(color, 16)
            embed_color = discord.Color(color_int)
        except ValueError:
            embed_color = discord.Color.blue()
        
        # Handle image upload from device gallery
        image_url = None
        if image and hasattr(image, 'content_type') and image.content_type and image.content_type.startswith('image/'):
            # Process the uploaded image
            try:
                processed_url = await process_image(image)
                image_url = processed_url or image.url
            except:
                image_url = image.url
        elif image:
            embed = discord.Embed(
                title="❌ Invalid File",
                description="Please upload an image file from your device gallery.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return
        
        # Create the custom embed
        custom_embed = discord.Embed(
            title=title,
            description=description,
            color=embed_color,
            timestamp=datetime.utcnow()
        )
        
        if image_url:
            custom_embed.set_image(url=image_url)
        
        custom_embed.set_footer(text="Made by kokex - xSportBS")
        
        await interaction.response.send_message(embed=custom_embed)
        await self.bot.log_command_usage(interaction, "embed")
    
    @app_commands.command(name="serverinfo", description="Display server information")
    async def server_info(self, interaction: discord.Interaction):
        """Display detailed server information"""
        guild = interaction.guild
        if not guild:
            return
        
        # Get member counts
        total_members = guild.member_count or 0
        humans = len([m for m in guild.members if not m.bot])
        bots = len([m for m in guild.members if m.bot])
        
        # Get channel counts
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        categories = len(guild.categories)
        
        embed = discord.Embed(
            title=f"📊 {guild.name} Server Information",
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        if guild.icon:
            embed.set_thumbnail(url=guild.icon.url)
        
        # Server details
        owner_mention = guild.owner.mention if guild.owner else 'Unknown'
        embed.add_field(
            name="📋 General Info",
            value=f"**Owner:** {owner_mention}\n"
                  f"**Created:** <t:{int(guild.created_at.timestamp())}:F>\n"
                  f"**Server ID:** {guild.id}\n"
                  f"**Verification Level:** {guild.verification_level.name.title()}",
            inline=False
        )
        
        # Member statistics
        embed.add_field(
            name="👥 Members",
            value=f"**Total:** {total_members}\n**Humans:** {humans}\n**Bots:** {bots}",
            inline=True
        )
        
        # Channel statistics
        embed.add_field(
            name="📺 Channels",
            value=f"**Text:** {text_channels}\n**Voice:** {voice_channels}\n**Categories:** {categories}",
            inline=True
        )
        
        # Role count
        embed.add_field(
            name="🎭 Roles",
            value=str(len(guild.roles)),
            inline=True
        )
        
        # Boost information
        if guild.premium_subscription_count and guild.premium_subscription_count > 0:
            embed.add_field(
                name="✨ Nitro Boosts",
                value=f"**Level:** {guild.premium_tier}\n**Boosts:** {guild.premium_subscription_count}",
                inline=True
            )
        
        embed.set_footer(text="Made by kokex - xSportBS")
        
        await interaction.response.send_message(embed=embed)
        await self.bot.log_command_usage(interaction, "serverinfo")
    
    @app_commands.command(name="userinfo", description="Display user information")
    @app_commands.describe(user="The user to get information about")
    async def user_info(self, interaction: discord.Interaction, user: discord.Member = None):
        """Display detailed user information"""
        if user is None:
            if isinstance(interaction.user, discord.Member):
                user = interaction.user
            else:
                embed = discord.Embed(
                    title="❌ Error",
                    description="User information not available in DMs.",
                    color=discord.Color.red()
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        
        embed = discord.Embed(
            title=f"👤 {user.display_name}",
            color=user.color if user.color != discord.Color.default() else discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        
        embed.set_thumbnail(url=user.display_avatar.url)
        
        # Basic info
        embed.add_field(
            name="📋 Basic Info",
            value=f"**Username:** {user.name}\n"
                  f"**Discriminator:** #{user.discriminator}\n"
                  f"**ID:** {user.id}\n"
                  f"**Bot:** {'Yes' if user.bot else 'No'}",
            inline=False
        )
        
        # Dates
        joined_timestamp = int(user.joined_at.timestamp()) if user.joined_at else 0
        embed.add_field(
            name="📅 Dates",
            value=f"**Account Created:** <t:{int(user.created_at.timestamp())}:F>\n"
                  f"**Joined Server:** <t:{joined_timestamp}:F>",
            inline=False
        )
        
        # Roles
        if len(user.roles) > 1:
            roles = [role.mention for role in user.roles[1:]]  # Skip @everyone
            roles_text = ", ".join(roles[:10])  # Limit to first 10 roles
            if len(user.roles) > 11:
                roles_text += f" and {len(user.roles) - 11} more..."
            
            embed.add_field(
                name=f"🎭 Roles ({len(user.roles) - 1})",
                value=roles_text,
                inline=False
            )
        
        # Permissions
        if user.guild_permissions.administrator:
            embed.add_field(
                name="🔑 Key Permissions",
                value="Administrator",
                inline=True
            )
        else:
            key_perms = []
            if user.guild_permissions.manage_guild:
                key_perms.append("Manage Server")
            if user.guild_permissions.manage_roles:
                key_perms.append("Manage Roles")
            if user.guild_permissions.manage_channels:
                key_perms.append("Manage Channels")
            if user.guild_permissions.manage_messages:
                key_perms.append("Manage Messages")
            
            if key_perms:
                embed.add_field(
                    name="🔑 Key Permissions",
                    value=", ".join(key_perms[:3]),
                    inline=True
                )
        
        embed.set_footer(text="Made by kokex - xSportBS")
        
        await interaction.response.send_message(embed=embed)
        await self.bot.log_command_usage(interaction, "userinfo")

async def setup(bot):
    await bot.add_cog(UtilityCog(bot))