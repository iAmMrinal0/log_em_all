from slackclient import SlackClient
import os
import time


slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))


def save_data(user, content, date):
    filename = user + ".md"
    with open(filename, "a") as w:
        w.write(date + "\n" + content + "\n\n")


def split_bot_tag(message):
    bot_tag = "<@" + os.environ.get("BOT_ID") + ">"
    if bot_tag in message:
        return message[len(bot_tag) + 1:]


def parse_data(slack_rtm_data):
    if slack_rtm_data:
        for messages_obj in slack_rtm_data:
            if messages_obj and "text" in messages_obj:
                msg_content = split_bot_tag(messages_obj["text"])
                from_user = messages_obj["user"]
                date = time.strftime("%d-%m-%Y",
                                     time.localtime(float(messages_obj["ts"])))
                return from_user, msg_content, date
    return None, None, None


def main():
    if slack_client.rtm_connect():
        print("report_tracker connected and running")
        while True:
            from_user, message, date = parse_data(slack_client.rtm_read())
            if from_user and message and date:
                print(from_user, message, date)
                save_data(from_user, message, date)
            time.sleep(1)
    else:
        print("Connection failed. Invalid Slack token or Slack is down!")


if __name__ == "__main__":
    main()
