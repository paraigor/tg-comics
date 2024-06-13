import os
import random
import sys
from pathlib import Path

import requests
import telegram
from dotenv import load_dotenv

TG_IMG_SIZE_LIMIT = 20971520


def get_last_comic_num():
    comic_url = "https://xkcd.com/info.0.json"
    response = requests.get(comic_url)
    response.raise_for_status()
    return response.json()["num"]


def get_rand_comic():
    last_comic_number = get_last_comic_num()
    rand_comic_number = random.randint(1, last_comic_number)

    comic_url = f"https://xkcd.com/{rand_comic_number}/info.0.json"
    response = requests.get(comic_url)
    response.raise_for_status()

    img_url = response.json()["img"]
    transcript_text = response.json()["transcript"]
    alt_text = response.json()["alt"]

    return img_url, transcript_text, alt_text


def download_image(link, img_path):
    response = requests.get(link)
    response.raise_for_status()

    with open(img_path, "wb") as file:
        file.write(response.content)


def send_comic_tg(bot, chat_id, comic):
    img_path, transcript_text, alt_text = comic
    if img_path.stat().st_size <= TG_IMG_SIZE_LIMIT:
        with open(img_path, "rb") as file:
            bot.send_document(chat_id=chat_id, document=file)
        if transcript_text:
            bot.send_message(chat_id=chat_id, text=transcript_text)
        else:
            bot.send_message(chat_id=chat_id, text=alt_text)
    else:
        raise Exception


def main():
    load_dotenv()
    tg_token = os.environ["TG_TOKEN"]
    tg_channel_id = os.environ["TG_CHANNEL_ID"]

    tg_bot = telegram.Bot(token=tg_token)

    img_url, transcript_text, alt_text = get_rand_comic()
    img_dir = Path(__file__).cwd()
    img_path = img_dir / Path(img_url).name

    download_image(img_url, img_path)

    comic = (img_path, transcript_text, alt_text)

    try:
        send_comic_tg(tg_bot, tg_channel_id, comic)
    except Exception:
        sys.exit("Current image is too big for Telegram")
    finally:
        img_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
