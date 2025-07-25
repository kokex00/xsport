"""Translation system for multilingual support"""

LANGUAGES = {
    "en": "English",
    "pt": "Português", 
    "es": "Español"
}

TRANSLATIONS = {
    # General
    "made_by": {
        "en": "Made by kokex - xSportBS",
        "pt": "Feito por kokex - xSportBS",
        "es": "Hecho por kokex - xSportBS"
    },
    
    # Help Command
    "help_title": {
        "en": "🤖 xSportBS Bot - Help & Commands",
        "pt": "🤖 xSportBS Bot - Ajuda & Comandos", 
        "es": "🤖 xSportBS Bot - Ayuda y Comandos"
    },
    "help_description": {
        "en": "Welcome to xSportBS! Here are all available commands organized by category.",
        "pt": "Bem-vindo ao xSportBS! Aqui estão todos os comandos disponíveis organizados por categoria.",
        "es": "¡Bienvenido a xSportBS! Aquí están todos los comandos disponibles organizados por categoría."
    },
    "admin_commands": {
        "en": "🔧 Admin Commands",
        "pt": "🔧 Comandos de Admin",
        "es": "🔧 Comandos de Admin"
    },
    "admin_commands_list": {
        "en": "`/setlogchannel` - Set the log channel for bot activity\n`/setchannelbot` - Control bot visibility in specific channels\n`/dmuser` - Send a DM to a specific user\n`/dmrole` - Send a DM to all users with a specific role",
        "pt": "`/setlogchannel` - Definir o canal de logs para atividade do bot\n`/setchannelbot` - Controlar visibilidade do bot em canais específicos\n`/dmuser` - Enviar DM para um usuário específico\n`/dmrole` - Enviar DM para todos os usuários com um cargo específico",
        "es": "`/setlogchannel` - Establecer el canal de logs para actividad del bot\n`/setchannelbot` - Controlar visibilidad del bot en canales específicos\n`/dmuser` - Enviar DM a un usuario específico\n`/dmrole` - Enviar DM a todos los usuarios con un rol específico"
    },
    "match_commands": {
        "en": "⚽ Match Management",
        "pt": "⚽ Gestão de Partidas",
        "es": "⚽ Gestión de Partidos"
    },
    "match_commands_list": {
        "en": "`/creatematch` - Create a new match with scheduling and image upload\n`/endmatch` - End an active match by ID\n`/listmatches` - List all currently active matches",
        "pt": "`/creatematch` - Criar uma nova partida com agendamento e upload de imagem\n`/endmatch` - Terminar uma partida ativa por ID\n`/listmatches` - Listar todas as partidas atualmente ativas",
        "es": "`/creatematch` - Crear un nuevo partido con programación y subida de imagen\n`/endmatch` - Terminar un partido activo por ID\n`/listmatches` - Listar todos los partidos actualmente activos"
    },
    "utility_commands": {
        "en": "🛠️ Utility Commands",
        "pt": "🛠️ Comandos de Utilidade",
        "es": "🛠️ Comandos de Utilidad"
    },
    "utility_commands_list": {
        "en": "`/embed` - Create custom embeds with image upload from device\n`/serverinfo` - Display detailed server information\n`/userinfo` - Display user information\n`/help` - Show this help message",
        "pt": "`/embed` - Criar embeds personalizados com upload de imagem do dispositivo\n`/serverinfo` - Exibir informações detalhadas do servidor\n`/userinfo` - Exibir informações do usuário\n`/help` - Mostrar esta mensagem de ajuda",
        "es": "`/embed` - Crear embeds personalizados con subida de imagen desde dispositivo\n`/serverinfo` - Mostrar información detallada del servidor\n`/userinfo` - Mostrar información del usuario\n`/help` - Mostrar este mensaje de ayuda"
    },
    "features": {
        "en": "✨ Key Features",
        "pt": "✨ Recursos Principais",
        "es": "✨ Características Clave"
    },
    "features_list": {
        "en": "🌍 **Multilingual Support** - English, Portuguese, Spanish\n🔄 **Translation Buttons** - Instant language switching on all messages\n📱 **Image Upload** - Upload images from your device gallery/album\n⏰ **Smart Reminders** - Automatic DM reminders 10 & 3 minutes before matches\n🕒 **Timezone Conversion** - Times auto-convert based on language\n📊 **Activity Logging** - Complete bot activity tracking\n🔒 **Admin Protection** - Secure admin-only commands",
        "pt": "🌍 **Suporte Multilíngue** - Inglês, Português, Espanhol\n🔄 **Botões de Tradução** - Mudança instantânea de idioma em todas as mensagens\n📱 **Upload de Imagem** - Envie imagens da galeria/álbum do seu dispositivo\n⏰ **Lembretes Inteligentes** - Lembretes automáticos por DM 10 e 3 minutos antes das partidas\n🕒 **Conversão de Fuso Horário** - Horários se convertem automaticamente baseado no idioma\n📊 **Log de Atividades** - Rastreamento completo da atividade do bot\n🔒 **Proteção Admin** - Comandos seguros apenas para administradores",
        "es": "🌍 **Soporte Multiidioma** - Inglés, Portugués, Español\n🔄 **Botones de Traducción** - Cambio instantáneo de idioma en todos los mensajes\n📱 **Subida de Imagen** - Sube imágenes desde la galería/álbum de tu dispositivo\n⏰ **Recordatorios Inteligentes** - Recordatorios automáticos por DM 10 y 3 minutos antes de los partidos\n🕒 **Conversión de Zona Horaria** - Los horarios se convierten automáticamente según el idioma\n📊 **Registro de Actividad** - Seguimiento completo de la actividad del bot\n🔒 **Protección Admin** - Comandos seguros solo para administradores"
    },
    "support": {
        "en": "💬 Support",
        "pt": "💬 Suporte",
        "es": "💬 Soporte"
    },
    "support_info": {
        "en": "**Discord Server:** https://discord.gg/5BHpgnG8QP\n**Technical Support:** kokex | Wo\n**Need Help?** Use the translation buttons below!",
        "pt": "**Servidor Discord:** https://discord.gg/5BHpgnG8QP\n**Suporte Técnico:** kokex | Wo\n**Precisa de Ajuda?** Use os botões de tradução abaixo!",
        "es": "**Servidor Discord:** https://discord.gg/5BHpgnG8QP\n**Soporte Técnico:** kokex | Wo\n**¿Necesitas Ayuda?** ¡Usa los botones de traducción de abajo!"
    },
    
    # About Command
    "about_title": {
        "en": "🤖 About xSportBS Bot",
        "pt": "🤖 Sobre o xSportBS Bot",
        "es": "🤖 Acerca del xSportBS Bot"
    },
    "about_description": {
        "en": "A powerful multilingual Discord bot designed for server management and match scheduling.",
        "pt": "Um poderoso bot Discord multilíngue projetado para gestão de servidor e agendamento de partidas.",
        "es": "Un poderoso bot de Discord multiidioma diseñado para gestión de servidor y programación de partidos."
    },
    "about_bot_desc": {
        "en": "xSportBS is a comprehensive server management bot with advanced match scheduling, multilingual support, and image upload capabilities. Built specifically for the xSportBS community.",
        "pt": "xSportBS é um bot abrangente de gestão de servidor com agendamento avançado de partidas, suporte multilíngue e capacidades de upload de imagem. Construído especificamente para a comunidade xSportBS.",
        "es": "xSportBS es un bot integral de gestión de servidor con programación avanzada de partidos, soporte multiidioma y capacidades de subida de imágenes. Construido específicamente para la comunidad xSportBS."
    },
    "version_info": {
        "en": "**Version:** 2.0\n**Languages:** English, Portuguese, Spanish\n**Slash Commands:** ✅\n**Image Upload:** ✅\n**Translation Buttons:** ✅\n**Match System:** ✅\n**Admin Tools:** ✅",
        "pt": "**Versão:** 2.0\n**Idiomas:** Inglês, Português, Espanhol\n**Comandos Slash:** ✅\n**Upload de Imagem:** ✅\n**Botões de Tradução:** ✅\n**Sistema de Partidas:** ✅\n**Ferramentas Admin:** ✅",
        "es": "**Versión:** 2.0\n**Idiomas:** Inglés, Portugués, Español\n**Comandos Slash:** ✅\n**Subida de Imagen:** ✅\n**Botones de Traducción:** ✅\n**Sistema de Partidos:** ✅\n**Herramientas Admin:** ✅"
    },
    "team_info": {
        "en": "**Lead Developer:** kokex\n**Support Team:** Wo\n**Server:** xSportBS\n**Discord:** https://discord.gg/5BHpgnG8QP",
        "pt": "**Desenvolvedor Principal:** kokex\n**Equipe de Suporte:** Wo\n**Servidor:** xSportBS\n**Discord:** https://discord.gg/5BHpgnG8QP",
        "es": "**Desarrollador Principal:** kokex\n**Equipo de Soporte:** Wo\n**Servidor:** xSportBS\n**Discord:** https://discord.gg/5BHpgnG8QP"
    },
    "start_info": {
        "en": "Use `/help` to see all available commands.\nAdministrators can use `/setlogchannel` to set up logging.\nCreate matches with `/creatematch` and upload images from your device!",
        "pt": "Use `/help` para ver todos os comandos disponíveis.\nAdministradores podem usar `/setlogchannel` para configurar logging.\nCrie partidas com `/creatematch` e envie imagens do seu dispositivo!",
        "es": "Usa `/help` para ver todos los comandos disponibles.\nLos administradores pueden usar `/setlogchannel` para configurar el registro.\n¡Crea partidos con `/creatematch` y sube imágenes desde tu dispositivo!"
    },
    
    # Match System
    "match_created": {
        "en": "⚽ Match Created Successfully!",
        "pt": "⚽ Partida Criada com Sucesso!",
        "es": "⚽ ¡Partido Creado Exitosamente!"
    },
    "match_created_desc": {
        "en": "Your match has been created and scheduled successfully.",
        "pt": "Sua partida foi criada e agendada com sucesso.",
        "es": "Tu partido ha sido creado y programado exitosamente."
    },
    "match_id": {
        "en": "Match ID",
        "pt": "ID da Partida",
        "es": "ID del Partido"
    },
    "title": {
        "en": "Title",
        "pt": "Título",
        "es": "Título"
    },
    "teams": {
        "en": "Teams",
        "pt": "Equipes",
        "es": "Equipos"
    },
    "start_time": {
        "en": "Start Time",
        "pt": "Horário de Início",
        "es": "Hora de Inicio"
    },
    "notify_role": {
        "en": "Notify Role",
        "pt": "Notificar Cargo",
        "es": "Notificar Rol"
    },
    "active_matches": {
        "en": "📋 Active Matches",
        "pt": "📋 Partidas Ativas",
        "es": "📋 Partidos Activos"
    },
    "active_matches_desc": {
        "en": "Here are all currently active matches.",
        "pt": "Aqui estão todas as partidas atualmente ativas.",
        "es": "Aquí están todos los partidos actualmente activos."
    },
    
    # Server Info
    "server_info": {
        "en": "📊 Server Information",
        "pt": "📊 Informações do Servidor",
        "es": "📊 Información del Servidor"
    },
    "server_info_desc": {
        "en": "Detailed information about this server.",
        "pt": "Informações detalhadas sobre este servidor.",
        "es": "Información detallada sobre este servidor."
    },
    "general_info": {
        "en": "📋 General Info",
        "pt": "📋 Informações Gerais",
        "es": "📋 Información General"
    },
    "members": {
        "en": "👥 Members",
        "pt": "👥 Membros",
        "es": "👥 Miembros"
    },
    "channels": {
        "en": "📺 Channels",
        "pt": "📺 Canais",
        "es": "📺 Canales"
    },
    
    # User Info
    "user_info": {
        "en": "👤 User Information",
        "pt": "👤 Informações do Usuário",
        "es": "👤 Información del Usuario"
    },
    "user_info_desc": {
        "en": "Detailed information about this user.",
        "pt": "Informações detalhadas sobre este usuário.",
        "es": "Información detallada sobre este usuario."
    },
    "basic_info": {
        "en": "📋 Basic Info",
        "pt": "📋 Informações Básicas", 
        "es": "📋 Información Básica"
    },
    "dates": {
        "en": "📅 Dates",
        "pt": "📅 Datas",
        "es": "📅 Fechas"
    },
    
    # Log Channel
    "log_channel_set": {
        "en": "✅ Log Channel Set",
        "pt": "✅ Canal de Log Definido",
        "es": "✅ Canal de Log Establecido"
    },
    "log_channel_description": {
        "en": "Bot activity will now be logged to this channel.",
        "pt": "A atividade do bot agora será registrada neste canal.",
        "es": "La actividad del bot ahora se registrará en este canal."
    },
    "channel": {
        "en": "Channel",
        "pt": "Canal",
        "es": "Canal"
    },
    
    # Custom Embed
    "custom_embed": {
        "en": "📝 Custom Embed",
        "pt": "📝 Embed Personalizado",
        "es": "📝 Embed Personalizado"
    },
    "custom_embed_desc": {
        "en": "This is a custom embed created by an administrator.",
        "pt": "Este é um embed personalizado criado por um administrador.",
        "es": "Este es un embed personalizado creado por un administrador."
    },
    "description": {
        "en": "Description",
        "pt": "Descrição",
        "es": "Descripción"
    },
    "version_features": {
        "en": "🌟 Version & Features",
        "pt": "🌟 Versão & Recursos",
        "es": "🌟 Versión y Características"
    },
    "dev_team": {
        "en": "👨‍💻 Development Team",
        "pt": "👨‍💻 Equipe de Desenvolvimento",
        "es": "👨‍💻 Equipo de Desarrollo"
    },
    "getting_started": {
        "en": "🚀 Getting Started",
        "pt": "🚀 Começando",
        "es": "🚀 Empezando"
    }
}

def get_translation(key: str, language: str) -> str:
    """Get translation for a key in specified language"""
    if key not in TRANSLATIONS:
        return key
    
    if language not in TRANSLATIONS[key]:
        language = "en"  # Fallback to English
    
    return TRANSLATIONS[key][language]

def get_available_languages() -> dict:
    """Get all available languages"""
    return LANGUAGES
