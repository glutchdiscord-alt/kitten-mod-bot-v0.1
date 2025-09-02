#!/usr/bin/env python3
"""
Production startup script for Render deployment
"""

import os
import sys
import asyncio
from main import main

if __name__ == '__main__':
    # Ensure Discord token is available
    if not os.getenv('DISCORD_TOKEN'):
        print("ERROR: DISCORD_TOKEN environment variable is required!")
        sys.exit(1)
    
    # Run the bot
    asyncio.run(main())