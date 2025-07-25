"""Database utilities for storing bot data"""

import sqlite3
import asyncio
import aiosqlite
from datetime import datetime
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = "xsportbs.db"):
        self.db_path = db_path
    
    async def init_tables(self):
        """Initialize all database tables"""
        async with aiosqlite.connect(self.db_path) as db:
            # Guild settings table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS guild_settings (
                    guild_id INTEGER PRIMARY KEY,
                    log_channel_id INTEGER,
                    language TEXT DEFAULT 'en',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Channel visibility settings
            await db.execute("""
                CREATE TABLE IF NOT EXISTS channel_visibility (
                    guild_id INTEGER,
                    channel_id INTEGER,
                    visible BOOLEAN DEFAULT TRUE,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (guild_id, channel_id)
                )
            """)
            
            # Match history
            await db.execute("""
                CREATE TABLE IF NOT EXISTS matches (
                    match_id INTEGER PRIMARY KEY,
                    guild_id INTEGER,
                    title TEXT,
                    teams TEXT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    role_id INTEGER,
                    creator_id INTEGER,
                    language TEXT DEFAULT 'en',
                    image_url TEXT,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Command usage logs
            await db.execute("""
                CREATE TABLE IF NOT EXISTS command_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    command_name TEXT,
                    guild_id INTEGER,
                    user_id INTEGER,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Bot event logs
            await db.execute("""
                CREATE TABLE IF NOT EXISTS event_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT,
                    guild_id INTEGER,
                    description TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            await db.commit()
    
    async def set_log_channel(self, guild_id: int, channel_id: int):
        """Set the log channel for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO guild_settings (guild_id, log_channel_id)
                VALUES (?, ?)
            """, (guild_id, channel_id))
            await db.commit()
    
    async def get_log_channel(self, guild_id: int) -> Optional[int]:
        """Get the log channel for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT log_channel_id FROM guild_settings WHERE guild_id = ?
            """, (guild_id,))
            result = await cursor.fetchone()
            return result[0] if result else None
    
    async def set_channel_visibility(self, guild_id: int, channel_id: int, visible: bool):
        """Set channel visibility for bot"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO channel_visibility (guild_id, channel_id, visible, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """, (guild_id, channel_id, visible))
            await db.commit()
    
    async def get_channel_visibility(self, guild_id: int, channel_id: int) -> bool:
        """Get channel visibility setting"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT visible FROM channel_visibility 
                WHERE guild_id = ? AND channel_id = ?
            """, (guild_id, channel_id))
            result = await cursor.fetchone()
            return result[0] if result else True  # Default to visible
    
    async def create_match(self, match_data: dict):
        """Store match data in database"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO matches 
                (match_id, guild_id, title, teams, start_time, role_id, creator_id, language, image_url)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                match_data['id'],
                match_data['guild_id'],
                match_data['title'],
                match_data['teams'],
                match_data['start_time'],
                match_data['role_id'],
                match_data['creator_id'],
                match_data['language'],
                match_data.get('image_url')
            ))
            await db.commit()
    
    async def end_match(self, match_id: int):
        """Mark a match as ended"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE matches 
                SET status = 'ended', end_time = CURRENT_TIMESTAMP
                WHERE match_id = ?
            """, (match_id,))
            await db.commit()
    
    async def get_active_matches(self, guild_id: int) -> List[Dict]:
        """Get all active matches for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT * FROM matches 
                WHERE guild_id = ? AND status = 'active'
                ORDER BY start_time ASC
            """, (guild_id,))
            results = await cursor.fetchall()
            
            # Convert to dict format
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in results]
    
    async def log_command(self, command_name: str, guild_id: int, user_id: int):
        """Log command usage"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO command_logs (command_name, guild_id, user_id)
                VALUES (?, ?, ?)
            """, (command_name, guild_id, user_id))
            await db.commit()
    
    async def log_event(self, event_type: str, guild_id: int, description: str):
        """Log bot events"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO event_logs (event_type, guild_id, description)
                VALUES (?, ?, ?)
            """, (event_type, guild_id, description))
            await db.commit()
    
    async def get_command_stats(self, guild_id: int, days: int = 7) -> List[Dict]:
        """Get command usage statistics"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT command_name, COUNT(*) as usage_count
                FROM command_logs 
                WHERE guild_id = ? AND timestamp > datetime('now', '-{} days')
                GROUP BY command_name
                ORDER BY usage_count DESC
            """.format(days), (guild_id,))
            results = await cursor.fetchall()
            
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in results]
    
    async def get_guild_language(self, guild_id: int) -> str:
        """Get preferred language for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                SELECT language FROM guild_settings WHERE guild_id = ?
            """, (guild_id,))
            result = await cursor.fetchone()
            return result[0] if result else 'en'
    
    async def set_guild_language(self, guild_id: int, language: str):
        """Set preferred language for a guild"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT OR REPLACE INTO guild_settings (guild_id, language)
                VALUES (?, ?)
                ON CONFLICT(guild_id) DO UPDATE SET language = ?
            """, (guild_id, language, language))
            await db.commit()
    
    async def cleanup_old_logs(self, days: int = 30):
        """Clean up old log entries"""
        async with aiosqlite.connect(self.db_path) as db:
            # Clean old command logs
            await db.execute("""
                DELETE FROM command_logs 
                WHERE timestamp < datetime('now', '-{} days')
            """.format(days))
            
            # Clean old event logs
            await db.execute("""
                DELETE FROM event_logs 
                WHERE timestamp < datetime('now', '-{} days')
            """.format(days))
            
            await db.commit()
