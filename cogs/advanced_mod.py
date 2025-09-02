import discord
from discord.ext import commands
from datetime import datetime
import asyncio

class AdvancedModerationCog(commands.Cog):
    """Advanced moderation features for Kitten Mod"""
    
    def __init__(self, bot):
        self.bot = bot
        self.locked_channels = set()
    
    @commands.command(name='slowmode')
    @commands.has_permissions(manage_channels=True)
    async def set_slowmode(self, ctx, seconds: int):
        """Set channel slowmode with cute kitten messages"""
        
        if seconds < 0 or seconds > 21600:  # Discord limit is 6 hours
            embed = discord.Embed(
                title="🐱 Invalid Slowmode Time",
                description="Meow! Slowmode must be between 0 and 21600 seconds (6 hours)! 🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        try:
            await ctx.channel.edit(slowmode_delay=seconds)
            
            if seconds == 0:
                embed = discord.Embed(
                    title="🐱 Slowmode Disabled",
                    description="Meow! Everyone can chat as fast as they want again! No more waiting! 🐾💕",
                    color=discord.Color.from_rgb(144, 238, 144)
                )
            else:
                # Convert seconds to readable format
                if seconds < 60:
                    time_str = f"{seconds} seconds"
                elif seconds < 3600:
                    minutes = seconds // 60
                    time_str = f"{minutes} minute{'s' if minutes != 1 else ''}"
                else:
                    hours = seconds // 3600
                    minutes = (seconds % 3600) // 60
                    time_str = f"{hours}h {minutes}m" if minutes > 0 else f"{hours} hour{'s' if hours != 1 else ''}"
                
                embed = discord.Embed(
                    title="🐱 Slowmode Activated",
                    description=f"Meow! I've set a {time_str} cooldown between messages. This helps keep chat nice and organized! 🐾⏰",
                    color=discord.Color.from_rgb(255, 192, 203)
                )
            
            embed.add_field(
                name="📝 Set by:",
                value=f"{ctx.author.mention}",
                inline=True
            )
            embed.add_field(
                name="📍 Channel:",
                value=f"{ctx.channel.mention}",
                inline=True
            )
            
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="🐱 Kitty Can't Help",
                description="Meow! I don't have permission to change slowmode in this channel! 🥺",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
    
    @commands.command(name='lockdown')
    @commands.has_permissions(manage_channels=True)
    async def lockdown_channel(self, ctx, duration: int = 0):
        """Lock down a channel temporarily (duration in minutes, 0 = permanent)"""
        
        if ctx.channel.id in self.locked_channels:
            embed = discord.Embed(
                title="🐱 Already Locked Down",
                description="Meow! This channel is already locked down! Use `!unlock` to open it back up! 🔒",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        try:
            # Get @everyone role
            everyone_role = ctx.guild.default_role
            
            # Remove send message permissions
            await ctx.channel.set_permissions(
                everyone_role,
                send_messages=False,
                reason=f"Lockdown by {ctx.author} via Kitten Mod"
            )
            
            self.locked_channels.add(ctx.channel.id)
            
            if duration > 0:
                embed = discord.Embed(
                    title="🔒 Channel Locked Down!",
                    description=f"Meow! I've temporarily locked this channel for {duration} minute{'s' if duration != 1 else ''}. Only moderators can send messages now! 🐾🔒",
                    color=discord.Color.from_rgb(255, 192, 203),
                    timestamp=datetime.now()
                )
                
                # Schedule unlock
                asyncio.create_task(self._auto_unlock(ctx.channel, duration))
            else:
                embed = discord.Embed(
                    title="🔒 Channel Locked Down!",
                    description="Meow! I've locked this channel until a moderator uses `!unlock`. Only moderators can send messages now! 🐾🔒",
                    color=discord.Color.from_rgb(255, 192, 203),
                    timestamp=datetime.now()
                )
            
            embed.add_field(
                name="👮 Locked by:",
                value=f"{ctx.author.mention}",
                inline=True
            )
            
            if duration > 0:
                embed.add_field(
                    name="⏰ Duration:",
                    value=f"{duration} minute{'s' if duration != 1 else ''}",
                    inline=True
                )
            
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="🐱 Kitty Can't Help",
                description="Meow! I don't have permission to manage this channel! 🥺",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
    
    @commands.command(name='unlock')
    @commands.has_permissions(manage_channels=True)
    async def unlock_channel(self, ctx):
        """Unlock a previously locked channel"""
        
        if ctx.channel.id not in self.locked_channels:
            embed = discord.Embed(
                title="🐱 Not Locked Down",
                description="Meow! This channel isn't locked down! Everyone can already chat freely! 🐾💕",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        try:
            # Get @everyone role
            everyone_role = ctx.guild.default_role
            
            # Restore send message permissions
            await ctx.channel.set_permissions(
                everyone_role,
                send_messages=None,  # Reset to default
                reason=f"Unlocked by {ctx.author} via Kitten Mod"
            )
            
            self.locked_channels.discard(ctx.channel.id)
            
            embed = discord.Embed(
                title="🔓 Channel Unlocked!",
                description="Meow! The channel is open again! Everyone can chat freely now! Welcome back! 🐾✨",
                color=discord.Color.from_rgb(144, 238, 144),
                timestamp=datetime.now()
            )
            
            embed.add_field(
                name="👮 Unlocked by:",
                value=f"{ctx.author.mention}",
                inline=True
            )
            
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="🐱 Kitty Can't Help",
                description="Meow! I don't have permission to manage this channel! 🥺",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
    
    async def _auto_unlock(self, channel, duration_minutes):
        """Automatically unlock channel after duration"""
        await asyncio.sleep(duration_minutes * 60)  # Convert to seconds
        
        if channel.id in self.locked_channels:
            try:
                everyone_role = channel.guild.default_role
                await channel.set_permissions(
                    everyone_role,
                    send_messages=None,
                    reason="Auto-unlock via Kitten Mod"
                )
                
                self.locked_channels.discard(channel.id)
                
                embed = discord.Embed(
                    title="🔓 Auto-Unlock!",
                    description="Meow! The lockdown time is over! Everyone can chat again! 🐾⏰",
                    color=discord.Color.from_rgb(144, 238, 144),
                    timestamp=datetime.now()
                )
                # Cute kitten thumbnail would go here
                
                await channel.send(embed=embed)
            except discord.Forbidden:
                pass  # Can't send message or manage channel
    
    @commands.command(name='nickname')
    @commands.has_permissions(manage_nicknames=True)
    async def change_nickname(self, ctx, member: discord.Member, *, new_nickname: str = None):
        """Change someone's nickname with kitten flair"""
        
        # Check if we can modify this member
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="🐱 Can't Change That Nickname",
                description="Meow! I can't change the nickname of someone with a higher or equal role! 🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        old_nick = member.display_name
        
        try:
            await member.edit(nick=new_nickname if new_nickname else None, reason=f"Nickname changed by {ctx.author} via Kitten Mod")
            
            if new_nickname:
                embed = discord.Embed(
                    title="🐱 Nickname Changed!",
                    description=f"Meow! I've given {member.mention} a new nickname! 🏷️✨",
                    color=discord.Color.from_rgb(144, 238, 144),
                    timestamp=datetime.now()
                )
                embed.add_field(name="📛 Old Nickname:", value=old_nick, inline=True)
                embed.add_field(name="🆕 New Nickname:", value=new_nickname, inline=True)
            else:
                embed = discord.Embed(
                    title="🐱 Nickname Removed!",
                    description=f"Meow! I've removed {member.mention}'s nickname! They're back to their original name! 🐾",
                    color=discord.Color.from_rgb(144, 238, 144),
                    timestamp=datetime.now()
                )
                embed.add_field(name="📛 Old Nickname:", value=old_nick, inline=True)
                embed.add_field(name="🆕 Current Name:", value=member.name, inline=True)
            
            embed.add_field(name="👮 Changed by:", value=ctx.author.mention, inline=False)
            
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="🐱 Kitty Can't Help",
                description="Meow! I don't have permission to change nicknames, or this person has a higher role than me! 🥺",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
    
    @commands.command(name='role')
    @commands.has_permissions(manage_roles=True)
    async def manage_role(self, ctx, member: discord.Member, *, role_name: str):
        """Add or remove roles with cute kitten messages"""
        
        # Find the role
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if not role:
            embed = discord.Embed(
                title="🐱 Role Not Found",
                description=f"Meow! I can't find a role called '{role_name}'. Make sure you spelled it correctly! 🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        # Check if bot can manage this role
        if role >= ctx.guild.me.top_role:
            embed = discord.Embed(
                title="🐱 Role Too High",
                description="Meow! That role is higher than mine! I can't manage roles above my position! 🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        # Check if author can manage this role
        if role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="🐱 Can't Manage That Role",
                description="Meow! You can't manage a role that's higher than or equal to your highest role! 🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        try:
            if role in member.roles:
                # Remove role
                await member.remove_roles(role, reason=f"Role removed by {ctx.author} via Kitten Mod")
                embed = discord.Embed(
                    title="🐱 Role Removed!",
                    description=f"Meow! I've removed the {role.mention} role from {member.mention}! 🏷️➖",
                    color=discord.Color.from_rgb(255, 192, 203),
                    timestamp=datetime.now()
                )
                embed.add_field(name="🗑️ Action:", value="Role Removed", inline=True)
            else:
                # Add role
                await member.add_roles(role, reason=f"Role added by {ctx.author} via Kitten Mod")
                embed = discord.Embed(
                    title="🐱 Role Added!",
                    description=f"Meow! I've given {member.mention} the {role.mention} role! 🏷️➕",
                    color=discord.Color.from_rgb(144, 238, 144),
                    timestamp=datetime.now()
                )
                embed.add_field(name="✅ Action:", value="Role Added", inline=True)
            
            embed.add_field(name="👤 Member:", value=member.mention, inline=True)
            embed.add_field(name="👮 Managed by:", value=ctx.author.mention, inline=True)
            
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="🐱 Kitty Can't Help",
                description="Meow! I don't have permission to manage roles! 🥺",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AdvancedModerationCog(bot))