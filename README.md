# TanukiBot

## Installation

TBD

## SlackBot Usage

```python
import os
import tanukibot

token = os.environ.get('TANUKIBOT_TOKEN') # Slack token
ids = os.environ.get('TANUKIBOT_IDS') # Comma-separated Slack IDs

bot = tanukibot.SlackBot(token, ids.split(','))
bot.connect()
```

## SMSBot Usage

Deploy the bot on a publically accessible server and register the `/sms` endpoint with Twilio.

```python
from tanukibot import SMSBot

bot = SMSBot(corpus='/path/to/corpus')
bot.connect()
```

## Development

```
pip install -r requirements.txt
```
