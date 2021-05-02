#! /usr/bin/env python
from os import environ, remove

from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext
from telegram.ext.filters import Filters

from downloader import download_audio


def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Welcome to my velvet room')


def hello(update: Update, context: CallbackContext) -> None:
    update.message.reply_chat_action(ChatAction.RECORD_AUDIO)
    audio_filename = download_audio(update.message.text)
    audio_file = open(audio_filename, 'rb')

    update.message.reply_chat_action(ChatAction.UPLOAD_AUDIO)
    update.message.reply_audio(audio_file, quote=True, timeout=180)

    remove(audio_file.name)


API_BOT_TOKEN = environ['API_BOT_TOKEN']
updater = Updater(API_BOT_TOKEN)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler((Filters.text), hello))

updater.start_polling()
updater.idle()

