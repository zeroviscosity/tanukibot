from pathlib import Path
import random
import re
import time
from slackclient import SlackClient
from .core import Core

MENTION_REGEX = '^<@(|[WU].+?)> (.+)'

class SlackBot:
    def __init__(self, token, ids, names, rtm_read_delay=1, *args, **kwargs):
        self.ids = ids
        self.names = names
        self.rtm_read_delay = rtm_read_delay

        self.ids.append('all')
        self.models = {}
        for id in self.ids:
            filename = self.get_filename(id)
            if not Path(filename).is_file():
                with open(filename, 'a') as f:
                    f.write('lol\n')
            self.models[id] = Core(filename, *args, **kwargs)

        self.bot_id = None
        self.slack_client = SlackClient(token)

    def get_filename(self, id):
        return 'data/' + id + '.txt'

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
            author_id = event['user']
            if user_id == self.bot_id:
                print('Processing:', event)
                words = message.split(' ')
                name = words[0].lower()
                if name in self.names:
                    message = ' '.join(words[1:])
                    model = self.models[self.names[name]]
                else:
                    model = self.models['all']
                sentence = model.get_sentence(message)
                self.post_message(sentence, channel)
            elif author_id in self.ids:
                print('Saving:', event)
                text = event['text'] + '\n'
                with open(self.get_filename(author_id), 'a') as f:
                    f.write(text)
                    self.models[author_id].generate_sentences()
                with open(self.get_filename('all'), 'a') as f:
                    f.write(text)
                    self.models['all'].generate_sentences()

    def parse_direct_mention(self, message):
        matches = re.search(MENTION_REGEX, message)
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)

    def post_message(self, message, channel):
        self.slack_client.api_call(
            'chat.postMessage',
            channel=channel,
            text=message
        )
