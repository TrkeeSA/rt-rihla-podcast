import os
import asyncio
import httpx
from selectolax.parser import HTMLParser
from dotenv import load_dotenv
from db import add_episode
from utils.mp3_info import get_mp3_duration, get_mp3_size

load_dotenv()
base_url = os.getenv("BASE_URL")
episode_url = os.getenv("EPISODE_URL")

api_url = f"{base_url}{episode_url}"
max_results = 229

async def get_episodes_details():
    async with httpx.AsyncClient() as client:
        for i in range(max_results):
            episode_card = await client.get(f"{base_url}/{episode_url}{i}")
            if episode_card.status_code == 200:
                tree = HTMLParser(episode_card.text)
                link = tree.css_first(".post-card__link").attributes["href"]

                episode_page = await client.get(f"{base_url}{link}")
                episode_page_tree = HTMLParser(episode_page.text)

                title = episode_page_tree.css_first(".main-article__title").text()
                summary = episode_page_tree.css_first(".main-article__summary").text()
                audio_url = episode_page_tree.css_first("audio").attributes["src"]
                audio_duration = get_mp3_duration(audio_url)
                audio_size = get_mp3_size(audio_url)
                date = episode_page_tree.css_first(".main-article__date").text()

                await add_episode(title, summary, audio_url, audio_duration, audio_size, date)
            else:
                raise Exception(f"Failed to retrieve episode details: {episode_card.status_code}")

if __name__ == "__main__":
    asyncio.run(get_episodes_details())