"""
Configuration file for Discord moderation bot
"""

BOT_CONFIG = {
    # Bot command prefix
    'prefix': '!',
    
    # Bot settings
    'description': 'Kitten Mod - Your adorable Discord moderation assistant! Keeping servers purrfect with cute commands! 🐱💕',
    
    # Moderation settings
    'max_warnings': 5,  # Maximum warnings before automatic action
    'default_mute_duration': 10,  # Default mute duration in minutes
    'spam_threshold': 5,  # Messages per 10 seconds considered spam
    
    # Logging settings
    'log_level': 'INFO',
    'max_log_entries': 5000,  # Increased for production
    'enable_debug': False,  # Disable debug mode in production
    
    # Permission roles (these are Discord permission names, not role names)
    'required_permissions': {
        'kick': 'kick_members',
        'ban': 'ban_members',
        'mute': 'manage_roles',
        'warn': 'manage_messages',
        'clear': 'manage_messages'
    }
}

# Cute kitten message responses
MESSAGES = {
    'no_permission': "🐱 Meow! You don't have permission to use this command.",
    'user_not_found': "🐱 Kitty can't find that user.",
    'bot_no_permission': "🐱 Meow! I don't have permission to do that.",
    'cannot_moderate_higher': "🐱 Oopsie! I can't moderate someone with a higher rank.",
    'action_successful': "🐾 Purrfect! Action completed successfully.",
    'dm_failed': "🐱 Could not send a private meow to the user."
}

# Naughty words that make kitten sad (content filtering)
CONTENT_FILTER = {
    'banned_words': [
        'spam', 'scam', 'hack', 'cheat', 'bot', 'free nitro',
        'discord.gg/', 'bit.ly/', 'tinyurl.com'
    ],
    'allow_links': False,  # Set to True to allow all links
    'link_whitelist': [
        'discord.com', 'github.com', 'youtube.com', 'youtu.be'
    ]
}
