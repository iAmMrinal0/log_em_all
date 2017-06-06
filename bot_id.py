from slackclient import SlackClient
import os


BOT_NAME = "report_tracker"


slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))


def main():
    api_call = slack_client.api_call("users.list")
    if (api_call.get("ok")):
        users = api_call.get("members")
        for user in users:
            if "name" in user and user.get("name") == BOT_NAME:
                print("Bot id for " + user["name"] + " is " + user["id"])
    else:
        print("No bot with " + BOT_NAME + " found")


if __name__ == "__main__":
    main()
