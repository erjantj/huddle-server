import feedparser
import ssl


if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context


class FeedParser():
    def __init__(self, url):
        self.url = url
        self.source = {}
        self._feed_obj = None
        self.parse()

    def parse(self):
        self.feed_obj = feedparser.parse(self.url)
        self.parse_source()

    def parse_source(self):
        self.source['name'] = self.feed_obj.feed.get('title', '')
        self.source['description'] = self.feed_obj.feed.get('description', '')
        self.source['url'] = self.feed_obj.feed.get('link', '')
        self.source['feed_link'] = self.url
        self.source['icon'] = self.feed_obj.feed.get('icon', '')
        