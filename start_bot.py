from slackclient import SlackClient
import os
import time


slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))


def split_bot_tag(message):
    bot_tag = "<@" + os.environ.get("BOT_ID") + ">"
    if bot_tag in message:
        return message[len(bot_tag) + 1:]


def parse_data(slack_rtm_data):
    if slack_rtm_data:
        for messages_obj in slack_rtm_data:
            if messages_obj and "text" in messages_obj:
                msg_content = split_bot_tag(messages_obj["text"])
                return msg_content


def main():
    if slack_client.rtm_connect():
        print("report_tracker connected and running")
        while True:
            message = parse_data(slack_client.rtm_read())
            if message:
                print(message)
            time.sleep(1)
    else:
        print("Connection failed. Invalid Slack token")


if __name__ == "__main__":
    main()
