"""Simple Telegram bot for getting the latest web comics"""

import json
import logging
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(HERE, "./vendored"))

import feedparser
import telegram
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters

TOKEN = os.environ['TELEGRAM_TOKEN']
FEED_MAP = {
    "smbc": {
        "url": "https://www.smbc-comics.com/comic/rss",
    },
    "xkcd": {
        "url": "https://xkcd.com/rss.xml"
    },
    "ch": {
        "url": "http://feeds.feedburner.com/Explosm"
    },
    "bugbash": {
        "url": "http://feeds.feedburner.com/BugBash"
    },
    "dilbert": {
        "url": "http://feed.dilbert.com/dilbert/daily_strip"
    },
    "oglaf": {
        "url": "https://www.oglaf.com/feeds/rss/"
    },
    "myjetpack": {
        "url": "http://myjetpack.tumblr.com/rss"
    },
    "frogpants": {
        "url": "https://www.frogpants.com/2018?format=rss"
    },
    "geekandpoke": {
        "url": "http://feeds.feedburner.com/GeekAndPoke"
    },
    "oatmeal": {
        "url": "http://feeds.feedburner.com/oatmealfeed"
    }
}

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def get_latest(comic):
    logger.info("Searching for comic %s.", comic)
    if comic in FEED_MAP:
        feed = feedparser.parse(FEED_MAP[comic]["url"])
        return (
            feed['entries'][0]['title'] + "\n" +
            feed['entries'][0]['link'])
    logger.info("Comic %s not found in mapping", comic)
    return "Sorry {0} is not supported yet".format(comic)


def get(bot, update, args):
    logger.info('Args: {}'.format(args))
    if len(args):
        if args[0] == "all":
            for comic in FEED_MAP:
                bot.send_message(
                    chat_id=update.message.chat_id,
                    text=get_latest(comic))
        else:
            bot.send_message(
                chat_id=update.message.chat_id,
                text=get_latest(args[0]))
    else:
        bot.send_message(
            chat_id=update.message.chat_id,
            text="I need something to work with")


def webcomic_bot(event, context):
    """Entrypoint for AWS Lambda"""
    logger.info('Event: %s', event)
    logger.info("Request ID: %s", context.aws_request_id)

    try:
        bot = telegram.Bot(TOKEN)
        dispatcher = Dispatcher(bot, None, workers=0)
        data = json.loads(event["body"])
        update = telegram.update.Update.de_json(data, bot)
        dispatcher.add_handler(CommandHandler('get', get, pass_args=True))
        dispatcher.process_update(update)

    except Exception as error:
        logger.exception(error)

    return {"statusCode": 200}
