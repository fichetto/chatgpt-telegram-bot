import os
import time
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ChatAction
from openai import OpenAI

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

def save_chat_message(chat_id, message):
    """Salva il messaggio nel file della cronologia della chat."""
    file_name = f"chat_history_{chat_id}.txt"
    with open(file_name, "a") as file:
        file.write(f"{message}\n")

# def respond(update, context):
#     chat_id = update.effective_chat.id
#     user_message = update.message.text

#     # Mostra che il bot sta scrivendo
#     context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)
#     time.sleep(1)

#     # Aggiorna la cronologia della chat
#     save_chat_message(chat_id, f"User: {user_message}")

#     # Recupera la cronologia della chat
#     chat_history = get_chat_history(chat_id)

#     # Genera una risposta da GPT-3
#     response = client.chat.completions.create(
#         messages=[{"role": "system", "content": "You are a helpful assistant."}]
#                 + [{"role": "user", "content": chat_history}],
#         model="gpt-3.5-turbo"
#     )

#     # Estrai il testo della risposta
#     reply_text = response.choices[0].message.content.strip()
#     save_chat_message(chat_id, f"Bot: {reply_text}")

#     # Invia la risposta
#     update.message.reply_text(reply_text)

def respond(update, context):
    chat_id = update.effective_chat.id
    user_message = update.message.text

    # Mostra che il bot sta scrivendo
    context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    # Inizia lo streaming della risposta da GPT-4
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_message}],
        stream=True,
    )

    try:
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                # Invia ogni pezzo della risposta non appena disponibile
                context.bot.send_message(chat_id=chat_id, text=chunk.choices[0].delta.content)
    except Exception as e:
        # Gestisci eventuali eccezioni
        print(f"Errore durante lo streaming della risposta: {e}")


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
