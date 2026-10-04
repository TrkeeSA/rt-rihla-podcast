import asyncio
from update import update_episodes
from db import last_episode
from generate_rss import generate_rss

def main(le):
    asyncio.run(update_episodes(le))

if __name__ == "__main__":
    le = last_episode()
    main(le)