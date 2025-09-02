import discord
from discord.ext import commands
import random
import asyncio
from datetime import datetime

class FunCog(commands.Cog):
    """Fun and interactive commands for Kitten Mod"""
    
    def __init__(self, bot):
        self.bot = bot
        self.is_napping = False
        self.play_sessions = {}
        
        # Cute responses for different commands
        self.pet_responses = [
            "*purrs loudly* Meow! That feels so nice! 🐾",
            "*rubs against your hand* Purr purr! More pets please! 😸",
            "*rolls over for belly rubs* Mrow! You're the best! 💕",
            "*stretches paws* Meow meow! I love pets! 🐱",
            "*closes eyes happily* Purrrrr... So relaxing! ✨"
        ]
        
        self.treat_responses = [
            "*munches happily* Nom nom! This is delicious! 🐾",
            "*purrs with mouth full* Mrow! Thank you for the yummy treat! 😋",
            "*licks lips* Meow! That was purrfect! 💕",
            "*does little happy dance* Best treat ever! 🐱",
            "*sits like a good kitty* Meow! I've been such a good moderator! ✨"
        ]
        
        self.cat_facts = [
            "Did you know? Cats spend 70% of their lives sleeping! That's 13-16 hours a day! 😴",
            "Meow fact: A group of cats is called a 'clowder'! 🐱",
            "Purrfect fact: Cats have a third eyelid called a 'nictitating membrane'! 👁️",
            "Cute fact: Cats can't taste sweetness! They're missing the gene for it! 🍯",
            "Amazing fact: A cat's purr vibrates at 25-50 Hz, which can help heal bones! 💕",
            "Fun fact: Cats have 32 muscles in each ear! No wonder they hear everything! 👂",
            "Adorable fact: When cats slow blink at you, it's like giving you a kiss! 😽"
        ]
    
    @commands.command(name='pet')
    async def pet_kitten(self, ctx):
        """Pet the adorable kitten bot!"""
        response = random.choice(self.pet_responses)
        
        embed = discord.Embed(
            title="🐱 *Getting Pets*",
            description=f"{response}\n\n*Kitten Mod happiness level: {random.randint(95, 100)}%*",
            color=discord.Color.from_rgb(255, 192, 203)
        )
        # Cute kitten thumbnail would go here
        
        # Add random cute emoji reaction
        cute_emojis = ["😸", "😺", "😻", "🐾", "💕", "✨"]
        embed.add_field(
            name="💭 Kitten's Mood:",
            value=f"Feeling loved and happy! {random.choice(cute_emojis)}",
            inline=False
        )
        
        # Send message and add reactions
        try:
            msg = await ctx.send(embed=embed)
            await msg.add_reaction("🐾")
            await msg.add_reaction("💕")
        except:
            pass
    
    @commands.command(name='treat')
    async def give_treat(self, ctx):
        """Give the kitten bot a delicious treat!"""
        response = random.choice(self.treat_responses)
        
        treats = [
            "🐟 Fishy treat",
            "🥛 Bowl of milk", 
            "🍗 Chicken bits",
            "🧀 Cheese cube",
            "🥩 Tiny steak piece"
        ]
        
        treat = random.choice(treats)
        
        embed = discord.Embed(
            title="🍽️ Treat Time!",
            description=f"You gave me: {treat}\n\n{response}",
            color=discord.Color.from_rgb(255, 220, 177)
        )
        # Cute kitten thumbnail would go here
        
        embed.add_field(
            name="🎯 Kitten's Energy:",
            value=f"Ready to moderate even better! {random.randint(90, 100)}% charged!",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name='meow')
    async def meow_command(self, ctx):
        """Get random cat facts and cute sounds!"""
        
        # Random between fact and sound
        if random.choice([True, False]):
            # Cat fact
            fact = random.choice(self.cat_facts)
            embed = discord.Embed(
                title="🐱 Kitten's Cat Fact!",
                description=fact,
                color=discord.Color.from_rgb(255, 192, 203)
            )
        else:
            # Cute sound
            sounds = [
                "Meow! 🐱",
                "Mrow mrow! 😸", 
                "Purrrrrr... 💕",
                "Mew mew! 🐾",
                "Meooooow! ✨",
                "*chirp chirp* (excited kitten sounds!) 😺",
                "Prrrp! (little trill sound!) 🎵"
            ]
            sound = random.choice(sounds)
            embed = discord.Embed(
                title="🐱 Kitten Says:",
                description=f"{sound}\n\n*{ctx.author.mention}, you made me so happy I had to make cute sounds!*",
                color=discord.Color.from_rgb(255, 192, 203)
            )
        
        # Cute kitten thumbnail would go here
        await ctx.send(embed=embed)
    
    @commands.command(name='nap')
    async def nap_time(self, ctx):
        """Put the kitten bot down for a cute nap!"""
        if self.is_napping:
            embed = discord.Embed(
                title="😴 Already Napping",
                description="Shhh... I'm already taking a cozy nap! Don't wake me up! 💤",
                color=discord.Color.from_rgb(200, 200, 255)
            )
        else:
            self.is_napping = True
            embed = discord.Embed(
                title="😴 Nap Time!",
                description="*yawns and stretches* Time for a little kitty nap... zzz... 💤\n\nI'll wake up in 2 minutes, refreshed and ready to moderate! 🐱",
                color=discord.Color.from_rgb(200, 200, 255)
            )
            
            # Wake up after 2 minutes
            asyncio.create_task(self._wake_up_after_nap(ctx))
        
        # Cute kitten thumbnail would go here
        await ctx.send(embed=embed)
    
    async def _wake_up_after_nap(self, ctx):
        """Wake up the kitten after nap time"""
        await asyncio.sleep(120)  # 2 minutes
        self.is_napping = False
        
        embed = discord.Embed(
            title="😸 Kitten Woke Up!",
            description="*stretches and yawns* Meow! That was a purrfect nap! I'm ready to keep everyone safe and happy again! 🐾✨",
            color=discord.Color.from_rgb(255, 192, 203)
        )
        # Cute kitten thumbnail would go here
        
        try:
            await ctx.send(embed=embed)
        except:
            pass  # Channel might be deleted or bot lacks permissions
    
    @commands.command(name='playtime')
    async def play_time(self, ctx):
        """Start a fun playtime activity with the kitten!"""
        
        games = [
            {
                "name": "🧶 Yarn Ball Chase",
                "description": "I'm chasing a yarn ball around! React with 🐾 to help me catch it!",
                "emoji": "🐾",
                "success": "Caught it! Thanks for playing! *purrs happily* 💕"
            },
            {
                "name": "🐭 Mouse Hunt",
                "description": "There's a toy mouse hiding! React with 🐭 to help me find it!",
                "emoji": "🐭", 
                "success": "Found the mouse! Great teamwork! *does victory dance* 🎉"
            },
            {
                "name": "📦 Box Adventure",
                "description": "I found an empty box! React with 📦 to join me inside!",
                "emoji": "📦",
                "success": "This box is perfect! Room for both of us! *settles in cozily* 😸"
            }
        ]
        
        game = random.choice(games)
        
        embed = discord.Embed(
            title=f"🎮 {game['name']}",
            description=game['description'],
            color=discord.Color.from_rgb(255, 192, 203)
        )
        embed.add_field(
            name="🎯 How to Play:",
            value=f"React with {game['emoji']} within 30 seconds to play with me!",
            inline=False
        )
        # Cute kitten thumbnail would go here
        
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(game['emoji'])
        
        # Start the game session
        self.play_sessions[msg.id] = {
            'game': game,
            'players': set(),
            'channel': ctx.channel
        }
        
        # Wait for reactions
        await asyncio.sleep(30)
        
        # Check results
        if msg.id in self.play_sessions:
            session = self.play_sessions[msg.id]
            if session['players']:
                result_embed = discord.Embed(
                    title="🎉 Playtime Success!",
                    description=f"{game['success']}\n\nThanks to: {', '.join([f'<@{uid}>' for uid in session['players']])}",
                    color=discord.Color.from_rgb(144, 238, 144)
                )
            else:
                result_embed = discord.Embed(
                    title="😿 No Playmates",
                    description="No one wanted to play... Maybe next time! *sits sadly but still cute*",
                    color=discord.Color.from_rgb(255, 182, 193)
                )
            
            # Cute kitten thumbnail would go here
            await session['channel'].send(embed=result_embed)
            del self.play_sessions[msg.id]
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        """Handle playtime reactions"""
        if user.bot:
            return
        
        msg_id = reaction.message.id
        if msg_id in self.play_sessions:
            session = self.play_sessions[msg_id]
            if str(reaction.emoji) == session['game']['emoji']:
                session['players'].add(user.id)

async def setup(bot):
    await bot.add_cog(FunCog(bot))