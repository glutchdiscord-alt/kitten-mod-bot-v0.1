import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime, timedelta
import re
from typing import Optional

class UtilityCog(commands.Cog):
    """Utility commands for Kitten Mod"""
    
    def __init__(self, bot):
        self.bot = bot
        self.reminders = {}  # Store active reminders
        self.polls = {}  # Store active polls
        
        # 8ball responses
        self.eightball_responses = [
            "🐱 Meow! Absolutely yes! I'm purrfectly sure!",
            "🐾 Definitely! My kitten instincts say so!",
            "✨ Yes! The universe and I both agree!",
            "😸 Of course! Why would you even doubt it?",
            "💕 Yes, and I'm purring with excitement about it!",
            "🤔 Hmm... maybe? My whiskers are twitching uncertainly...",
            "😿 I don't think so... sorry to disappoint!",
            "🙈 Meow no! My kitten senses say absolutely not!",
            "😾 Definitely not! I'm hissing at that idea!",
            "💤 Ask me later... I'm too sleepy to decide right meow...",
            "🎲 The answer is unclear... like when I knock things off tables!",
            "🐾 My paws are crossed - it could go either way!",
            "✨ The stars and my favorite sunbeam say... maybe!",
            "😺 Yes, but only if you give me treats first!",
            "🥛 As likely as me refusing a bowl of milk!"
        ]
        
        # Compliment lists
        self.compliments = [
            "You're pawsitively amazing! 🐾",
            "You make the world a better place, just like catnip makes everything better! 🌿",
            "You're more wonderful than a warm sunbeam! ☀️",
            "You're absolutely purrfect just the way you are! 😸",
            "You bring joy wherever you go, like a playful kitten! 🐱",
            "You're incredibly thoughtful and kind! 💕",
            "You're stronger than you know, like a fierce lion! 🦁",
            "You're as beautiful as a graceful cat stretching in the morning! ✨",
            "You're incredibly talented and smart! 🧠",
            "You're more precious than my favorite toy mouse! 🐭",
            "You have a heart as warm as a purring kitten! 💖",
            "You're uniquely wonderful, one in a meow-illion! 🌟",
            "You're as comforting as a cat's purr on a sad day! 😊",
            "You light up rooms like cats knock things off tables - effortlessly! 💡",
            "You're absolutely fantastic, no kitten around! 🎉"
        ]
    
    @commands.command(name='remind')
    async def set_reminder(self, ctx, time_str: str, *, message: str):
        """Set a cute reminder (e.g., !remind 10m Feed the cats)"""
        
        # Parse time string
        time_match = re.match(r'^(\d+)([smhd])$', time_str.lower())
        if not time_match:
            embed = discord.Embed(
                title="🐱 Invalid Time Format",
                description="Meow! Use formats like: `10m`, `2h`, `1d` (minutes, hours, days) 🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        amount, unit = int(time_match.group(1)), time_match.group(2)
        
        # Convert to seconds
        seconds = amount  # Default to amount as seconds
        if unit == 's':
            seconds = amount
        elif unit == 'm':
            seconds = amount * 60
        elif unit == 'h':
            seconds = amount * 3600
        elif unit == 'd':
            seconds = amount * 86400
        
        # Check reasonable limits
        if seconds < 10:  # Minimum 10 seconds
            embed = discord.Embed(
                title="🐱 Too Quick!",
                description="Meow! Please set reminders for at least 10 seconds! 🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        if seconds > 7776000:  # Maximum 90 days
            embed = discord.Embed(
                title="🐱 Too Long!",
                description="Meow! I can only remember things for up to 90 days! 🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        # Set reminder
        reminder_time = datetime.now() + timedelta(seconds=seconds)
        reminder_id = f"{ctx.author.id}_{len(self.reminders)}"
        
        self.reminders[reminder_id] = {
            'user_id': ctx.author.id,
            'channel_id': ctx.channel.id,
            'message': message,
            'time': reminder_time
        }
        
        embed = discord.Embed(
            title="🐱 Reminder Set!",
            description=f"Meow! I'll remind you about: **{message}**\n\nI'll send you a message in {time_str}! 🐾⏰",
            color=discord.Color.from_rgb(144, 238, 144),
            timestamp=reminder_time
        )
        # Cute kitten thumbnail would go here
        
        await ctx.send(embed=embed)
        
        # Schedule the reminder
        asyncio.create_task(self._send_reminder(reminder_id, seconds))
    
    async def _send_reminder(self, reminder_id, delay_seconds):
        """Send the reminder after the specified delay"""
        await asyncio.sleep(delay_seconds)
        
        if reminder_id not in self.reminders:
            return  # Reminder was cancelled
        
        reminder = self.reminders[reminder_id]
        channel = self.bot.get_channel(reminder['channel_id'])
        user = self.bot.get_user(reminder['user_id'])
        
        if channel and user:
            embed = discord.Embed(
                title="🐱 Reminder Alert!",
                description=f"Meow! You asked me to remind you about:\n\n**{reminder['message']}**\n\nHope this helps! 🐾💕",
                color=discord.Color.from_rgb(255, 192, 203),
                timestamp=datetime.now()
            )
            # Cute kitten thumbnail would go here
            
            try:
                await channel.send(f"{user.mention}", embed=embed)
            except discord.Forbidden:
                pass  # Can't send message
        
        # Clean up
        del self.reminders[reminder_id]
    
    @commands.command(name='poll')
    async def create_poll(self, ctx, *, question: str):
        """Create a poll with cute kitten reactions"""
        
        if len(question) > 200:
            embed = discord.Embed(
                title="🐱 Question Too Long",
                description="Meow! Please keep your poll question under 200 characters! 🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        embed = discord.Embed(
            title="🐱 Kitten Poll!",
            description=f"**{question}**\n\nReact with 👍 for yes or 👎 for no!\nResults will be shown in 60 seconds! 🐾",
            color=discord.Color.from_rgb(255, 192, 203),
            timestamp=datetime.now()
        )
        
        embed.add_field(
            name="📊 How to Vote:",
            value="👍 = Yes/Agree\n👎 = No/Disagree",
            inline=True
        )
        
        embed.add_field(
            name="⏰ Duration:",
            value="60 seconds",
            inline=True
        )
        
        embed.set_footer(text=f"Poll by {ctx.author.display_name}")
        # Cute kitten thumbnail would go here
        
        poll_msg = await ctx.send(embed=embed)
        await poll_msg.add_reaction("👍")
        await poll_msg.add_reaction("👎")
        
        # Store poll data
        self.polls[poll_msg.id] = {
            'question': question,
            'author': ctx.author,
            'channel': ctx.channel
        }
        
        # Wait and show results
        await asyncio.sleep(60)
        await self._show_poll_results(poll_msg)
    
    async def _show_poll_results(self, poll_msg):
        """Show poll results after voting period"""
        try:
            # Refresh message to get current reactions
            poll_msg = await poll_msg.channel.fetch_message(poll_msg.id)
            
            yes_votes = 0
            no_votes = 0
            
            for reaction in poll_msg.reactions:
                if str(reaction.emoji) == "👍":
                    yes_votes = reaction.count - 1  # Subtract bot's reaction
                elif str(reaction.emoji) == "👎":
                    no_votes = reaction.count - 1  # Subtract bot's reaction
            
            total_votes = yes_votes + no_votes
            
            if total_votes == 0:
                result_text = "No one voted... *sad kitten noises* 😿"
                color = discord.Color.from_rgb(255, 182, 193)
            else:
                yes_percent = (yes_votes / total_votes) * 100
                no_percent = (no_votes / total_votes) * 100
                
                if yes_votes > no_votes:
                    result_text = f"**Yes wins!** 🎉\n👍 Yes: {yes_votes} votes ({yes_percent:.1f}%)\n👎 No: {no_votes} votes ({no_percent:.1f}%)"
                    color = discord.Color.from_rgb(144, 238, 144)
                elif no_votes > yes_votes:
                    result_text = f"**No wins!** 📊\n👎 No: {no_votes} votes ({no_percent:.1f}%)\n👍 Yes: {yes_votes} votes ({yes_percent:.1f}%)"
                    color = discord.Color.from_rgb(255, 182, 193)
                else:
                    result_text = f"**It's a tie!** 🤝\n👍 Yes: {yes_votes} votes (50%)\n👎 No: {no_votes} votes (50%)"
                    color = discord.Color.from_rgb(255, 192, 203)
            
            poll_data = self.polls.get(poll_msg.id)
            if poll_data:
                embed = discord.Embed(
                    title="🐱 Poll Results!",
                    description=f"**Question:** {poll_data['question']}\n\n{result_text}\n\nMeow! Thanks everyone for voting! 🐾",
                    color=color,
                    timestamp=datetime.now()
                )
                embed.set_footer(text=f"Poll by {poll_data['author'].display_name}")
                # Cute kitten thumbnail would go here
                
                await poll_data['channel'].send(embed=embed)
                del self.polls[poll_msg.id]
                
        except discord.NotFound:
            # Message was deleted
            if poll_msg.id in self.polls:
                del self.polls[poll_msg.id]
        except Exception:
            pass  # Other error, just clean up
    
    @commands.command(name='8ball')
    async def magic_8ball(self, ctx, *, question: str):
        """Ask the magic 8-ball a question and get a cute kitten response"""
        
        if len(question) > 200:
            embed = discord.Embed(
                title="🐱 Question Too Long",
                description="Meow! Please keep your question under 200 characters! 🐾",
                color=discord.Color.from_rgb(255, 182, 193)
            )
            # Cute kitten thumbnail would go here
            await ctx.send(embed=embed)
            return
        
        # Add dramatic pause
        thinking_embed = discord.Embed(
            title="🔮 Magic Kitten Ball",
            description="*shakes the magic ball with tiny paws* 🐾\n\nLet me consult my kitten wisdom...",
            color=discord.Color.from_rgb(255, 192, 203)
        )
        # Cute kitten thumbnail would go here
        
        msg = await ctx.send(embed=thinking_embed)
        await asyncio.sleep(2)  # Dramatic pause
        
        response = random.choice(self.eightball_responses)
        
        embed = discord.Embed(
            title="🔮 Magic Kitten Ball Says:",
            description=f"**Your Question:** {question}\n\n**My Answer:** {response}",
            color=discord.Color.from_rgb(255, 192, 203),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Asked by {ctx.author.display_name}")
        # Cute kitten thumbnail would go here
        
        await msg.edit(embed=embed)
    
    @commands.command(name='compliment')
    async def give_compliment(self, ctx, member: Optional[discord.Member] = None):
        """Send an adorable compliment to someone (or yourself!)"""
        
        target_member = member if member is not None else ctx.author
        
        if target_member.bot and target_member != self.bot.user:
            embed = discord.Embed(
                title="🐱 Bot Compliment",
                description=f"Meow! {target_member.mention} is a helpful bot friend! We bots need to stick together! 🤖🐾",
                color=discord.Color.from_rgb(255, 192, 203)
            )
        elif target_member == self.bot.user:
            embed = discord.Embed(
                title="🐱 Aww, Thanks!",
                description="Meow! You're so sweet! I'm just doing my best to keep everyone happy and safe! *purrs* 🐾💕",
                color=discord.Color.from_rgb(255, 192, 203)
            )
        else:
            compliment = random.choice(self.compliments)
            
            embed = discord.Embed(
                title="🐱 Kitten Compliment!",
                description=f"{target_member.mention}, {compliment}",
                color=discord.Color.from_rgb(255, 192, 203),
                timestamp=datetime.now()
            )
            
            embed.add_field(
                name="💝 From:",
                value=f"Your friendly Kitten Mod (requested by {ctx.author.mention})",
                inline=False
            )
        
        # Cute kitten thumbnail would go here
        msg = await ctx.send(embed=embed)
        
        # Add heart reaction
        try:
            await msg.add_reaction("💕")
        except:
            pass

async def setup(bot):
    await bot.add_cog(UtilityCog(bot))
