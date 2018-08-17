=====================
WebComic Telegram Bot
=====================

***************
What it this?
***************

This is a very simple Telegram bot using Amazon Lambda as a backed for processing user messages. It can be currently found as @web_comic_bot on Telegram

***************
Deployment
***************

This project uses `Serverless <https://github.com/serverless/serverless>`_ to automate the deployment.
It can be called via

``serverless deploy``


***************
TODO
***************
At this point, the future of this bot is not certain. It could either be used by individual users or send regular updates to a Telegram channel. This needs to be decided.
Depending on the above decision todos are either:

* Allow users to subscribe to particular comics
* Store state of last update sent to user (to avoid flooding the user)

or:

* Store the state in DynamoDB or something similar
* Change the AWS Lambda function to a scheduled one

Independent todos:

* tests/CI!
* figure out if feed parsing can be optimized.