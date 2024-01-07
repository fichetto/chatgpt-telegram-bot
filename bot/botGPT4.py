import os
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from openai import OpenAI
from datetime import datetime

# Carica le variabili d'ambiente
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inizializza il client OpenAI
client = OpenAI(api_key=OPENAI_API_KEY)

def start(update, context):
    """Invia un messaggio di benvenuto."""
    update.message.reply_text('Ciao! Sono un bot alimentato da GPT-3.')

def get_chat_history(chat_id):
    """Recupera la cronologia della chat da un file."""
    file_name = f"chat_history_{chat_id}.txt"
    try:
        with open(file_name, "r") as file:
            return file.read()
    except FileNotFoundError:
        return ""

def save_chat_message(chat_id, username, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name = f"chat_history_{chat_id}.txt"
    with open(file_name, "a") as file:
        #file.write(f"{username}: {message}\n")
        file.write(f"[{timestamp}] {username}: {message}\n")

def truncate_chat_history(chat_history, new_message, max_tokens=4096):
    # Aggiungi il nuovo messaggio alla chat history
    updated_history = chat_history + "\n" + new_message

    # Calcola la lunghezza del contesto in token (questo è un esempio semplificato)
    total_length = len(updated_history)

    # Tronca i messaggi più vecchi se necessario
    while total_length > max_tokens:
        first_newline = updated_history.find('\n')
        if first_newline != -1:
            updated_history = updated_history[first_newline + 1:]
        else:
            updated_history = ""  # Nessun newline, cancella tutto
        total_length = len(updated_history)

    return updated_history

def remove_timestamps(chat_history):
    # Rimuove i timestamp dalla cronologia della chat
    # Questo è un esempio, la logica potrebbe dipendere dal formato esatto dei tuoi timestamp
    return '\n'.join(line.split('] ')[1] if '] ' in line else line for line in chat_history.split('\n'))

def get_current_context(chat_id, new_message):
    chat_history = get_chat_history(chat_id)
    chat_history_without_timestamps = remove_timestamps(chat_history)
    truncated_history = truncate_chat_history(chat_history_without_timestamps, new_message)
    return truncated_history

def respond(update, context):
    chat_id = update.effective_chat.id
    user_message = update.message.text
    username = update.message.from_user.username

    save_chat_message(chat_id, username, user_message)

    if '@assitecnocons' in user_message or 'Tecnocons_BOT' in user_message:
        context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
        time.sleep(1)

        current_context = get_current_context(chat_id, f"User: {user_message}")

        response = client.chat.completions.create(
            messages=[{"role": "system", "content": "You are a helpful assistant. Please read all user content before answer."}]
                    + [{"role": "user", "content": current_context}],
            model="gpt-3.5-turbo"
        )

        reply_text = response.choices[0].message.content.strip()
        save_chat_message(chat_id, "Bot", reply_text)
        update.message.reply_text(reply_text)

def main():
    """Avvia il bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
