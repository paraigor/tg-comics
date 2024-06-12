# XKCD comics Telegram

A script for downloading random image with comics from XKCD website and automatically publishing it to Telegram channel.

### Installation

Python3 should already be installed. 
Use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:
```
pip install -r requirements.txt
```
Telegram bot and channel (group) also needed for images publishing. Create bot via [@BotFather](https://t.me/BotFather). Bot token looks like: `1234567890:XXXxx0Xxx-xxxX0xXXxXxx0X0XX0XXXXxXx`.

Security sensitive information recommended storing in the project using `.env` files.

Key name to store bot API token value is `TG_TOKEN`.  
Key name to store Telegram channel ID is `TG_CHANNEL_ID`.

### Usage
```
$ python tg_comic_publish.py
```

### Project Goals

This code was written for educational purposes as part of an online course for web developers at [dvmn.org](https://dvmn.org/). 
 
