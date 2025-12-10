# ⚠️ CORE REACTION BOT LOGIC
        # ... (reaction_update, chat_id, message_id, new_reactions variable loading yahi rahega)

        if new_reactions:
            # Hum naye reactions mein se pehle emoji par focus karenge
            first_reaction = new_reactions[0]
            response_text = None
            
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
        return
        # ⚠️ REACTION BOT LOGIC ENDS HERE
