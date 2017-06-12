from slackclient import SlackClient
import db
import os
import time


def process_data(data):
    messages_dict = {}
    for val in data:
        date = time.strftime("%d-%m-%Y", time.localtime(float(val[0])))
        adder = messages_dict.get(date, [])
        adder.append(val[1])
        messages_dict[date] = adder
    return messages_dict


def format_data(data):
    result = ""
    newline = "\n"
    for key, val in data.items():
        result += "*" + key + "*" + newline
        result += (newline * 2).join(val)
        result += newline * 2
    return result.strip()


def create_response(channel, user_id):
    mode = "chat.postMessage"
    file_content = db.get_data(channel, user_id)
    if file_content:
        mode = "files.upload"
        message_data = {"filename": "log.md",
                        "file": format_data(process_data(file_content)),
                        "channels": user_id}
    else:
        response = "There was an error handling your command."
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
                    and "bot_id" not in messages_obj):
                msg_content = messages_obj["text"]
                from_user = messages_obj["user"]
                date = messages_obj["ts"]
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
                if message.lower() == "get":
                    mode, kwargs = create_response(channel, from_user)
                    response = slack_client.api_call(mode, **kwargs)
                    error = handle_response(response)
                    if error:
                        print(error)
                else:
                    db.save_data(channel, from_user, message, date)
            time.sleep(1)
    else:
        print("Connection failed. Invalid Slack token or Slack is down!")


if __name__ == "__main__":
    main()
