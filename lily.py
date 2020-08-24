import os
from telegram.ext  import Updater, CommandHandler, MessageHandler, Filters
import dialogflow
updater = Updater(token='970206869:AAHniFy5XySKlbhZwDe0uE0eP2bGfKudgVc') # Токен API к Telegram
dispatcher = updater.dispatcher
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'annulet-cffd-0aac53ba3794.json'# скачнный JSON


DIALOGFLOW_PROJECT_ID = 'annulet-cffd' #PROJECT ID из DialogFlow 
DIALOGFLOW_LANGUAGE_CODE = 'ru' # язык
SESSION_ID = 'annulet_bot'  # ID бота из телеграма

def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Добрый день')

def textMessage(bot, update):

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, SESSION_ID)
    text_input = dialogflow.types.TextInput(text=update.message.text , language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)
    try:
        response = session_client.detect_intent(session=session, query_input=query_input)
    except InvalidArgument:
         raise

    text = response.query_result.fulfillment_text
    if text:
        bot.send_message(chat_id=update.message.chat_id, text= response.query_result.fulfillment_text)
    else:
        bot.send_message(chat_id=update.message.chat_id, text= 'что?')


# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
