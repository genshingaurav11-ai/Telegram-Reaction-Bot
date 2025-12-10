# main.py (Reaction Bot - FINAL CODE)
import logging
import os
import sys
import asyncio 
from telegram import Bot
from flask import Flask, request, jsonify 
from typing import Final

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# --- SECURE TOKEN LOADING ---
BOT_TOKEN: Final = os.environ.get("BOT_TOKEN") 
if not BOT_TOKEN:
    logger.error("❌ FATAL: BOT_TOKEN environment variable not set!")
    sys.exit(1)
    
BOT = Bot(token=BOT_TOKEN)
# ---------------------

# --- ASYNC HELPER ---
def run_sync(coroutine):
    """Safely runs an async coroutine synchronously for Webhook."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coroutine)
# --------------------

def handle_update(update_data):
    """Processes a single Telegram Update dictionary (Raw JSON)."""
    
    # ⚠️ 1. MESSAGE REACTION HANDLING
    if 'message_reaction' in update_data:
        reaction_update = update_data['message_reaction']
        chat_id = reaction_update['chat']['id']
        message_id = reaction_update['message_id']
        
        new_reactions = [r['emoji'] for r in reaction_update.get('new_reaction', [])]
        
        if new_reactions:
            first_reaction = new_reactions[0]
            
            # --- Reaction Dictionary ---
            reaction_responses = {
                '💋': "A kiss back! 💋 Thank you!",
                '👻': "Boo! 👻 Did I scare you?",
                '👀': "I see what you did there! 👀",
                '🤯': "Mind Blown! 🤯 That's a strong reaction!",
                '💊': "Taking the pill, I see. 💊",
                '🙉': "Monkey business! 🙉",
                '🕊️': "Peace and harmony. 🕊️",
                '😻': "Awwww, cute! 😻",
                '👍': "Got the Thumbs Up! 👍",
                '🆒': "That's cool! 😎",
                '💗': "Sending love back! 💗",
                '🔥': "That's a FIRE reaction! 🔥"
            }
            # --- End Reaction Dictionary ---
            
            response_text = reaction_responses.get(first_reaction)
            
            if response_text:
                run_sync(BOT.send_message(
                    chat_id, 
                    response_text,
                    reply_to_message_id=message_id,
                    parse_mode='Markdown'
                ))
        return # Reaction handled, exit here

    
    # ⚠️ 2. ALL MESSAGE TYPES HANDLING (Text, Photo, File, Video)
    
    message_data = update_data.get('message', {})
    chat_id = message_data.get('chat', {}).get('id')
    
    if not chat_id:
        return

    text = message_data.get('text', '').strip()
    reply_to_message_id = message_data.get('message_id')

    response_text = None
    
    if message_data.get('photo'):
        response_text = "🖼️ I received a photo! Looking good."
    elif message_data.get('document'):
        response_text = "📄 File received! What's inside?"
    elif message_data.get('video'):
        response_text = "📹 Video received! Hope it's interesting."
    elif text and not text.startswith('/'):
        # Saada text (non-command)
        response_text = "💬 Got your message! Thanks for chatting."
    
    # Send response for any handled message type
    if response_text:
        run_sync(BOT.send_message(
            chat_id, 
            response_text, 
            reply_to_message_id=reply_to_message_id
        ))
        return
        
    # ⚠️ 3. START COMMAND HANDLING (If nothing else was handled)
    if text == "/start" and chat_id:
        start_message = (
            "🚀 **I'm ready for reactions and chat!**\n\n"
            "I will reply to any message (photo, video, file, or text) and also react to these emojis:\n"
            "💋 👻 👀 🤯 💊 🙉 🕊️ 😻 👍 🆒 💗 🔥"
        )
        
        run_sync(BOT.send_message(chat_id, start_message, parse_mode='Markdown'))
        return


# --- FLASK APPLICATION SETUP ---

def create_app():
    """Initializes the Flask app for Gunicorn/Webhook."""
    app = Flask(__name__)

    @app.route('/telegram', methods=['POST'])
    def webhook():
        if request.method == "POST":
            update_data = request.get_json()
            handle_update(update_data) 

        return jsonify({'status': 'ok'}), 200 

    return app
