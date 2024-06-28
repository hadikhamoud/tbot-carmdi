from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
import os
from dotenv import load_dotenv
from database import search_numbers, search_cars
import utils
load_dotenv()



TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_API_KEY")


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Send me a message with a number or a number followed by a letter.')

def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text.strip()
    
    checked_input_status = utils.check_user_input(text)
    if checked_input_status == "car valid":    
        results = search_cars(text)
        update.message.reply_text(f"Searching for cars... Found: {results}")
    elif checked_input_status == "phone valid":
        results = search_numbers(text)
        keyboard = [[InlineKeyboardButton(f"Option {i+1}", callback_data=str(i))] for i in range(len(results))]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Choose an option:', reply_markup=reply_markup)
        context.user_data['results'] = results
    elif checked_input_status == "invalid":
        update.message.reply_text('Error: Please send a valid input (number or number followed by a letter).')

def handle_option_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    option_index = int(query.data)
    results = context.user_data.get('results', [])
    if results and 0 <= option_index < len(results):
        selected_option = results[option_index]
        query.edit_message_text(text=f"You selected: {selected_option}")
    else:
        query.edit_message_text(text="Invalid selection.")

def main() -> None:
    updater = Updater(TELEGRAM_TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))

    # on non-command i.e message - handle the message
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Handle callback queries from inline keyboard
    dispatcher.add_handler(CallbackQueryHandler(handle_option_selection))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
