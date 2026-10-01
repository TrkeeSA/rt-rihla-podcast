import os
import asyncio
import httpx
from selectolax.parser import HTMLParser
from dotenv import load_dotenv
from db import add_episode, last_episode as get_last_episode
from utils.mp3_info import get_mp3_duration, get_mp3_size
from utils.date_parse import parse_date

load_dotenv()
base_url = os.getenv("BASE_URL")
episode_url = os.getenv("EPISODE_URL")

api_url = f"{base_url}{episode_url}"
max_results = 230

async def update_episodes(last_ep):
    async with httpx.AsyncClient(follow_redirects=True) as client:
        for i in range(max_results):
            episode_card = await client.get(f"{base_url}/{episode_url}{i}")

            if episode_card.status_code == 404:
                print("Reached the end of episodes.")
                break
        
            if episode_card.status_code == 200:
                tree = HTMLParser(episode_card.text)
                link = tree.css_first(".post-card__link").attributes["href"]

                episode_page = await client.get(f"{base_url}{link}")
                episode_page_tree = HTMLParser(episode_page.text)

                audio_node = episode_page_tree.css_first("audio")
                title_node = episode_page_tree.css_first(".main-article__title")
                summary_node = episode_page_tree.css_first(".main-article__summary")
                date_node = episode_page_tree.css_first(".main-article__date")

                audio_url = audio_node.attributes.get("src") if audio_node else None
                title = title_node.text() if title_node else "No Title"
                summary = summary_node.text() if summary_node else ""
                date = parse_date(date_node.text()) if date_node else ""

                if not audio_url or (last_ep is None) or (last_ep >= date):
                    continue

                audio_duration = await asyncio.to_thread(get_mp3_duration, audio_url)
                audio_size = await asyncio.to_thread(get_mp3_size, audio_url)

                await asyncio.to_thread(
                    add_episode,
                    title, summary, audio_url, audio_duration, audio_size, date
                    )
                
                last_ep = date

                print(f"Episode added: {title} Successfully")
            else:
                raise Exception(f"Failed to retrieve episode details: {episode_card.status_code}")

if __name__ == "__main__":
    last_episode = get_last_episode()
    asyncio.run(update_episodes(last_episode))