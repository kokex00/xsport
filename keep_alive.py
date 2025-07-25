"""Keep-alive server to maintain bot uptime on Replit and similar platforms"""

from flask import Flask
import threading
import time
import os

# Create Flask app for keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    """Simple health check endpoint"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>xSportBS Bot - Keep Alive</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: linear-gradient(135deg, #5865f2, #007bff); 
                color: white; 
                text-align: center; 
                padding: 50px; 
            }
            .container { 
                max-width: 600px; 
                margin: 0 auto; 
                background: rgba(255,255,255,0.1); 
                padding: 30px; 
                border-radius: 15px; 
            }
            .status { 
                font-size: 24px; 
                margin: 20px 0; 
            }
            .bot-info { 
                background: rgba(255,255,255,0.1); 
                padding: 20px; 
                border-radius: 10px; 
                margin: 20px 0; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 xSportBS Bot</h1>
            <div class="status">
                <span style="color: #00ff00;">● ONLINE</span>
            </div>
            <div class="bot-info">
                <h3>Bot Status</h3>
                <p><strong>Name:</strong> xSportBS</p>
                <p><strong>Version:</strong> 2.0</p>
                <p><strong>Developer:</strong> kokex</p>
                <p><strong>Server:</strong> <a href="https://discord.gg/5BHpgnG8QP" style="color: #00ff88;">Join Discord</a></p>
                <p><strong>Features:</strong> Multilingual Support, Match Management, Image Upload</p>
            </div>
            <p>Keep-alive server is running. Bot is active and ready!</p>
            <p><em>Made by kokex - xSportBS</em></p>
        </div>
    </body>
    </html>
    '''

@app.route('/status')
def status():
    """API endpoint for bot status"""
    return {
        "status": "online",
        "bot": "xSportBS",
        "version": "2.0",
        "developer": "kokex",
        "timestamp": time.time(),
        "message": "Bot is running successfully!"
    }

@app.route('/health')
def health():
    """Health check endpoint"""
    return {
        "health": "ok",
        "uptime": time.time(),
        "service": "xSportBS Keep-Alive"
    }

def run_flask():
    """Run the Flask keep-alive server"""
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

def keep_alive():
    """Start the keep-alive server in a separate thread"""
    print("🚀 Starting keep-alive server...")
    
    # Start Flask server in a separate thread
    server_thread = threading.Thread(target=run_flask, daemon=True)
    server_thread.start()
    
    print("✅ Keep-alive server started on port 5000")
    print("🌐 Access: http://0.0.0.0:5000")
    
    return server_thread

if __name__ == "__main__":
    # If run directly, start the keep-alive server
    keep_alive()
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Keep-alive server stopped")
