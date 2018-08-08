import random
import re
import time
from slackclient import SlackClient
from .core import Core

MENTION_REGEX = '^<@(|[WU].+?)>(.*)'

class Bot(Core):
    def __init__(self, token, target_id, rtm_read_delay=1, stock_phrases=[], posting_channels=[], *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.token = token
        self.target_id = target_id
        self.rtm_read_delay = rtm_read_delay
        self.stock_phrases = stock_phrases
        self.posting_channels = posting_channels
        self.bot_id = None
        self.new_sentences = 0

        self.slack_client = SlackClient(self.token)

    def connect(self):
        if self.slack_client.rtm_connect(with_team_state=False):
            print('TanukiBot connected and running!')
            # Read bot's user ID by calling Web API method `auth.test`
            self.bot_id = self.slack_client.api_call('auth.test')['user_id']
            while True:
                self.process_events(self.slack_client.rtm_read())
                time.sleep(self.rtm_read_delay)
        else:
            print('Connection failed. Exception traceback printed above.')

    def process_events(self, slack_events):
        for event in slack_events:
            # print('EVENT', event)
            if event['type'] != 'message' or 'subtype' in event:
                continue
            user_id, message = self.parse_direct_mention(event['text'])
            channel = event['channel']
            if user_id == self.bot_id:
                print('Processing:', event)
                sentence = self.get_sentence(message)
                self.post_message(sentence, channel)
                return
            
            if event['user'] == self.target_id:
                print('Saving:', event)
                with open(self.corpus, 'a') as f:
                    text = event['text'] + '\n'
                    f.write(text)
                self.new_sentences += 1
                if self.new_sentences % 5 == 0:
                    self.generate_sentences()

            # Randomly post a stock phrase in one of the approved channels
            rand = random.randrange(100)
            if channel in self.posting_channels and rand < len(self.stock_phrases):
                stock_phrase = self.stock_phrases[rand]
                self.post_message(stock_phrase, channel)

    def parse_direct_mention(self, message):
        matches = re.search(MENTION_REGEX, message)
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def post_message(self, message, channel):
        """
        Posts a message in a channel.
        """
        self.slack_client.api_call(
            'chat.postMessage',
            channel=channel,
            text=message
        )
