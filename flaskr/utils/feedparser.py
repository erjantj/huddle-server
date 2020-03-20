import feedparser
import datetime
import time
import ssl

from flaskr import helpers


if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


class FeedParser():
    def parse_source(self, url: str):
        feed_obj = feedparser.parse(url)
        source = {}
        entries = []

        source['name'] = feed_obj.feed.get('title', '')
        source['description'] = feed_obj.feed.get('description', '')
        source['url'] = helpers.get_base_url(feed_obj.feed.get('link', ''))
        source['feed_link'] = self.get_feed_link(feed_obj.feed, url)
        source['icon'] = feed_obj.feed.get('icon', '')

        for entry in feed_obj.entries:
            entry_data = {}
            entry_data['title'] = entry.get('title', '')
            entry_data['content'] = entry.get('description', '')
            entry_data['link'] = entry.get('link', '')
            entry_data['author'] = entry.get('author', '')
            if entry.get('published_parsed', ''):
                entry_data['published_at'] = datetime.datetime.fromtimestamp(time.mktime(entry.get('published_parsed', '')))

            entries.append(entry_data)

        return {'source': source, 'entries': entries}
        

    def get_feed_link(self, feed: dict, parsed_url: str) -> str:
        if feed.get('id', ''):
            return feed.get('id', '')

        if feed.get('links', ''):
            for link in feed.get('links', []):
                if link['type'] == 'application/rss+xml':
                    return link['href']

        return parsed_url


