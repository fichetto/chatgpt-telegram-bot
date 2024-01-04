from telegram.ext import Updater, CommandHandler

def start(update, context):
    """Invia un messaggio quando viene eseguito il comando /start."""
    update.message.reply_text('Ciao! Sono il tuo bot Telegram.')

def main():
    """Avvia il bot."""
    # Sostituisci 'YOUR_TOKEN' con il token effettivo del tuo bot.
    updater = Updater("1048683775:AAFnPAEHW0YICYApmxhBGuUqwujxywR5AgI", use_context=True)

    # Ottieni il dispatcher per registrare i gestori
    dp = updater.dispatcher

    # Registra un gestore di comandi; in questo caso gestisce il comando /start
    dp.add_handler(CommandHandler("start", start))

    # Avvia il bot
    updater.start_polling(timeout=10)

    # Esegui il bot finché non viene premuto Ctrl-C o il processo viene interrotto
    updater.idle()

if __name__ == '__main__':
    main()
