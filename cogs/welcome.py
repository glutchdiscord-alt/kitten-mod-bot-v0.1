import discord
from discord.ext import commands
from datetime import datetime

class WelcomeCog(commands.Cog):
    """Welcome system and autorole features for Kitten Mod"""
    
    def __init__(self, bot):
        self.bot = bot
        self.welcome_settings = {}  # Guild settings for welcome messages
        self.goodbye_settings = {}  # Guild settings for goodbye messages
        self.autorole_settings = {}  # Guild settings for autoroles
    
    @commands.command(name='welcome')
    @commands.has_permissions(administrator=True)
    async def setup_welcome(self, ctx, action: str, *, message_or_channel=None):
        """Set up cute welcome messages for new members"""
        guild_id = ctx.guild.id
        
        if action.lower() == 'setup':
            if not message_or_channel:
                embed = discord.Embed(
                    title="🐱 Welcome Setup Help",
                    description="Meow! Here's how to set up welcome messages:\n\n"
                               f"`!welcome setup #channel` - Set welcome channel\n"
                               f"`!welcome message <text>` - Set custom message\n"
                               f"`!welcome disable` - Turn off welcomes\n"
                               f"`!welcome test` - Test current settings\n\n"
                               f"**Current Status:** {'Enabled' if guild_id in self.welcome_settings else 'Disabled'} 🐾",
                    color=discord.Color.from_rgb(255, 192, 203)
                )
                # Cute kitten thumbnail would go here
                await ctx.send(embed=embed)
                return
            
            # Try to parse as channel
            try:
                channel = await commands.TextChannelConverter().convert(ctx, message_or_channel)
                self.welcome_settings[guild_id] = {
                    'channel_id': channel.id,
                    'message': None  # Will use default
                }
                
                embed = discord.Embed(
                    title="🐱 Welcome Channel Set!",
                    description=f"Meow! I'll now welcome new members in {channel.mention}! 🎉🐾",
                    color=discord.Color.from_rgb(144, 238, 144)
                )
                # Cute kitten thumbnail would go here
                await ctx.send(embed=embed)
                
            except commands.BadArgument:
                embed = discord.Embed(
                    title="🐱 Invalid Channel",
                    description="Meow! I can't find that channel. Please mention a valid channel like #general! 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
                # Cute kitten thumbnail would go here
                await ctx.send(embed=embed)
        
        elif action.lower() == 'message':
            if guild_id not in self.welcome_settings:
                embed = discord.Embed(
                    title="🐱 No Welcome Channel",
                    description="Meow! You need to set up a welcome channel first with `!welcome setup #channel`! 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
                # Cute kitten thumbnail would go here
                await ctx.send(embed=embed)
                return
            
            if not message_or_channel:
                embed = discord.Embed(
                    title="🐱 No Message Provided",
                    description="Meow! Please provide a welcome message! Use `{user}` to mention the new member and `{server}` for server name! 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
                # Cute kitten thumbnail would go here
                await ctx.send(embed=embed)
                return
            
            self.welcome_settings[guild_id]['message'] = message_or_channel
            
            embed = discord.Embed(
                title="🐱 Welcome Message Set!",
                description=f"Meow! Here's your new welcome message:\n\n{message_or_channel.replace('{user}', ctx.author.mention).replace('{server}', ctx.guild.name)} 🐾",
                color=discord.Color.from_rgb(144, 238, 144)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
        
        elif action.lower() == 'disable':
            if guild_id in self.welcome_settings:
                del self.welcome_settings[guild_id]
                embed = discord.Embed(
                    title="🐱 Welcome Disabled",
                    description="Meow! I've turned off welcome messages. I'll miss greeting new friends! 🥺🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
            else:
                embed = discord.Embed(
                    title="🐱 Welcome Already Off",
                    description="Meow! Welcome messages are already disabled! 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
        
        elif action.lower() == 'test':
            if guild_id not in self.welcome_settings:
                embed = discord.Embed(
                    title="🐱 No Welcome Setup",
                    description="Meow! Welcome messages aren't set up yet! Use `!welcome setup #channel` first! 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
                # Cute kitten thumbnail would go here
                await ctx.send(embed=embed)
                return
            
            # Test the welcome message
            await self._send_welcome_message(ctx.guild, ctx.author, test=True)
    
    @commands.command(name='goodbye')
    @commands.has_permissions(administrator=True) 
    async def setup_goodbye(self, ctx, action: str, *, message_or_channel=None):
        """Set up cute goodbye messages when members leave"""
        guild_id = ctx.guild.id
        
        if action.lower() == 'setup':
            if not message_or_channel:
                embed = discord.Embed(
                    title="🐱 Goodbye Setup Help",
                    description="Meow! Here's how to set up goodbye messages:\n\n"
                               f"`!goodbye setup #channel` - Set goodbye channel\n"
                               f"`!goodbye message <text>` - Set custom message\n"
                               f"`!goodbye disable` - Turn off goodbyes\n\n"
                               f"**Current Status:** {'Enabled' if guild_id in self.goodbye_settings else 'Disabled'} 🐾",
                    color=discord.Color.from_rgb(255, 192, 203)
                )
                # Cute kitten thumbnail would go here
                await ctx.send(embed=embed)
                return
            
            # Try to parse as channel
            try:
                channel = await commands.TextChannelConverter().convert(ctx, message_or_channel)
                self.goodbye_settings[guild_id] = {
                    'channel_id': channel.id,
                    'message': None  # Will use default
                }
                
                embed = discord.Embed(
                    title="🐱 Goodbye Channel Set!",
                    description=f"Meow! I'll say goodbye to members who leave in {channel.mention}! 👋🐾",
                    color=discord.Color.from_rgb(144, 238, 144)
                )
                # Cute kitten thumbnail would go here
                await ctx.send(embed=embed)
                
            except commands.BadArgument:
                embed = discord.Embed(
                    title="🐱 Invalid Channel",
                    description="Meow! I can't find that channel. Please mention a valid channel! 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
                # Cute kitten thumbnail would go here
                await ctx.send(embed=embed)
        
        elif action.lower() == 'message':
            if guild_id not in self.goodbye_settings:
                embed = discord.Embed(
                    title="🐱 No Goodbye Channel",
                    description="Meow! You need to set up a goodbye channel first with `!goodbye setup #channel`! 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
                # Cute kitten thumbnail would go here
                await ctx.send(embed=embed)
                return
            
            if not message_or_channel:
                embed = discord.Embed(
                    title="🐱 No Message Provided", 
                    description="Meow! Please provide a goodbye message! Use `{user}` for the member's name and `{server}` for server name! 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
                # Cute kitten thumbnail would go here
                await ctx.send(embed=embed)
                return
            
            self.goodbye_settings[guild_id]['message'] = message_or_channel
            
            embed = discord.Embed(
                title="🐱 Goodbye Message Set!",
                description=f"Meow! Here's your goodbye message:\n\n{message_or_channel.replace('{user}', ctx.author.display_name).replace('{server}', ctx.guild.name)} 🐾",
                color=discord.Color.from_rgb(144, 238, 144)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
        
        elif action.lower() == 'disable':
            if guild_id in self.goodbye_settings:
                del self.goodbye_settings[guild_id]
                embed = discord.Embed(
                    title="🐱 Goodbye Disabled",
                    description="Meow! I've turned off goodbye messages. 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
            else:
                embed = discord.Embed(
                    title="🐱 Goodbye Already Off",
                    description="Meow! Goodbye messages are already disabled! 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
    
    @commands.command(name='autorole')
    @commands.has_permissions(administrator=True)
    async def setup_autorole(self, ctx, action: str, *, role_name=None):
        """Set up automatic role assignment for new members"""
        guild_id = ctx.guild.id
        
        if action.lower() == 'set':
            if not role_name:
                embed = discord.Embed(
                    title="🐱 No Role Specified",
                    description="Meow! Please specify a role name! Example: `!autorole set Member` 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
                # Cute kitten thumbnail would go here
                await ctx.send(embed=embed)
                return
            
            # Find the role
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            if not role:
                embed = discord.Embed(
                    title="🐱 Role Not Found",
                    description=f"Meow! I can't find a role called '{role_name}'. Make sure it exists! 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
                # Cute kitten thumbnail would go here
                await ctx.send(embed=embed)
                return
            
            # Check if bot can assign this role
            if role >= ctx.guild.me.top_role:
                embed = discord.Embed(
                    title="🐱 Role Too High",
                    description="Meow! That role is higher than mine! I can't assign roles above my position! 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
                # Cute kitten thumbnail would go here
                await ctx.send(embed=embed)
                return
            
            self.autorole_settings[guild_id] = role.id
            
            embed = discord.Embed(
                title="🐱 Autorole Set!",
                description=f"Meow! I'll now automatically give new members the {role.mention} role! 🏷️✨",
                color=discord.Color.from_rgb(144, 238, 144)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
        
        elif action.lower() == 'disable':
            if guild_id in self.autorole_settings:
                del self.autorole_settings[guild_id]
                embed = discord.Embed(
                    title="🐱 Autorole Disabled",
                    description="Meow! I've turned off automatic role assignment! 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
            else:
                embed = discord.Embed(
                    title="🐱 Autorole Already Off",
                    description="Meow! Autorole is already disabled! 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
        
        elif action.lower() == 'status':
            if guild_id in self.autorole_settings:
                role = ctx.guild.get_role(self.autorole_settings[guild_id])
                if role:
                    embed = discord.Embed(
                        title="🐱 Autorole Status",
                        description=f"Meow! Autorole is enabled! New members get: {role.mention} 🏷️",
                        color=discord.Color.from_rgb(144, 238, 144)
                    )
                else:
                    # Role was deleted
                    del self.autorole_settings[guild_id]
                    embed = discord.Embed(
                        title="🐱 Autorole Broken",
                        description="Meow! The autorole was set to a role that no longer exists! It's been disabled. 🐾",
                        color=discord.Color.from_rgb(255, 182, 193)
                    )
            else:
                embed = discord.Embed(
                    title="🐱 Autorole Status",
                    description="Meow! Autorole is currently disabled! 🐾",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Handle new member events"""
        guild_id = member.guild.id
        
        # Send welcome message
        if guild_id in self.welcome_settings:
            await self._send_welcome_message(member.guild, member)
        
        # Assign autorole
        if guild_id in self.autorole_settings:
            role = member.guild.get_role(self.autorole_settings[guild_id])
            if role and role < member.guild.me.top_role:
                try:
                    await member.add_roles(role, reason="Autorole via Kitten Mod")
                except discord.Forbidden:
                    pass  # Bot lacks permissions
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Handle member leave events"""
        guild_id = member.guild.id
        
        # Send goodbye message
        if guild_id in self.goodbye_settings:
            await self._send_goodbye_message(member.guild, member)
    
    async def _send_welcome_message(self, guild, member, test=False):
        """Send welcome message to the configured channel"""
        settings = self.welcome_settings.get(guild.id)
        if not settings:
            return
        
        channel = guild.get_channel(settings['channel_id'])
        if not channel:
            return
        
        # Use custom message or default
        if settings['message']:
            description = settings['message'].replace('{user}', member.mention).replace('{server}', guild.name)
        else:
            description = f"🎉 Welcome to **{guild.name}**, {member.mention}!\n\nMeow! I'm so excited to have a new friend! Make yourself comfortable and don't hesitate to ask if you need anything! 🐾💕"
        
        embed = discord.Embed(
            title="🐱 New Friend Arrived!" + (" (Test)" if test else ""),
            description=description,
            color=discord.Color.from_rgb(144, 238, 144),
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="📊 Member Count:",
            value=f"{len(guild.members)} wonderful members! 🎊",
            inline=True
        )
        
        embed.add_field(
            name="📅 Account Created:",
            value=member.created_at.strftime("%Y-%m-%d"),
            inline=True
        )
        
        # Cute kitten thumbnail would go here
        embed.set_author(name=member.display_name, icon_url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass  # Bot lacks permissions
    
    async def _send_goodbye_message(self, guild, member):
        """Send goodbye message to the configured channel"""
        settings = self.goodbye_settings.get(guild.id)
        if not settings:
            return
        
        channel = guild.get_channel(settings['channel_id'])
        if not channel:
            return
        
        # Use custom message or default
        if settings['message']:
            description = settings['message'].replace('{user}', member.display_name).replace('{server}', guild.name)
        else:
            description = f"👋 **{member.display_name}** has left **{guild.name}**.\n\nMeow... I'll miss them! I hope they come back to visit sometime! 🐾💙"
        
        embed = discord.Embed(
            title="🐱 Goodbye Friend...",
            description=description,
            color=discord.Color.from_rgb(200, 200, 255),
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="📊 Member Count:",
            value=f"{len(guild.members)} members remaining",
            inline=True
        )
        
        # Cute kitten thumbnail would go here
        embed.set_author(name=member.display_name, icon_url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            pass  # Bot lacks permissions

async def setup(bot):
    await bot.add_cog(WelcomeCog(bot))