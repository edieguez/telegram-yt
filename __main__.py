#! /usr/bin/env python
import os

from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import Filters

from downloader import download_audio


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to my velvet room')


def download_video(update: Update, context: CallbackContext) -> None:
    update.message.reply_chat_action(ChatAction.RECORD_AUDIO)
    audio_file, display_name = download_audio(update.message.text)

    update.message.reply_chat_action(ChatAction.UPLOAD_AUDIO)
    update.message.reply_audio(
        audio_file,
        title=display_name,
        filename=f'{display_name}.mp3',
        quote=True,
        timeout=180
    )

    os.remove(audio_file.name)


def error_handler(update: Update, context: CallbackContext) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id, text="Unexpected error")


API_BOT_TOKEN = os.environ['API_BOT_TOKEN']
updater = Updater(API_BOT_TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler((Filters.text), download_video))
updater.dispatcher.add_error_handler(error_handler)

updater.start_polling()
updater.idle()
