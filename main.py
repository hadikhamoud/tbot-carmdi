from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
import os
from dotenv import load_dotenv
from database import search_phone_numbers, search_cars
import utils

load_dotenv()



TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_API_KEY")

config = utils.read_config()


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(config['messages']['start'])

def handle_message(update: Update, context: CallbackContext) -> None:
    text = update.message.text.strip()
    
    checked_input_status = utils.check_user_input(text)
    if checked_input_status == "car valid":    
        col_names, results = search_cars(text)
        if len(results) == 0:
            update.message.reply_text(config['messages']['no_results'])
        else:
            result = results[0]
            result_text = "\n".join([f"{col_name}: {result[i]}" for i, col_name in enumerate(col_names)])
            update.message.reply_text(result_text)


    elif checked_input_status == "phone valid":
        col_names,results = search_phone_numbers(text)
            
        if len(results) == 0:
            update.message.reply_text(config['messages']['no_results'])
        else:
            phone_numbers = [result[utils.TEL_PROP_INDEX] for result in results]
    
            # Display phone numbers as options in the inline keyboard
            keyboard = [[InlineKeyboardButton(phone_numbers[i], callback_data=str(i))] for i in range(len(results))]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text(config['messages']['choose_option'], reply_markup=reply_markup)
            context.user_data['results'] = results
            context.user_data['col_names'] = col_names


    elif checked_input_status == "invalid":
        update.message.reply_text(config['messages']['invalid_input'])

def handle_option_selection(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    option_index = int(query.data)
    col_names = context.user_data.get('col_names', [])
    results = context.user_data.get('results', [])
    if results and 0 <= option_index < len(results):
        selected_option = results[option_index]
        result_text = "\n".join([f"{col_name}: {selected_option[i]}" for i, col_name in enumerate(col_names)])
        query.edit_message_text(text=f"{result_text}")
    else:
        query.edit_message_text(text=config['messages']['invalid_selection'])

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
