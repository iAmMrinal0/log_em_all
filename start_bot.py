from slackclient import SlackClient
import os
import time


slack_client = SlackClient(os.environ.get("SLACK_BOT_TOKEN"))


def main():
    if slack_client.rtm_connect():
        print("report_tracker connected and running")
        while True:
            output = slack_client.rtm_read()
            print(output)
            time.sleep(1)
    else:
        print("Connection failed. Invalid Slack token")


if __name__ == "__main__":
    main()
