# track_my_report

A Slack bot which saves messages when you tag it

## Requirements

1. Python >= 3.4
2. Install `slackclient` using `pip` or just do `pip install -r requirements.txt`
3. Create a bot user for your team from this [link](https://slack.com/apps/A0F7YS25R-bots)
4. Get your Slack API token after you select your bot username.
5. Export the API token as an environment variable:

``` shell
export SLACK_BOT_TOKEN='xoxb-xxxxxxxxxxxxxxxxxxx'
```

## How to run

1. Change `BOT_NAME` variable in `bot_id.py` file and run the file using `python bot_id.py`
2. Export the bot ID received from step 1 as an environment variable.

``` shell
export BOT_ID='xxxxxxxx'
```

3. Now run `python start_bot.py` to start the bot.
4. The bot will now listen to all messages in the team in all the channels it is a part of, and whenever it is tagged, it will save whatever message the user provided.

### License
 See the [LICENSE](LICENSE) file for license rights and limitations (MIT)
