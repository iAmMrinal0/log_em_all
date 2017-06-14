# Log'em all

A Slack bot which monitors all messages and logs them

## Requirements

1. Python >= 3.4
2. Install `slackclient` using `pip` or just do `pip install -r requirements.txt`
3. Create a bot user for your team from this [link](https://slack.com/apps/A0F7YS25R-bots)
4. Get your Slack API token after you select your bot username.
5. Export the API token as an environment variable.

``` shell
export SLACK_BOT_TOKEN='xoxb-xxxxxxxxxxxxxxxxxxx'
```

## How to run

1. Run `python start_bot.py` to start the bot.
2. The bot will now listen to all messages in the team in all the channels it is a part of and store them.

### License
 See the [LICENSE](LICENSE) file for license rights and limitations (MIT)
