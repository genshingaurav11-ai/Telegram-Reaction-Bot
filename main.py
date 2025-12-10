# main.py (Reaction Bot - FINAL FIX and Updated Start Message)
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
    
    # ⚠️ CORE REACTION BOT LOGIC START
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
            
            # FIX: Agar defined reactions mein nahi mila, to default response dein aur log karein.
            if response_text is None:
                response_text = f"Received reaction: {first_reaction}. (Reacting to ensure connection is live)"
                logger.info(f"Unhandled reaction received: {first_reaction}") 

            if response_text:
                run_sync(BOT.send_message(
                    chat_id, 
                    response_text,
                    reply_to_message_id=message_id,
                    parse_mode='Markdown'
                ))
        return
    # ⚠️ CORE REACTION BOT LOGIC ENDS
    
    # Simple /start handler (UPDATED MESSAGE)
    message_data = update_data.get('message', {})
    text = message_data.get('text', '').strip()
    chat_id = message_data.get('chat', {}).get('id')
    
    if text == "/start" and chat_id:
        
        # ⚠️ UPDATED START MESSAGE
        start_message = (
            "🚀 **I'm ready for reactions!**\n\n"
            "Please use any of these emojis on a message to see me respond:\n"
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
