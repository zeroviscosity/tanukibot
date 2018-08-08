# TanukiBot

## Installation

TBD

## Usage

```python
import os
import tanukibot

token = os.environ.get('TANUKIBOT_SLACK_TOKEN')
target_id = os.environ.get('TANUKIBOT_TARGET_ID')

bot = tanukibot.Bot(token, target_id)
bot.connect()
```

## Development

```
pip install -r requirements.txt
```
