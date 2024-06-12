import os
import random
import sys
from pathlib import Path

import requests
import telegram
from dotenv import load_dotenv

TG_IMG_SIZE_LIMIT = 20971520


def download_image(link, img_path):
    response = requests.get(link)
    response.raise_for_status()

    with open(img_path, "wb") as file:
        file.write(response.content)


def main():
    load_dotenv()
    tg_token = os.environ["TG_TOKEN"]
    tg_channel_id = os.environ["TG_CHANNEL_ID"]

    tg_bot = telegram.Bot(token=tg_token)

    last_comic_url = "https://xkcd.com/info.0.json"
    last_response = requests.get(last_comic_url)
    last_response.raise_for_status()

    last_comic_number = last_response.json()["num"]
    rand_comic_number = random.randint(1, last_comic_number)

    comic_url = f"https://xkcd.com/{rand_comic_number}/info.0.json"
    response = requests.get(comic_url)
    response.raise_for_status()

    img_url = response.json()["img"]
    img_dir = Path(__file__).cwd()
    img_path = img_dir / Path(img_url).name
    transcript_text = response.json()["transcript"]
    alt_text = response.json()["alt"]

    download_image(img_url, img_path)

    if img_path.stat().st_size <= TG_IMG_SIZE_LIMIT:
        with open(img_path, "rb") as file:
            tg_bot.send_document(chat_id=tg_channel_id, document=file)
        if transcript_text:
            tg_bot.send_message(chat_id=tg_channel_id, text=transcript_text)
        else:
            tg_bot.send_message(chat_id=tg_channel_id, text=alt_text)
        img_path.unlink(missing_ok=True)
    else:
        img_path.unlink(missing_ok=True)
        sys.exit("Current image is too big for Telegram")


if __name__ == "__main__":
    main()
