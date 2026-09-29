import json
from feedgen.feed import FeedGenerator
from db import get_all_episodes

def rss_generator():
    fg = FeedGenerator()
    
    with open('podcast_info.json', 'r', encoding='utf-8') as f:
        content = json.load(f)

    fg.load_extension('podcast')

    fg.title(content["title"])
    fg.description(content["description"])
    fg.logo(content["image"])
    fg.language('ar')
    fg.author(content["author"])
    fg.generator(content["generator"])

    fg.podcast.itunes_author(content["author"])
    fg.podcast.itunes_summary(content["description"])
    fg.podcast.itunes_explicit('no')

    for episode in get_all_episodes():
        fe = fg.add_entry()
        fe.guid(episode['id'])
        fe.title(episode['title'])
        fe.description(episode['description'])
        fe.enclosure(episode['audio_url'], episode['size'], 'audio/mpeg')
        fe.podcast.ituens_duration(episode['duration'])
        fe.pubDate(episode['pub_date'])

    fg.rss_file('podcast.rss', pretty=True)
    print("RSS file generated successfully.")

if __name__ == "__main__":
    rss_generator()