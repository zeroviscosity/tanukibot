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

## Development

```
pip install -r requirements.txt
```
