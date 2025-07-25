"""Flask web dashboard for xSportBS Bot"""

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Bot information
BOT_INFO = {
    "name": "xSportBS",
    "version": "2.0",
    "description": "A powerful multilingual Discord bot designed for server management and match scheduling.",
    "developer": "kokex",
    "support_team": [
        {"name": "kokex", "id": "1215053388404756580", "color": "blue"},
        {"name": "Wo", "id": "1162196073280966686", "color": "red"}
    ],
    "discord_server": "https://discord.gg/5BHpgnG8QP",
    "languages": ["en", "pt", "es"]
}

# Command information organized by category
COMMANDS = {
    "admin": [
        {
            "name": "/setlogchannel",
            "description": "Set the log channel for bot activity",
            "usage": "/setlogchannel <channel>",
            "permissions": "Administrator"
        },
        {
            "name": "/setchannelbot",
            "description": "Control bot visibility in specific channels",
            "usage": "/setchannelbot <channel> <visible>",
            "permissions": "Administrator"
        },
        {
            "name": "/dmuser",
            "description": "Send a DM to a specific user",
            "usage": "/dmuser <user> <message>",
            "permissions": "Administrator"
        },
        {
            "name": "/dmrole",
            "description": "Send a DM to all users with a specific role",
            "usage": "/dmrole <role> <message>",
            "permissions": "Administrator"
        }
    ],
    "matches": [
        {
            "name": "/creatematch",
            "description": "Create a new match with scheduling and image upload",
            "usage": "/creatematch <title> <teams> <time> <role> [image]",
            "permissions": "Administrator"
        },
        {
            "name": "/endmatch",
            "description": "End an active match by ID",
            "usage": "/endmatch <match_id>",
            "permissions": "Administrator"
        },
        {
            "name": "/listmatches",
            "description": "List all currently active matches",
            "usage": "/listmatches",
            "permissions": "Everyone"
        }
    ],
    "utility": [
        {
            "name": "/embed",
            "description": "Create custom embeds with image upload from device",
            "usage": "/embed <title> <description> [color] [image]",
            "permissions": "Administrator"
        },
        {
            "name": "/serverinfo",
            "description": "Display detailed server information",
            "usage": "/serverinfo",
            "permissions": "Everyone"
        },
        {
            "name": "/userinfo",
            "description": "Display user information",
            "usage": "/userinfo [user]",
            "permissions": "Everyone"
        },
        {
            "name": "/help",
            "description": "Show all available commands and assistance",
            "usage": "/help",
            "permissions": "Everyone"
        },
        {
            "name": "/about",
            "description": "About xSportBS Bot",
            "usage": "/about",
            "permissions": "Everyone"
        }
    ]
}

# Translations for the web interface
TRANSLATIONS = {
    "en": {
        "title": "xSportBS Bot Dashboard",
        "subtitle": "Server Management & Match System Bot",
        "description": "A powerful multilingual Discord bot designed for server management and match scheduling.",
        "features": "Key Features",
        "features_list": [
            "🌍 Multilingual Support - English, Portuguese, Spanish",
            "🔄 Translation Buttons - Instant language switching",
            "📱 Image Upload - Upload from device gallery/album",
            "⏰ Smart Reminders - Automatic match notifications",
            "🕒 Timezone Conversion - Auto-convert based on language",
            "📊 Activity Logging - Complete bot activity tracking",
            "🔒 Admin Protection - Secure admin-only commands"
        ],
        "support_team": "Support Team",
        "discord_server": "Discord Server",
        "commands": "Commands",
        "admin_commands": "Admin Commands",
        "match_commands": "Match Management",
        "utility_commands": "Utility Commands",
        "made_by": "Made by kokex - xSportBS",
        "view_commands": "View Commands",
        "back_to_home": "Back to Home"
    },
    "pt": {
        "title": "Painel do xSportBS Bot",
        "subtitle": "Bot de Gestão de Servidor e Sistema de Partidas",
        "description": "Um poderoso bot Discord multilíngue projetado para gestão de servidor e agendamento de partidas.",
        "features": "Recursos Principais",
        "features_list": [
            "🌍 Suporte Multilíngue - Inglês, Português, Espanhol",
            "🔄 Botões de Tradução - Mudança instantânea de idioma",
            "📱 Upload de Imagem - Envie da galeria/álbum do dispositivo",
            "⏰ Lembretes Inteligentes - Notificações automáticas de partidas",
            "🕒 Conversão de Fuso Horário - Conversão automática baseada no idioma",
            "📊 Log de Atividades - Rastreamento completo da atividade do bot",
            "🔒 Proteção Admin - Comandos seguros apenas para administradores"
        ],
        "support_team": "Equipe de Suporte",
        "discord_server": "Servidor Discord",
        "commands": "Comandos",
        "admin_commands": "Comandos de Admin",
        "match_commands": "Gestão de Partidas",
        "utility_commands": "Comandos de Utilidade",
        "made_by": "Feito por kokex - xSportBS",
        "view_commands": "Ver Comandos",
        "back_to_home": "Voltar ao Início"
    },
    "es": {
        "title": "Panel del xSportBS Bot",
        "subtitle": "Bot de Gestión de Servidor y Sistema de Partidos",
        "description": "Un poderoso bot de Discord multiidioma diseñado para gestión de servidor y programación de partidos.",
        "features": "Características Clave",
        "features_list": [
            "🌍 Soporte Multiidioma - Inglés, Portugués, Español",
            "🔄 Botones de Traducción - Cambio instantáneo de idioma",
            "📱 Subida de Imagen - Sube desde la galería/álbum del dispositivo",
            "⏰ Recordatorios Inteligentes - Notificaciones automáticas de partidos",
            "🕒 Conversión de Zona Horaria - Conversión automática según el idioma",
            "📊 Registro de Actividad - Seguimiento completo de la actividad del bot",
            "🔒 Protección Admin - Comandos seguros solo para administradores"
        ],
        "support_team": "Equipo de Soporte",
        "discord_server": "Servidor Discord",
        "commands": "Comandos",
        "admin_commands": "Comandos de Admin",
        "match_commands": "Gestión de Partidos",
        "utility_commands": "Comandos de Utilidad",
        "made_by": "Hecho por kokex - xSportBS",
        "view_commands": "Ver Comandos",
        "back_to_home": "Volver al Inicio"
    }
}

@app.route('/')
def index():
    """Main dashboard page"""
    language = request.args.get('lang', 'en')
    if language not in TRANSLATIONS:
        language = 'en'
    
    return render_template('index.html', 
                         bot_info=BOT_INFO, 
                         translations=TRANSLATIONS[language],
                         current_lang=language)

@app.route('/commands')
def commands():
    """Commands page"""
    language = request.args.get('lang', 'en')
    if language not in TRANSLATIONS:
        language = 'en'
    
    return render_template('commands.html',
                         commands=COMMANDS,
                         translations=TRANSLATIONS[language],
                         current_lang=language)

@app.route('/api/bot-status')
def bot_status():
    """API endpoint for bot status"""
    return jsonify({
        "status": "online",
        "version": BOT_INFO["version"],
        "uptime": "Active"
    })

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
