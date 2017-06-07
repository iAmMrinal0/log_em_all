from slackclient import SlackClient
import os
import time


slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))


def save_data(user, content, date):
    filename = user + ".md"
    with open(filename, "a") as w:
        w.write(date + "\n" + content + "\n\n")


def get_data(user):
    filename = user + ".md"
    try:
        return open(filename, "r")
    except FileNotFoundError:
        return False


def post_response(channel, command):
    mode = "chat.postMessage"
    if command:
        file_content = get_data(channel)
        if file_content:
            mode = "files.upload"
            message_data = {"filename": "log.md",
                            "file": file_content,
                            "channels": channel}
        else:
            response = "There was an error handling your command."
            message_data = {"text": response,
                            "channel": channel,
                            "as_user": True}
    else:
        response = "I have added your message to the log with the \
current date."
        message_data = {"text": response,
                        "channel": channel,
                        "as_user": True}
    return slack_client.api_call(mode, **message_data)


def handle_response(response):
    if not response.get("ok"):
        return response["error"]


def split_bot_tag(message):
    bot_tag = "<@" + os.environ.get("BOT_ID") + ">"
    if bot_tag in message:
        return message[len(bot_tag) + 1:]


def is_dm(channel_id):
    return channel_id[0] == "D"


def parse_data(slack_rtm_data):
    from_user, msg_content, date, channel = [None] * 4
    if slack_rtm_data:
        for messages_obj in slack_rtm_data:
            if (messages_obj and "text" in messages_obj
                    and "bot_id" not in messages_obj
                    and is_dm(messages_obj["channel"])):
                msg_content = messages_obj["text"]
                from_user = messages_obj["user"]
                date = time.strftime("%d-%m-%Y",
                                     time.localtime(float(messages_obj["ts"])))
                channel = messages_obj["channel"]
    return from_user, msg_content, date, channel


def main():
    if slack_client.rtm_connect():
        print("report_tracker connected and running")
        while True:
            from_user, message, date, channel = parse_data(
                slack_client.rtm_read())
            if all([from_user, message, date, channel]):
                print(from_user, message, date)
                if message == "get":
                    command = True
                    channel = from_user
                else:
                    command = False
                    save_data(from_user, message, date)
                response = post_response(channel, command)
                error = handle_response(response)
                if error:
                    print(error)
            time.sleep(1)
    else:
        print("Connection failed. Invalid Slack token or Slack is down!")


if __name__ == "__main__":
    main()
