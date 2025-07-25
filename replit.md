# xSportBS Discord Bot

## Overview

xSportBS is a powerful multilingual Discord bot designed for server management and match scheduling. Built with Python using discord.py, the bot provides comprehensive server administration tools, match management systems, and utility commands. The bot supports three languages (English, Portuguese, and Spanish) with automatic timezone conversion and includes a Flask web dashboard for documentation and support.

## User Preferences

Preferred communication style: Simple, everyday language.
Request for requirements.txt file: User requested adding requirements.txt file (note: Replit manages dependencies automatically through its packager system).

## System Architecture

### Core Architecture
- **Language**: Python 3.x
- **Framework**: discord.py with slash commands
- **Database**: SQLite with aiosqlite for async operations
- **Web Interface**: Flask with Bootstrap frontend
- **Deployment**: Designed for Replit with keep-alive functionality

### Modular Design
The bot follows a cog-based architecture for command organization:
- Admin commands (server management)
- Match management (scheduling and reminders)
- Utility commands (custom embeds, image handling)
- Help system with multilingual support

## Key Components

### 1. Bot Core (`bot.py`)
- Main bot class `XSportBSBot` extending `commands.Bot`
- Slash command integration
- Multilingual support with translation system
- Database initialization and management
- Automatic cog loading system

### 2. Command Modules (Cogs)
- **Admin Cog**: Server management, log channels, user/role DMs
- **Matches Cog**: Match creation, scheduling, automatic reminders
- **Utility Cog**: Custom embeds with image upload support
- **Help Cog**: Comprehensive command documentation

### 3. Utility Systems
- **Translation System**: Complete multilingual support (EN/PT/ES)
- **Timezone Handler**: Automatic timezone conversion based on language
- **Image Handler**: Device gallery image upload processing with PIL
- **Database Layer**: Async SQLite operations for data persistence

### 4. Web Dashboard
- Flask-based documentation interface
- Language switcher (EN/PT/ES)
- Command reference and bot information
- Support team contact information
- Responsive Bootstrap design

## Data Flow

### Command Processing
1. User issues slash command
2. Language detection from user locale
3. Permission validation (admin commands)
4. Database operations (if required)
5. Response generation with translation support
6. Logging to configured channels

### Match Management Flow
1. Admin creates match with `/creatematch`
2. Match stored in database with UTC timestamp
3. Background task monitors for reminder times
4. Automatic DM reminders sent (10min, 3min before)
5. Match can be ended with `/endmatch`

### Translation Flow
1. Commands detect user language preference
2. Responses generated in appropriate language
3. Translation buttons added to embeds
4. Timezone conversion applied automatically

## External Dependencies

### Required Packages
- `discord.py` - Discord API interaction
- `aiosqlite` - Async SQLite database operations
- `flask` - Web dashboard
- `pytz` - Timezone handling
- `Pillow (PIL)` - Image processing
- `aiohttp` - HTTP requests for image downloads

### Discord Permissions
- Send Messages
- Use Slash Commands
- Embed Links
- Attach Files
- Manage Messages (for admin functions)
- Read Message History

## Deployment Strategy

### Replit Deployment
- `keep_alive.py` provides Flask server for uptime monitoring
- `main.py` serves as entry point with async bot initialization
- Environment variable `DISCORD_TOKEN` for bot authentication
- SQLite database file (`xsportbs.db`) for persistent storage

### Database Schema
- `guild_settings` - Server configurations and log channels
- `channel_visibility` - Bot visibility per channel
- `matches` - Active and historical match data
- `command_logs` - Command usage tracking

### File Structure
```
├── bot.py              # Main bot class
├── main.py             # Entry point
├── keep_alive.py       # Uptime server
├── cogs/               # Command modules
├── utils/              # Utility systems
├── web/                # Flask dashboard
│   ├── templates/      # HTML templates
│   └── static/         # CSS/JS assets
└── xsportbs.db         # SQLite database
```

### Configuration
- Default language: English
- Supported languages: English, Portuguese, Spanish
- Command prefix: "!" (for legacy support)
- Primary interface: Slash commands
- Timezone mappings: GMT (EN), Portugal (PT), Spain (ES)

The bot is designed to be easily deployable on Replit with minimal configuration, requiring only the Discord bot token to be set as an environment variable.