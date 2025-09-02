import discord
from discord.ext import commands
import os
import asyncio
from config import BOT_CONFIG
from utils.logging import setup_logging
from aiohttp import web

# Setup logging
logger = setup_logging()

# Global variables
guild_prefixes = {}
processed_commands = set()

# Dynamic prefix function
def get_prefix(bot, message):
    """Get the prefix for the current guild"""
    if message.guild is None:
        return BOT_CONFIG['prefix']
    return guild_prefixes.get(message.guild.id, BOT_CONFIG['prefix'])

# Bot setup with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

# Create bot instance
bot = commands.Bot(
    command_prefix=get_prefix,
    intents=intents,
    help_command=None,
    case_insensitive=True
)

@bot.before_invoke
async def before_any_command(ctx):
    """Prevent duplicate command execution"""
    command_key = f"{ctx.message.id}_{ctx.command.name}_{ctx.author.id}"
    
    if command_key in processed_commands:
        raise commands.CommandError("Duplicate command prevented")
    
    processed_commands.add(command_key)
    
    # Clean old entries to prevent memory issues
    if len(processed_commands) > 1000:
        old_entries = list(processed_commands)[:500]
        for entry in old_entries:
            processed_commands.discard(entry)

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
        return
    
    # Prevent duplicate error handling
    if hasattr(ctx, '_error_handled'):
        return
    ctx._error_handled = True
    
    # Skip our duplicate prevention errors
    if isinstance(error, commands.CommandError) and "Duplicate command prevented" in str(error):
        return
    
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="🐱 Meow! No Permission",
            description="Sorry, but you don't have the right permissions to use this command! Only moderators can help me keep things purrfect.",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="🐱 Oops! Missing Something",
            description=f"Meow! I need more information. You forgot to tell me: `{error.param}`",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        await ctx.send(embed=embed)
    
    elif isinstance(error, commands.BadArgument):
        embed = discord.Embed(
            title="🐱 That Doesn't Look Right",
            description="Meow! Something you typed doesn't look quite right. Could you check what you entered?",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        await ctx.send(embed=embed)
    
    else:
        logger.error(f"Unexpected error: {error}")
        embed = discord.Embed(
            title="🐱 Kitty Confusion",
            description="Meow! Something unexpected happened and I got a bit confused. Could you try that again?",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        await ctx.send(embed=embed)

@bot.command(name='help')
async def help_command(ctx):
    """Display help information"""
    embed = discord.Embed(
        title="🐱 Kitten Mod Help - Purrfect Moderation!",
        description="Meow! Here are all my cute commands to keep your server safe and cozy! 🐾",
        color=discord.Color.from_rgb(255, 192, 203)
    )
    
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
        name="⚙️ Bot Settings",
        value=f"`{BOT_CONFIG['prefix']}prefix` - Show current prefix\n"
              f"`{BOT_CONFIG['prefix']}prefix <new>` - Change bot prefix 🔧",
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

@bot.command(name='prefix')
@commands.has_permissions(administrator=True)
async def change_prefix(ctx, *, new_prefix = None):
    """Change the bot's command prefix for this server"""
    global guild_prefixes
    
    if new_prefix is None:
        # Show current prefix
        current_prefix = guild_prefixes.get(ctx.guild.id, BOT_CONFIG['prefix'])
        embed = discord.Embed(
            title="🐱 Current Prefix",
            description=f"Meow! My current prefix in this server is: **{current_prefix}**\n\nTo change it, use: `{current_prefix}prefix <new_prefix>` 🐾",
            color=discord.Color.from_rgb(255, 192, 203)
        )
        await ctx.send(embed=embed)
        return
    
    # Validate new prefix
    if len(new_prefix) > 5:
        embed = discord.Embed(
            title="🐱 Prefix Too Long",
            description="Meow! Please use a prefix that's 5 characters or shorter! 🐾",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        await ctx.send(embed=embed)
        return
    
    if any(char in new_prefix for char in [' ', '\n', '\t']):
        embed = discord.Embed(
            title="🐱 Invalid Characters",
            description="Meow! Prefixes can't contain spaces or special whitespace characters! 🐾",
            color=discord.Color.from_rgb(255, 182, 193)
        )
        await ctx.send(embed=embed)
        return
    
    # Store the new prefix for this guild
    old_prefix = guild_prefixes.get(ctx.guild.id, BOT_CONFIG['prefix'])
    guild_prefixes[ctx.guild.id] = new_prefix
    
    embed = discord.Embed(
        title="🐱 Prefix Changed!",
        description=f"Meow! I've changed my prefix from **{old_prefix}** to **{new_prefix}**!\n\nNow use commands like: `{new_prefix}help` 🐾✨",
        color=discord.Color.from_rgb(144, 238, 144)
    )
    await ctx.send(embed=embed)

async def load_cogs():
    """Load all cog files with proper cleanup"""
    # Clear all existing extensions first
    extensions_to_remove = list(bot.extensions.keys())
    for extension in extensions_to_remove:
        try:
            await bot.unload_extension(extension)
            logger.info(f"Unloaded {extension}")
        except Exception as e:
            logger.error(f"Failed to unload {extension}: {e}")
    
    # Load fresh cogs
    cogs = ['cogs.moderation', 'cogs.fun', 'cogs.advanced_mod', 'cogs.welcome', 'cogs.utility']
    for cog in cogs:
        try:
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
