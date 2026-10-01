import json, os
from feedgen.feed import FeedGenerator
from db import get_all_episodes

def generate_rss():
    fg = FeedGenerator()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_dir, 'podcast_info.json')

    with open(json_file_path, 'r', encoding='utf-8') as f:
        content = json.load(f)

    fg.load_extension('podcast')

    fg.title(content["title"])
    fg.id(content["id"])
    fg.description(content["description"])
    fg.link(href=content["link"])
    fg.logo(content["image"])
    fg.language('ar')
    fg.author(name=content["author"])
    fg.generator(content["generator"])

    fg.podcast.itunes_author(content["author"])
    fg.podcast.itunes_summary(content["description"])
    fg.podcast.itunes_explicit('no')

    for episode in get_all_episodes():
        fe = fg.add_entry()
        fe.id(str(episode['id']))
        fe.title(episode['title'])
        fe.description(episode['description'])
        fe.enclosure(episode['audio_url'], episode['size'], 'audio/mpeg')
        fe.podcast.itunes_duration(episode['duration'])
        fe.pubDate(episode['pub_date'])

    fg.rss_file('podcast.rss', pretty=True)
    print("RSS file generated successfully.")

if __name__ == "__main__":
    generate_rss()