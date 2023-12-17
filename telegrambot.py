from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from Translation import Translate
TOKEN = '6891598068:AAHPqBJwWE7olEzMepZ5UUn_3sUneWYbwh8'
CHOOSING = range(2)
language={"Python":("Python",".py"),"Java":("Java",".java"),"C++":("C++",".cpp"),"C":("C",".c"),"Ruby":("Ruby",".r"),"JavaScripte":("JavaScripte",".js")}
reply_markup = ReplyKeyboardMarkup([["Python","Java"],["C++","C"],["Ruby","JavaScripte"]], one_time_keyboard=True, resize_keyboard=True)
user_data = {}
def start(update, context):
    update.message.reply_text('Hello! I am your Telegram bot.')
def handle_document(update, context):
    document = update.message.document
    user_data["File"]=context.bot.get_file(document.file_id).download()
    update.message.reply_text("Select The translation Language:",reply_markup=reply_markup)
    return CHOOSING
def choose_option(update, context):
    user_text = update.message.text
    user_data['choice'] = language[user_text]
    update.message.reply_text("Pleas Wait File is getting translated.....")
    user_data["Response"]=Translate(user_data["File"],user_data["choice"])
    with open(user_data["Response"], 'rb') as file:
        context.bot.send_document(chat_id=update.message.chat_id, document=file)
    update.message.reply_text("Done")
    user_data.clear()
    return ConversationHandler.END
def cancel(update, context):
    update.message.reply_text("Translation canceled.")
    user_data.clear()
    return ConversationHandler.END
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.document, handle_document)],
        states={
            CHOOSING: [MessageHandler(Filters.text & ~Filters.command, choose_option)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()
if __name__ == '__main__':
    main()