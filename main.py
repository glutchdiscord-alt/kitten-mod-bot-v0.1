import discord
from discord.ext import commands
import os
import asyncio
from config import BOT_CONFIG
from utils.logging import setup_logging
from aiohttp import web

# Setup logging
logger = setup_logging()

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(
    command_prefix=BOT_CONFIG['prefix'],
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    """Event triggered when bot is ready"""
    logger.info(f'{bot.user} has connected to Discord!')
    logger.info(f'Bot is in {len(bot.guilds)} guilds')
    
    # Set bot status
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name=f"{BOT_CONFIG['prefix']}help | Keeping servers purrfect! 🐱"
    )
    await bot.change_presence(activity=activity)

@bot.event
async def on_command_error(ctx, error):
    """Global error handler"""
    if isinstance(error, commands.CommandNotFound):
        return  # Ignore command not found errors
    
    # Check if error has already been handled
    if hasattr(ctx, '_error_handled'):
        return
    ctx._error_handled = True
    
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="🐱 Meow! No Permission",
            description="Sorry, but you don't have the right permissions to use this command! Only moderators can help me keep things purrfect.",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        # Cute kitten thumbnail would go here
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="🐱 Oops! Missing Something",
            description=f"Meow! I need more information. You forgot to tell me: `{error.param}`",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        # Cute kitten thumbnail would go here
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            title="🐱 That Doesn't Look Right",
            description="Meow! Something you typed doesn't look quite right. Could you check what you entered?",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        # Cute kitten thumbnail would go here
        await ctx.send(embed=embed)
    
    else:
        logger.error(f"Unexpected error: {error}")
        embed = discord.Embed(
            title="🐱 Kitty Confusion",
            description="Meow! Something unexpected happened and I got a bit confused. Could you try that again?",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        # Cute kitten thumbnail would go here
        await ctx.send(embed=embed)

@bot.command(name='help')
async def help_command(ctx):
    """Display help information"""
    embed = discord.Embed(
        title="🐱 Kitten Mod Help - Purrfect Moderation!",
        description="Meow! Here are all my cute commands to keep your server safe and cozy! 🐾",
        color=discord.Color.from_rgb(255, 192, 203)
    )
    embed.set_thumbnail(url="attachment://IMG_0229_1756759800418.jpeg")
    
    embed.add_field(
        name="🐾 Kitten's Moderation Powers",
        value=f"`{BOT_CONFIG['prefix']}kick <user> [reason]` - Gently escort someone out 🚪\n"
              f"`{BOT_CONFIG['prefix']}ban <user> [reason]` - Send someone to the timeout corner 🏠\n"
              f"`{BOT_CONFIG['prefix']}unban <user_id>` - Welcome someone back home 💕\n"
              f"`{BOT_CONFIG['prefix']}mute <user> [duration] [reason]` - Give someone quiet time 🤫\n"
              f"`{BOT_CONFIG['prefix']}unmute <user>` - Let someone speak again 🗣️\n"
              f"`{BOT_CONFIG['prefix']}warn <user> <reason>` - Give a gentle reminder 📝\n"
              f"`{BOT_CONFIG['prefix']}removewarn <user> <id>` - Remove a reminder ✨\n"
              f"`{BOT_CONFIG['prefix']}automod <warnings> <action>` - Set auto-actions ⚡",
        inline=False
    )
    
    embed.add_field(
        name="⚡ Advanced Moderation",
        value=f"`{BOT_CONFIG['prefix']}slowmode <seconds>` - Set chat slowmode ⏰\n"
              f"`{BOT_CONFIG['prefix']}lockdown [minutes]` - Lock channel temporarily 🔒\n"
              f"`{BOT_CONFIG['prefix']}unlock` - Unlock locked channel 🔓\n"
              f"`{BOT_CONFIG['prefix']}nickname <user> <name>` - Change nicknames 🏷️\n"
              f"`{BOT_CONFIG['prefix']}role <user> <role>` - Add/remove roles 👥",
        inline=False
    )
    
    embed.add_field(
        name="🎮 Fun & Interactive",
        value=f"`{BOT_CONFIG['prefix']}pet` - Pet the adorable kitten! 🐾\n"
              f"`{BOT_CONFIG['prefix']}treat` - Give the kitten a yummy treat 🍽️\n"
              f"`{BOT_CONFIG['prefix']}meow` - Get cat facts and cute sounds 😸\n"
              f"`{BOT_CONFIG['prefix']}nap` - Put the kitten down for a nap 😴\n"
              f"`{BOT_CONFIG['prefix']}playtime` - Start fun activities! 🎯",
        inline=False
    )
    
    embed.add_field(
        name="📋 Info & Utilities",
        value=f"`{BOT_CONFIG['prefix']}warnings <user>` - Check reminder history 📚\n"
              f"`{BOT_CONFIG['prefix']}clear <amount>` - Clean up messages 🧹\n"
              f"`{BOT_CONFIG['prefix']}userinfo <user>` - Learn about someone 👤\n"
              f"`{BOT_CONFIG['prefix']}remind <time> <msg>` - Set cute reminders ⏰\n"
              f"`{BOT_CONFIG['prefix']}poll <question>` - Create polls 📊",
        inline=False
    )
    
    embed.add_field(
        name="🎊 Welcome System",
        value=f"`{BOT_CONFIG['prefix']}welcome setup` - Configure welcomes 🎉\n"
              f"`{BOT_CONFIG['prefix']}goodbye setup` - Configure goodbyes 👋\n"
              f"`{BOT_CONFIG['prefix']}autorole set <role>` - Auto-assign roles 🏷️",
        inline=False
    )
    
    embed.add_field(
        name="✨ Extra Fun",
        value=f"`{BOT_CONFIG['prefix']}8ball <question>` - Ask the magic kitten 🔮\n"
              f"`{BOT_CONFIG['prefix']}compliment [user]` - Send sweet words 💕",
        inline=False
    )
    
    embed.add_field(
        name="💝 Kitty Note",
        value="Meow! Only moderators with the right permissions can use moderation powers. Everyone can enjoy the fun commands! I'm here to help keep everyone safe and happy! 🐱💕",
        inline=False
    )
    
    await ctx.send(embed=embed)

async def load_cogs():
    """Load all cog files"""
    cogs = ['cogs.moderation', 'cogs.fun', 'cogs.advanced_mod', 'cogs.welcome', 'cogs.utility']
    for cog in cogs:
        try:
            # Unload if already loaded to prevent duplicates
            if cog in bot.extensions:
                await bot.unload_extension(cog)
            await bot.load_extension(cog)
            logger.info(f"Loaded {cog}")
        except Exception as e:
            logger.error(f"Failed to load {cog}: {e}")

async def health_check(request):
    """Health check endpoint for Render"""
    return web.json_response({"status": "healthy", "bot": bot.user.name if bot.user else "Starting..."})

async def main():
    """Main function to start the bot"""
    async with bot:
        await load_cogs()
        
        # Get token from environment variable
        token = os.getenv('DISCORD_TOKEN')
        if not token:
            logger.error("DISCORD_TOKEN environment variable not found!")
            return
        
        # Start health check server for Render
        app = web.Application()
        app.router.add_get('/health', health_check)
        
        # Start web server in background
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', int(os.getenv('PORT', 10000)))
        await site.start()
        
        logger.info("Health check server started on port 10000")
        
        # Start the bot
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
