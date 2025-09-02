"""
Logging utilities for the Discord moderation bot
"""

import logging
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

# Configure logging format
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

def setup_logging(level=logging.INFO):
    """Setup logging configuration"""
    
    # Create logger
    logger = logging.getLogger('discord_modbot')
    logger.setLevel(level)
    
    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    
    # Set discord.py logging level to WARNING to reduce noise
    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.WARNING)
    
    return logger

def get_logger(name):
    """Get a logger instance for a specific module"""
    return logging.getLogger(f'discord_modbot.{name}')

class ModLogManager:
    """Manage moderation logs in memory"""
    
    def __init__(self, max_entries=1000):
        self.logs: List[Dict[str, Any]] = []
        self.max_entries = max_entries
        self.logger = get_logger('modlogs')
    
    def add_log(self, action: str, moderator_id: int, target_id: Optional[int] = None, 
                reason: Optional[str] = None, guild_id: Optional[int] = None, **kwargs):
        """Add a moderation log entry"""
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action': action.upper(),
            'moderator_id': moderator_id,
            'target_id': target_id,
            'reason': reason,
            'guild_id': guild_id,
            **kwargs
        }
        
        self.logs.append(log_entry)
        
        # Keep only the last max_entries logs
        if len(self.logs) > self.max_entries:
            self.logs = self.logs[-self.max_entries:]
        
        # Log to console
        self.logger.info(f"Action: {action} | Moderator: {moderator_id} | Target: {target_id} | Reason: {reason}")
    
    def get_logs(self, limit: int = 50, guild_id: Optional[int] = None, 
                 action: Optional[str] = None, moderator_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get filtered logs"""
        
        filtered_logs = self.logs
        
        # Filter by guild
        if guild_id:
            filtered_logs = [log for log in filtered_logs if log.get('guild_id') == guild_id]
        
        # Filter by action
        if action:
            filtered_logs = [log for log in filtered_logs if log.get('action') == action.upper()]
        
        # Filter by moderator
        if moderator_id:
            filtered_logs = [log for log in filtered_logs if log.get('moderator_id') == moderator_id]
        
        # Return latest logs first
        return filtered_logs[-limit:][::-1]
    
    def get_user_logs(self, user_id: int, guild_id: Optional[int] = None) -> List[Dict[str, Any]]:
        """Get logs for a specific user (as target)"""
        
        filtered_logs = [log for log in self.logs if log.get('target_id') == user_id]
        
        if guild_id:
            filtered_logs = [log for log in filtered_logs if log.get('guild_id') == guild_id]
        
        return filtered_logs[::-1]  # Return latest first
    
    def clear_logs(self, older_than_days: Optional[int] = None):
        """Clear old logs"""
        
        if older_than_days:
            cutoff_date = datetime.now() - timedelta(days=older_than_days)
            self.logs = [
                log for log in self.logs 
                if datetime.fromisoformat(log['timestamp']) > cutoff_date
            ]
        else:
            self.logs.clear()
        
        self.logger.info(f"Cleared logs older than {older_than_days} days" if older_than_days else "Cleared all logs")

class ActionLogger:
    """Context manager for logging moderation actions"""
    
    def __init__(self, action: str, moderator_id: int, target_id: Optional[int] = None, 
                 reason: Optional[str] = None, guild_id: Optional[int] = None):
        self.action = action
        self.moderator_id = moderator_id
        self.target_id = target_id
        self.reason = reason
        self.guild_id = guild_id
        self.logger = get_logger('actions')
        self.start_time: Optional[datetime] = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"Starting action: {self.action}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time is None:
            return
        duration = datetime.now() - self.start_time
        
        if exc_type is None:
            self.logger.info(f"Completed action: {self.action} (took {duration.total_seconds():.2f}s)")
        else:
            self.logger.error(f"Failed action: {self.action} - {exc_val}")

# Global mod log manager instance
mod_log_manager = ModLogManager()

def log_moderation_action(action: str, moderator_id: int, target_id: Optional[int] = None, 
                         reason: Optional[str] = None, guild_id: Optional[int] = None, **kwargs):
    """Convenience function to log moderation actions"""
    mod_log_manager.add_log(action, moderator_id, target_id, reason, guild_id, **kwargs)
