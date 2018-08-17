import json
import logging
import os
import sys
import logging

HERE = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(HERE, "./vendored"))

import requests
import feedparser

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)
FEED_MAP = {
    "smbc": "https://www.smbc-comics.com/comic/rss"
}

class WebComicBot:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    @classmethod
    def get_latest(cls, comic):
        if comic in FEED_MAP:
            feed = feedparser.parse(FEED_MAP[comic])
            return feed['entries'][0]['title'] + "\n" + feed['entries'][0]['link']
        logger.info("Comic %s not found in mapping", comic)    
        return "Sorry {0} is not supported yet".format(comic)

    def get_command(self, message):
        logger.debug("Parsing user's /get command: %s", message)
        command_content = message.replace("/get ", "")
        return self.get_latest(command_content)

    def create_response(self, message):
        if message.startswith("/start"):
            logger.debug("User sent a /start command")
            return "It's a shame but this command doesn't do anything actually"
        if message.startswith("/get"):
            logger.debug("User sent a /get command")
            return self.get_command(message)

        return "I don't know what you mean. Please try again"

    def send_response(self, message):
        data = {"text": message.encode("utf8"), "chat_id": self.chat_id}
        logger.debug("Sending message %s to chat %s", data["text"], data["chat_id"])
        requests.post(BASE_URL + "/sendMessage", data)

    def respond(self, message):
        response = self.create_response(message)
        self.send_response(response)


def bot(event, context):
    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]
        logger.info("Received message %s from %s", message, chat_id)
        bot = WebComicBot(chat_id)
        bot.respond(message)

    except Exception as e:
        print(e)

    return {"statusCode": 200}
