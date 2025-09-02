"""
Permission utilities for the Discord moderation bot
"""

import discord
from discord.ext import commands
from functools import wraps

def has_mod_permissions():
    """Decorator to check if user has moderation permissions"""
    def predicate(ctx):
        # Bot owner always has permissions
        if ctx.author.id == ctx.bot.owner_id:
            return True
        
        # Check if user has administrator permission
        if ctx.author.guild_permissions.administrator:
            return True
        
        # Check for specific moderation permissions
        perms = ctx.author.guild_permissions
        return (perms.kick_members or perms.ban_members or 
                perms.manage_messages or perms.manage_roles)
    
    return commands.check(predicate)

def can_moderate_member(moderator, target):
    """Check if moderator can moderate the target member"""
    # Bot owner can moderate anyone
    if moderator.guild.owner_id == moderator.id:
        return True
    
    # Cannot moderate someone with higher or equal role
    if target.top_role >= moderator.top_role:
        return False
    
    # Cannot moderate bot itself
    if target.bot:
        return False
    
    return True

def has_higher_role(member1, member2):
    """Check if member1 has a higher role than member2"""
    return member1.top_role > member2.top_role

class PermissionLevel:
    """Permission level constants"""
    MEMBER = 0
    MODERATOR = 1
    ADMIN = 2
    OWNER = 3

def get_permission_level(member):
    """Get the permission level of a member"""
    if member.guild.owner_id == member.id:
        return PermissionLevel.OWNER
    
    perms = member.guild_permissions
    
    if perms.administrator:
        return PermissionLevel.ADMIN
    
    if (perms.kick_members or perms.ban_members or 
        perms.manage_messages or perms.manage_roles):
        return PermissionLevel.MODERATOR
    
    return PermissionLevel.MEMBER

def require_permission_level(required_level):
    """Decorator to require a minimum permission level"""
    def decorator(func):
        @wraps(func)
        async def wrapper(ctx, *args, **kwargs):
            user_level = get_permission_level(ctx.author)
            if user_level < required_level:
                embed = discord.Embed(
                    title="❌ Insufficient Permissions",
                    description="You don't have the required permission level for this command.",
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            return await func(ctx, *args, **kwargs)
        return wrapper
    return decorator

def is_mod_channel(channel):
    """Check if a channel is designated for moderation"""
    # This can be customized based on channel names or categories
    mod_channel_names = ['mod', 'moderation', 'admin', 'staff']
    
    if any(name in channel.name.lower() for name in mod_channel_names):
        return True
    
    # Check if channel is in a moderation category
    if channel.category:
        if any(name in channel.category.name.lower() for name in mod_channel_names):
            return True
    
    return False

async def check_bot_permissions(guild, required_perms):
    """Check if bot has required permissions in guild"""
    bot_member = guild.me
    bot_perms = bot_member.guild_permissions
    
    missing_perms = []
    
    for perm_name in required_perms:
        if not getattr(bot_perms, perm_name, False):
            missing_perms.append(perm_name)
    
    return missing_perms

def format_permissions(permissions):
    """Format permission list for display"""
    perm_names = {
        'kick_members': 'Kick Members',
        'ban_members': 'Ban Members',
        'manage_messages': 'Manage Messages',
        'manage_roles': 'Manage Roles',
        'manage_channels': 'Manage Channels',
        'administrator': 'Administrator',
        'manage_guild': 'Manage Server'
    }
    
    return [perm_names.get(perm, perm.replace('_', ' ').title()) for perm in permissions]
