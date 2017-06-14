from slackclient import SlackClient
import db
import logging
import os
import time

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def parse_data(slack_rtm_data):
    from_user, msg_content, date, channel = [None] * 4
    if slack_rtm_data:
        for messages_obj in slack_rtm_data:
            if (messages_obj and "text" in messages_obj
                    and "bot_id" not in messages_obj):
                msg_content = messages_obj["text"]
                from_user = messages_obj["user"]
                date = messages_obj["ts"]
                channel = messages_obj["channel"]
    return from_user, msg_content, date, channel


def main():
    slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))
    if slack_client.rtm_connect():
        logger.info("Bot started and running")
        while True:
            from_user, message, date, channel = parse_data(
                slack_client.rtm_read())
            if all([from_user, message, date, channel]):
                db.save_data(channel, from_user, message, date)
            time.sleep(1)
    else:
        logger.error("Connection failed. Invalid token or Slack is down!",
                     exc_info=True)


if __name__ == "__main__":
    main()
