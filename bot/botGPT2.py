import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from openai import OpenAI

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

def start(update, context):
    """Send a welcome message."""
    update.message.reply_text('Hello! I am a bot powered by GPT-3.')

def respond(update, context):
    user_message = update.message.text

    # Invia un messaggio temporaneo per indicare che la risposta è in elaborazione
    temp_message = update.message.reply_text("Sto elaborando la tua richiesta...")

    # Genera una risposta da GPT-3
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": user_message}],
        model="gpt-3.5-turbo"  # Aggiorna il modello secondo necessità
    )

    # Estrai il testo della risposta
    reply_text = response.choices[0].message.content.strip()

    # Controlla se il messaggio temporaneo è ancora presente prima di inviare la risposta
    try:
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=temp_message.message_id)
        update.message.reply_text(reply_text)
    except Exception as e:
        print(f"Errore nell'invio della risposta: {e}")


def main():
    """Start the bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, respond))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
