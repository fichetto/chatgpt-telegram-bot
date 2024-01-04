import os
import openai
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Carica il token del bot e la chiave API di OpenAI dal file .env o dalle variabili d'ambiente
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Inizializza il client di OpenAI
openai.api_key = OPENAI_API_KEY

def start(update, context):
    """Invia un messaggio di benvenuto."""
    update.message.reply_text('Ciao! Sono un bot alimentato da GPT-3.')

def respond(update, context):
    """Prende il messaggio dell'utente e risponde utilizzando GPT-3."""
    user_message = update.message.text

    # Genera la risposta di GPT-3
    response = openai.Completion.create(
      engine="text-davinci-003",  # Puoi cambiare il modello se necessario
      prompt=user_message,
      max_tokens=50  # Puoi cambiare il numero di token in base alle tue necessità
    )

    # Invia la risposta generata al chat di Telegram
    update.message.reply_text(response.choices[0].text.strip())

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
