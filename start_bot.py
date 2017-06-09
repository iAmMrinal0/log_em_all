from slackclient import SlackClient
import db
import os
import time


def process_data(data):
    messages_dict = {}
    for val in data:
        adder = messages_dict.get(val[0], [])
        adder.append(val[1])
        messages_dict[val[0]] = adder
    return messages_dict


def format_data(data):
    result = ""
    newline = "\n"
    for key, val in data.items():
        result += "*" + key + "*" + newline
        result += (newline * 2).join(val)
        result += newline * 2
    return result.strip()


def create_response(channel, command):
    mode = "chat.postMessage"
    if command:
        file_content = db.get_data(channel)
        if file_content:
            mode = "files.upload"
            message_data = {"filename": "log.md",
                            "file": format_data(process_data(file_content)),
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
    return (mode, message_data)


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
    slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))
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
                    db.save_data(from_user, message, date)
                mode, kwargs = create_response(channel, command)
                response = slack_client.api_call(mode, **kwargs)
                error = handle_response(response)
                if error:
                    print(error)
            time.sleep(1)
    else:
        print("Connection failed. Invalid Slack token or Slack is down!")


if __name__ == "__main__":
    main()
