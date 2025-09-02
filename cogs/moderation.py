import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio
import re
from typing import Optional
from utils.permissions import has_mod_permissions
from utils.logging import get_logger

logger = get_logger(__name__)

class ModerationCog(commands.Cog):
    """Moderation commands cog"""
    
    def __init__(self, bot):
        self.bot = bot
        self.warnings = {}  # In-memory storage for warnings
        self.muted_users = {}  # Track muted users
        self.mod_logs = []  # In-memory storage for moderation logs
        self.automod_settings = {}  # Auto-moderation settings per guild
        
        # Inappropriate content filters
        self.banned_words = [
            'spam', 'scam', 'hack', 'cheat'  # Basic filter words
        ]
        
        self.spam_threshold = 5  # Messages per 10 seconds
        self.user_message_history = {}
    
    @commands.Cog.listener()
    async def on_message(self, message):
        """Message filter for inappropriate content and bot mentions"""
        if message.author.bot:
            return
        
        # Check if bot is mentioned
        if self.bot.user.mentioned_in(message):
            # Create cute ping response
            embed = discord.Embed(
                title="🐱 Meow! Someone Called Me!",
                description=f"Hello there, {message.author.mention}! I'm Kitten Mod, your adorable moderation assistant! 🐾\n\nNeed help? Try `{self.bot.command_prefix}help` to see all my cute commands!\n\nI'm here to keep our server safe and cozy! 💕",
                color=discord.Color.from_rgb(255, 192, 203)
            )
            # Cute kitten thumbnail would go here
            
            # Add some random cute responses
            import random
            cute_responses = [
                "Purr purr! What can I help you with? 🐾",
                "Meow! Did someone need a fluffy moderator? ✨",
                "*stretches paws* I'm here to help! 🐱",
                "Mrow! Ready to keep things purrfect! 💕",
                "*blinks slowly* Hello friend! Need assistance? 😸"
            ]
            
            embed.add_field(
                name="💭 Kitten Says:",
                value=random.choice(cute_responses),
                inline=False
            )
            
            await message.channel.send(embed=embed)
            return
        
        # Check for banned words
        content_lower = message.content.lower()
        for word in self.banned_words:
            if word in content_lower:
                await message.delete()
                
                embed = discord.Embed(
                    title="🐱 Meow! Message Cleaned Up",
                    description=f"{message.author.mention}, I had to clean up your message because it had some naughty words! Let's keep things cute and friendly! 💕",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
                # Cute kitten thumbnail would go here
                warning_msg = await message.channel.send(embed=embed)
                
                # Delete warning message after 5 seconds
                await asyncio.sleep(5)
                try:
                    await warning_msg.delete()
                except:
                    pass
                return
        
        # Basic spam detection
        user_id = message.author.id
        now = datetime.now()
        
        if user_id not in self.user_message_history:
            self.user_message_history[user_id] = []
        
        # Add current message timestamp
        self.user_message_history[user_id].append(now)
        
        # Remove messages older than 10 seconds
        self.user_message_history[user_id] = [
            timestamp for timestamp in self.user_message_history[user_id]
            if now - timestamp < timedelta(seconds=10)
        ]
        
        # Check if user exceeded spam threshold
        if len(self.user_message_history[user_id]) > self.spam_threshold:
            try:
                # Delete recent messages
                async for msg in message.channel.history(limit=self.spam_threshold):
                    if msg.author.id == user_id:
                        await msg.delete()
                
                embed = discord.Embed(
                    title="🐱 Slow Down, Speedy!",
                    description=f"{message.author.mention}, you're typing too fast for this little kitten to keep up! Taking a short break to catch my breath... 😽",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
                # Cute kitten thumbnail would go here
                await message.channel.send(embed=embed)
                
                # Auto-mute for spam
                await self._mute_user(message.guild, message.author, duration_minutes=5, reason="Automatic: Spam detection")
                
            except discord.Forbidden:
                pass
    
    @commands.command(name='kick')
    @commands.has_permissions(kick_members=True)
    async def kick_user(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Kick a user from the server"""
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="🐱 Oopsie! Can't Do That",
                description="Meow! I can't help you with someone who has a higher rank than you. Even kittens have rules! 😸",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
            await ctx.send(embed=embed)
            return
        
        try:
            await member.kick(reason=f"Kicked by {ctx.author}: {reason}")
            
            embed = discord.Embed(
                title="🐾 Gently Escorted Out",
                description=f"**Kitty says goodbye to:** {member.mention} ({member.id})\n**Why:** {reason}\n**Helpful moderator:** {ctx.author.mention}\n\nMeow! Sometimes we need space to think! 🚪💕",
                color=discord.Color.from_rgb(255, 182, 193),
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
            
            await ctx.send(embed=embed)
            self._log_action("KICK", ctx.author, member, reason)
            
            logger.info(f"{ctx.author} kicked {member} for: {reason}")
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="🐱 Kitty Can't Help",
                description="Meow! I don't have the right permissions to help with this. Maybe ask a server admin to give me more powers? 🥺",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
            await ctx.send(embed=embed)
    
    @commands.command(name='ban')
    @commands.has_permissions(ban_members=True)
    async def ban_user(self, ctx, member: discord.Member, *, reason="No reason provided"):
        """Ban a user from the server"""
        if member.top_role >= ctx.author.top_role and ctx.author != ctx.guild.owner:
            embed = discord.Embed(
                title="🐱 Oopsie! Can't Do That",
                description="Meow! I can't help you with someone who has a higher rank than you. Even kittens have rules! 😸",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
            await ctx.send(embed=embed)
            return
        
        try:
            await member.ban(reason=f"Banned by {ctx.author}: {reason}", delete_message_days=1)
            
            embed = discord.Embed(
                title="🐱 Sent to the Naughty Corner",
                description=f"**Kitty had to ban:** {member.mention} ({member.id})\n**Why:** {reason}\n**Helpful moderator:** {ctx.author.mention}\n\nMeow! Sometimes we need a long timeout to think about our actions! 😿",
                color=discord.Color.from_rgb(255, 182, 193),
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
            
            await ctx.send(embed=embed)
            self._log_action("BAN", ctx.author, member, reason)
            
            logger.info(f"{ctx.author} banned {member} for: {reason}")
            
        except discord.Forbidden:
            embed = discord.Embed(
                title="🐱 Kitty Can't Help",
                description="Meow! I don't have the right permissions to help with this. Maybe ask a server admin to give me more powers? 🥺",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
            await ctx.send(embed=embed)
    
    @commands.command(name='unban')
    @commands.has_permissions(ban_members=True)
    async def unban_user(self, ctx, user_id: int):
        """Unban a user by their ID"""
        try:
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.unban(user, reason=f"Unbanned by {ctx.author}")
            
            embed = discord.Embed(
                title="🐱 Welcome Back Home!",
                description=f"**Kitty welcomed back:** {user.mention} ({user.id})\n**Kind moderator:** {ctx.author.mention}\n\nMeow! Everyone deserves a second chance! 🏠💕",
                color=discord.Color.from_rgb(144, 238, 144),
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
            
            await ctx.send(embed=embed)
            self._log_action("UNBAN", ctx.author, user, "Unbanned")
            
        except discord.NotFound:
            embed = discord.Embed(
                title="🐱 Kitty Can't Find Them",
                description="Meow! I can't find that person, or maybe they're not in the naughty corner anymore? 🤔🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
            await ctx.send(embed=embed)
    
    @commands.command(name='mute')
    @commands.has_permissions(manage_roles=True)
    async def mute_user(self, ctx, member: discord.Member, duration: str = "10m", *, reason="No reason provided"):
        """Mute a user for a specified duration"""
        # Parse duration
        duration_match = re.match(r'^(\d+)([smhd])$', duration.lower())
        if not duration_match:
            embed = discord.Embed(
                title="🐱 Confused Kitten",
                description="Meow! I don't understand that time format. Please use: `10m`, `1h`, `2d` (minutes, hours, days) 🕰️",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
            await ctx.send(embed=embed)
            return
        
        amount, unit = int(duration_match.group(1)), duration_match.group(2)
        
        # Convert to minutes
        duration_minutes = amount
        if unit == 's':
            duration_minutes = amount / 60
        elif unit == 'm':
            duration_minutes = amount
        elif unit == 'h':
            duration_minutes = amount * 60
        elif unit == 'd':
            duration_minutes = amount * 60 * 24
        
        await self._mute_user(ctx.guild, member, duration_minutes, reason, ctx.author)
        
        embed = discord.Embed(
            title="🤫 Quiet Time for Kitty!",
            description=f"**Little one taking a break:** {member.mention}\n**Quiet time:** {duration}\n**Why:** {reason}\n**Kind moderator:** {ctx.author.mention}\n\nMeow! Sometimes we all need a moment to think! 🐾💕",
            color=discord.Color.from_rgb(255, 182, 193),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
        
        await ctx.send(embed=embed)
    
    async def _mute_user(self, guild, member, duration_minutes, reason, moderator=None):
        """Helper method to mute a user"""
        # Create or get muted role
        muted_role = discord.utils.get(guild.roles, name="Muted")
        if not muted_role:
            muted_role = await guild.create_role(
                name="Muted",
                permissions=discord.Permissions(send_messages=False, speak=False),
                reason="Mute role for moderation"
            )
            
            # Set permissions for all channels
            for channel in guild.channels:
                await channel.set_permissions(muted_role, send_messages=False, speak=False)
        
        await member.add_roles(muted_role, reason=reason)
        
        # Store mute info
        self.muted_users[member.id] = {
            'guild_id': guild.id,
            'unmute_time': datetime.now() + timedelta(minutes=duration_minutes),
            'role': muted_role.id
        }
        
        # Schedule unmute
        asyncio.create_task(self._schedule_unmute(member, duration_minutes))
        
        if moderator:
            self._log_action("MUTE", moderator, member, f"{reason} ({duration_minutes}m)")
    
    async def _schedule_unmute(self, member, duration_minutes):
        """Schedule automatic unmute"""
        await asyncio.sleep(duration_minutes * 60)  # Convert to seconds
        
        if member.id in self.muted_users:
            guild = self.bot.get_guild(self.muted_users[member.id]['guild_id'])
            if guild:
                member = guild.get_member(member.id)
                if member:
                    muted_role = guild.get_role(self.muted_users[member.id]['role'])
                    if muted_role and muted_role in member.roles:
                        await member.remove_roles(muted_role, reason="Mute duration expired")
            
            del self.muted_users[member.id]
    
    @commands.command(name='unmute')
    @commands.has_permissions(manage_roles=True)
    async def unmute_user(self, ctx, member: discord.Member):
        """Unmute a user"""
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not muted_role or muted_role not in member.roles:
            embed = discord.Embed(
                title="🐱 Already Free to Speak!",
                description="Meow! This person isn't taking quiet time right now. They're free to chat! 🗣️🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
            await ctx.send(embed=embed)
            return
        
        await member.remove_roles(muted_role, reason=f"Unmuted by {ctx.author}")
        
        # Remove from muted users tracking
        if member.id in self.muted_users:
            del self.muted_users[member.id]
        
        embed = discord.Embed(
            title="🐱 Welcome Back to Chatting!",
            description=f"**Now free to speak:** {member.mention}\n**Kind moderator:** {ctx.author.mention}\n\nMeow! Quiet time is over! Hope you feel better now! 🗣️💕",
            color=discord.Color.from_rgb(144, 238, 144),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
        
        await ctx.send(embed=embed)
        self._log_action("UNMUTE", ctx.author, member, "Manual unmute")
    
    @commands.command(name='warn')
    @commands.has_permissions(manage_messages=True)
    async def warn_user(self, ctx, member: discord.Member, *, reason):
        """Warn a user"""
        guild_id = ctx.guild.id
        user_id = member.id
        
        # Initialize warning storage if needed
        if guild_id not in self.warnings:
            self.warnings[guild_id] = {}
        if user_id not in self.warnings[guild_id]:
            self.warnings[guild_id][user_id] = []
        
        # Add warning
        warning = {
            'reason': reason,
            'moderator': ctx.author.id,
            'timestamp': datetime.now().isoformat(),
            'id': len(self.warnings[guild_id][user_id]) + 1
        }
        
        self.warnings[guild_id][user_id].append(warning)
        
        embed = discord.Embed(
            title="🐱 Gentle Reminder from Kitten",
            description=f"**Little reminder for:** {member.mention}\n**What happened:** {reason}\n**Caring moderator:** {ctx.author.mention}\n**Reminder #:** {warning['id']}\n\nMeow! Let's try to be extra good next time! 🐾💕",
            color=discord.Color.from_rgb(255, 255, 224),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
        
        await ctx.send(embed=embed)
        self._log_action("WARN", ctx.author, member, reason)
        
        # Check if auto-moderation should trigger
        await self._check_automod(ctx.guild, member)
        
        # DM user about warning
        try:
            dm_embed = discord.Embed(
                title="🐱 Gentle Paw Tap from Kitten Mod",
                description=f"Meow! I wanted to send you a little reminder from **{ctx.guild.name}**\n\n**What happened:** {reason}\n**Caring moderator:** {ctx.author}\n\nNo worries! Everyone makes mistakes. Let's be extra awesome next time! 🐾💕",
                color=discord.Color.from_rgb(255, 255, 224)
            )
            dm_embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
            await member.send(embed=dm_embed)
        except:
            pass  # User has DMs disabled
    
    @commands.command(name='warnings')
    @commands.has_permissions(manage_messages=True)
    async def view_warnings(self, ctx, member: discord.Member):
        """View warnings for a user"""
        guild_id = ctx.guild.id
        user_id = member.id
        
        if guild_id not in self.warnings or user_id not in self.warnings[guild_id]:
            embed = discord.Embed(
                title="🐱 Clean Record!",
                description=f"{member.mention} has been such a good kitty! No reminders needed! 🐾💕",
                color=discord.Color.from_rgb(144, 238, 144)
            )
            embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
            await ctx.send(embed=embed)
            return
        
        user_warnings = self.warnings[guild_id][user_id]
        
        embed = discord.Embed(
            title=f"🐱 {member.display_name}'s Reminder History",
            description="Here's what this little one needs to remember:",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
        
        for warning in user_warnings[-5:]:  # Show last 5 warnings
            moderator = self.bot.get_user(warning['moderator'])
            mod_name = moderator.display_name if moderator else "Unknown"
            
            embed.add_field(
                name=f"🐾 Reminder #{warning['id']}",
                value=f"**What happened:** {warning['reason']}\n**Caring moderator:** {mod_name}\n**When:** {warning['timestamp'][:10]}",
                inline=False
            )
        
        embed.set_footer(text=f"💕 Total reminders: {len(user_warnings)} | Every mistake is a chance to grow!")
        await ctx.send(embed=embed)
    
    @commands.command(name='clear')
    @commands.has_permissions(manage_messages=True)
    async def clear_messages(self, ctx, amount: int):
        """Clear a specified number of messages"""
        if amount < 1 or amount > 100:
            embed = discord.Embed(
                title="🐱 Kitty Needs a Valid Number",
                description="Meow! Please give me a number between 1 and 100 so I know how many messages to clean up! 🧹",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
            await ctx.send(embed=embed)
            return
        
        deleted = await ctx.channel.purge(limit=amount + 1)  # +1 for the command message
        
        embed = discord.Embed(
            title="🧹 Kitty Cleaned Up!",
            description=f"Meow! I tidied up {len(deleted) - 1} messages for you! The chat looks much cleaner now! 🐾✨",
            color=discord.Color.from_rgb(144, 238, 144)
        )
        embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
        
        # Delete this message after 5 seconds
        msg = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        try:
            await msg.delete()
        except:
            pass
        
        self._log_action("CLEAR", ctx.author, None, f"Cleared {len(deleted) - 1} messages in {ctx.channel.name}")
    
    @commands.command(name='userinfo')
    async def user_info(self, ctx, member: Optional[discord.Member] = None):
        """Get information about a user"""
        if member is None:
            member = ctx.author
        
        embed = discord.Embed(
            title=f"🐱 Kitten's Info About: {member.display_name}",
            description="Here's what I know about this lovely person! 🐾",
            color=member.color if member.color != discord.Color.default() else discord.Color.from_rgb(255, 192, 203),
            timestamp=datetime.now()
        )
        
        embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
        
        embed.add_field(name="🏷️ Kitty Name", value=f"{member.name}#{member.discriminator if member.discriminator != '0' else ''}", inline=True)
        embed.add_field(name="🆔 ID Number", value=member.id, inline=True)
        embed.add_field(name="🟢 Current Status", value=str(member.status).title(), inline=True)
        
        embed.add_field(name="🎉 Birthday (Account)", value=member.created_at.strftime("%Y-%m-%d %H:%M UTC"), inline=True)
        embed.add_field(name="🏠 Joined Our Home", value=member.joined_at.strftime("%Y-%m-%d %H:%M UTC") if member.joined_at else "Unknown", inline=True)
        embed.add_field(name="🏆 Highest Role", value=member.top_role.mention, inline=True)
        
        # Count warnings
        guild_id = ctx.guild.id
        warning_count = 0
        if guild_id in self.warnings and member.id in self.warnings[guild_id]:
            warning_count = len(self.warnings[guild_id][member.id])
        
        embed.add_field(name="📝 Gentle Reminders", value=f"{warning_count} 🐾", inline=True)
        
        await ctx.send(embed=embed)
    
    @commands.command(name='removewarn')
    @commands.has_permissions(manage_messages=True)
    async def remove_warning(self, ctx, member: discord.Member, warning_id: int):
        """Remove a specific warning from a user"""
        guild_id = ctx.guild.id
        user_id = member.id
        
        if guild_id not in self.warnings or user_id not in self.warnings[guild_id]:
            embed = discord.Embed(
                title="🐱 No Reminders Found",
                description=f"{member.mention} doesn't have any reminders to remove! They've been such a good kitty! 🐾💕",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        user_warnings = self.warnings[guild_id][user_id]
        
        # Find and remove the warning
        removed_warning = None
        warning_found = False
        for i, warning in enumerate(user_warnings):
            if warning['id'] == warning_id:
                removed_warning = user_warnings.pop(i)
                warning_found = True
                break
        
        if not warning_found or removed_warning is None:
            embed = discord.Embed(
                title="🐱 Kitty Can't Find That Reminder",
                description=f"Meow! I couldn't find reminder #{warning_id} for {member.mention}. Maybe it was already removed? 🤔🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        # Clean up empty warning list
        if not user_warnings:
            del self.warnings[guild_id][user_id]
        
        embed = discord.Embed(
            title="🐱 Reminder Removed!",
            description=f"**Removed reminder for:** {member.mention}\n**Reminder #:** {warning_id}\n**What it was about:** {removed_warning['reason']}\n**Kind moderator:** {ctx.author.mention}\n\nMeow! Everyone deserves fresh starts! 🐾✨",
            color=discord.Color.from_rgb(144, 238, 144),
            timestamp=datetime.now()
        )
        # Cute kitten thumbnail would go here
        
        await ctx.send(embed=embed)
        self._log_action("REMOVE_WARN", ctx.author, member, f"Removed warning #{warning_id}: {removed_warning['reason']}")
    
    @commands.command(name='automod')
    @commands.has_permissions(administrator=True)
    async def setup_automod(self, ctx, warnings_threshold: int, action: str):
        """Set up automatic actions when users reach warning thresholds"""
        guild_id = ctx.guild.id
        
        valid_actions = ['kick', 'ban', 'mute']
        if action.lower() not in valid_actions:
            embed = discord.Embed(
                title="🐱 Confused Kitten",
                description=f"Meow! I don't understand that action. Please use one of these: `kick`, `ban`, or `mute` 🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        if warnings_threshold < 1 or warnings_threshold > 20:
            embed = discord.Embed(
                title="🐱 That's Too Many or Too Few!",
                description="Meow! Please choose a number between 1 and 20 warnings for the threshold! 🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        # Store automod settings
        if guild_id not in self.automod_settings:
            self.automod_settings[guild_id] = {}
        
        self.automod_settings[guild_id][warnings_threshold] = action.lower()
        
        action_descriptions = {
            'kick': 'gently escort them out 🚪',
            'ban': 'send them to the timeout corner 🏠',
            'mute': 'give them quiet time 🤫'
        }
        
        embed = discord.Embed(
            title="🐱 Automod Set Up!",
            description=f"**Threshold:** {warnings_threshold} reminders\n**Action:** {action_descriptions[action.lower()]}\n**Set by:** {ctx.author.mention}\n\nMeow! Now I'll automatically help when someone gets too many reminders! 🐾⚡",
            color=discord.Color.from_rgb(144, 238, 144),
            timestamp=datetime.now()
        )
        # Cute kitten thumbnail would go here
        
        await ctx.send(embed=embed)
        self._log_action("AUTOMOD_SET", ctx.author, None, f"Set {warnings_threshold} warnings -> {action}")
    
    async def _check_automod(self, guild, member):
        """Check if automod actions should be triggered"""
        guild_id = guild.id
        user_id = member.id
        
        if guild_id not in self.automod_settings or not self.automod_settings[guild_id]:
            return
        
        if guild_id not in self.warnings or user_id not in self.warnings[guild_id]:
            return
        
        warning_count = len(self.warnings[guild_id][user_id])
        
        # Check if any threshold is met (check highest threshold first)
        for threshold in sorted(self.automod_settings[guild_id].keys(), reverse=True):
            if warning_count >= threshold:
                action = self.automod_settings[guild_id][threshold]
                await self._execute_automod_action(guild, member, action, threshold)
                break
    
    async def _execute_automod_action(self, guild, member, action, threshold):
        """Execute the automod action"""
        try:
            if action == 'kick':
                await member.kick(reason=f"Automatic: Reached {threshold} warnings")
                action_text = "gently escorted out"
                emoji = "🚪"
            elif action == 'ban':
                await member.ban(reason=f"Automatic: Reached {threshold} warnings", delete_message_days=1)
                action_text = "sent to the timeout corner"
                emoji = "🏠"
            elif action == 'mute':
                await self._mute_user(guild, member, 60, f"Automatic: Reached {threshold} warnings")
                action_text = "given quiet time"
                emoji = "🤫"
            else:
                return  # Unknown action
            
            # Find a general channel to announce
            channel = guild.system_channel or (guild.text_channels[0] if guild.text_channels else None)
            if channel:
                embed = discord.Embed(
                    title=f"🐱 Automod Action Taken {emoji}",
                    description=f"**Member:** {member.mention}\n**Action:** {action_text.title()}\n**Reason:** Reached {threshold} reminders\n\nMeow! Sometimes I need to take automatic action to keep everyone safe! 🐾⚡",
                    color=discord.Color.from_rgb(255, 182, 193),
                    timestamp=datetime.now()
                )
                # Cute kitten thumbnail would go here
                await channel.send(embed=embed)
            
            self._log_action(f"AUTO_{action.upper()}", None, member, f"Automatic {action} for {threshold} warnings")
            
        except discord.Forbidden:
            pass  # Bot doesn't have permissions
    
    def _log_action(self, action, moderator, target, reason):
        """Log moderation actions"""
        log_entry = {
            'action': action,
            'moderator': moderator.id if moderator else None,
            'target': target.id if target else None,
            'reason': reason,
            'timestamp': datetime.now().isoformat()
        }
        
        self.mod_logs.append(log_entry)
        
        # Keep only last 1000 logs to prevent memory issues
        if len(self.mod_logs) > 1000:
            self.mod_logs = self.mod_logs[-1000:]

async def setup(bot):
    await bot.add_cog(ModerationCog(bot))
