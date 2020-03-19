import feedparser
import datetime
import time
import ssl


if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


class FeedParser():
    def __init__(self, url):
        self.url = url
        self.source = {}
        self.entries = []
        self._feed_obj = feedparser.parse(self.url)
        self.parse_source()

    def parse_source(self):
        self.source['name'] = self._feed_obj.feed.get('title', '')
        self.source['description'] = self._feed_obj.feed.get('description', '')
        self.source['url'] = self._feed_obj.feed.get('link', '')
        self.source['feed_link'] = self.url
        self.source['icon'] = self._feed_obj.feed.get('icon', '')

        for entry in self._feed_obj.entries:
            entry_data = {}
            entry_data['title'] = entry.get('title', '')
            entry_data['content'] = entry.get('description', '')
            entry_data['link'] = entry.get('link', '')
            entry_data['author'] = entry.get('author', '')
            if entry.get('published_parsed', ''):
                entry_data['published_at'] = datetime.datetime.fromtimestamp(time.mktime(entry.get('published_parsed', '')))

            self.entries.append(entry_data)
        
