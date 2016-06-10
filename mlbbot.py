import os
import time
import datetime
from datetime import datetime, timedelta
import mlbgame
from slackclient import SlackClient
from dotenv import load_dotenv
from os.path import join, dirname


#I want to refactor the games API calls below...
games_array = []
day = 


#Today's MLB Games!
todays_games_array = []
today = datetime.today()
today_game = mlbgame.games(today.year, today.month, today.day)
game = mlbgame.combine_games(today_game)
for g in game:
    todays_games_array.append(g)

#Yesterday's MLB Games!
yesterdays_games_array = []
yesterday = datetime.today() - timedelta(days=1)
yesterdays_games = mlbgame.games(yesterday.year, yesterday.month, yesterday.day)
yesterday_boxes = mlbgame.combine_games(yesterdays_games)
for g in yesterday_boxes:
    yesterdays_games_array.append(g)

#Tomorrow's MLB Games!
tomorrow_games_array = []
tomorrow = datetime.today() + timedelta(days=1)
tomorrow_games = mlbgame.games(tomorrow.year, tomorrow.month, tomorrow.day)
tomorrow_boxes = mlbgame.combine_games(tomorrow_games)
for g in tomorrow_boxes:
    tomorrow_games_array.append(g)


#Define function that will make API Call with appropriate response
def apicall(response):
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


# starterbot's IDs
BOT_NAME = 'mlbbot'
SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
BOT_ID = 'U1EJTDH9A'

# constants
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "games"
TODAY_COMMANDS = ['games today','todays games']
YESTERDAY_COMMANDS = ['games yesterday', 'yesterdays games']
TOMORROW_COMMANDS = ['games tomorrow','tomorrows games']

# instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """


    response = "Not sure what you mean. Type " + EXAMPLE_COMMAND + \
               " yesterday, today, or tomorrow for a list of todays games"
    if command.startswith(EXAMPLE_COMMAND):
        for g in todays_games_array:
            response = g
            apicall(g)
            
    else:
        apicall(response)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("MLBBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")